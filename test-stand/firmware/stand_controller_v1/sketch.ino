// W-2750 test stand controller, Phase 1 (water flow), Wokwi prototype on ESP32.
// Knobs = pressure sensors P1 supply, P2 injector manifold, P3 outlet (0-10 bar).
// KEY switch   = the hardware arm loop (key + E-stop). Off = SAFE, always.
//                After any abort, turn it off and on again to re-arm.
// LINK switch  = the RS-485 link to the bunker. Off = link lost.
// RUN button   = hold 2 s while armed to start a timed water run.
// LEDs: V1 supply valve (green = open), V2 vent (red = vent OPEN), ARM (yellow).
// Serial prints CSV at 50 Hz during a run: t_ms,P1,P2,P3,V1,V2,state
// Hardware note: on the real board the key loop cuts valve POWER directly.
// This code only mirrors it; it never relies on software to make the stand safe.

const int P1_PIN = 34, P2_PIN = 35, P3_PIN = 32;
const int KEY_PIN = 25, LINK_PIN = 26, RUN_PIN = 27;
const int V1_PIN = 18;   // supply, normally closed: HIGH = energised = open
const int V2_PIN = 19;   // vent, normally open:     HIGH = energised = closed
const int ARM_LED = 21;
const int V2_LED = 22;   // lit while the vent is OPEN (de-energised)

const float REDLINE_BAR = 8.0;           // P2 abort limit
const unsigned long RUN_MS = 5000;       // water run length
const unsigned long COUNTDOWN_MS = 3000;
const unsigned long HOLD_MS = 2000;      // RUN must be held this long
const unsigned long LINK_TIMEOUT_MS = 500;
const unsigned long HEARTBEAT_MS = 200;  // bunker sends one every 200 ms

// States: 0 SAFE, 1 ARMED, 2 COUNTDOWN, 3 RUNNING
int state = 0;
const char* NAMES[] = {"SAFE", "ARMED", "COUNTDOWN", "RUNNING"};
bool latched = false;  // set by any abort; cleared only by turning the key OFF
unsigned long stateStart = 0, holdStart = 0, lastHeartbeat = 0, lastBeatSent = 0, lastLog = 0;

float readBar(int pin) {
  return analogRead(pin) * 10.0 / 4095.0;  // real board: 0.5-4.5 V -> 0-10 bar
}

void setValves(bool supplyOpen, bool ventClosed) {
  digitalWrite(V1_PIN, supplyOpen ? HIGH : LOW);
  digitalWrite(V2_PIN, ventClosed ? HIGH : LOW);
  digitalWrite(V2_LED, ventClosed ? LOW : HIGH);
}

void goSafe(const char* why) {
  setValves(false, false);  // supply shut, vent open
  if (state != 0) {
    Serial.print("# SAFE: ");
    Serial.println(why);
    latched = true;
    Serial.println("# Turn the KEY off and on again to re-arm");
  }
  state = 0;
  holdStart = 0;
}

void setup() {
  Serial.begin(115200);
  pinMode(KEY_PIN, INPUT_PULLUP);   // switch to GND = armed
  pinMode(LINK_PIN, INPUT_PULLUP);  // switch to GND = link up
  pinMode(RUN_PIN, INPUT_PULLUP);
  pinMode(V1_PIN, OUTPUT);
  pinMode(V2_PIN, OUTPUT);
  pinMode(ARM_LED, OUTPUT);
  pinMode(V2_LED, OUTPUT);
  setValves(false, false);
  Serial.println("# W-2750 stand controller ready. Turn KEY on, hold RUN 2 s.");
}

void loop() {
  unsigned long now = millis();
  bool keyOn = digitalRead(KEY_PIN) == LOW;
  bool linkUp = digitalRead(LINK_PIN) == LOW;
  bool runPressed = digitalRead(RUN_PIN) == LOW;

  // Simulated bunker heartbeat: arrives every 200 ms while the link is up
  if (linkUp && now - lastBeatSent >= HEARTBEAT_MS) {
    lastBeatSent = now;
    lastHeartbeat = now;
  }
  bool linkOk = now - lastHeartbeat < LINK_TIMEOUT_MS;

  float p1 = readBar(P1_PIN), p2 = readBar(P2_PIN), p3 = readBar(P3_PIN);

  // Abort checks, in priority order
  if (!keyOn && state != 0) goSafe("key off / E-stop");
  else if (!linkOk && state >= 2) goSafe("link lost > 500 ms");
  else if (p2 > REDLINE_BAR && state == 3) goSafe("P2 over redline");

  digitalWrite(ARM_LED, keyOn ? HIGH : LOW);

  if (!keyOn) latched = false;
  if (state == 0 && keyOn && !latched) {
    state = 1;
    Serial.println("# ARMED");
  } else if (state == 1) {
    if (runPressed && linkOk) {
      if (holdStart == 0) holdStart = now;
      if (now - holdStart >= HOLD_MS) {
        state = 2;
        stateStart = now;
        Serial.println("# COUNTDOWN 3 s");
      }
    } else {
      holdStart = 0;
    }
  } else if (state == 2 && now - stateStart >= COUNTDOWN_MS) {
    state = 3;
    stateStart = now;
    setValves(true, true);  // vent closed, supply open
    Serial.println("t_ms,P1_bar,P2_bar,P3_bar,V1,V2_closed,state");
  } else if (state == 3 && now - stateStart >= RUN_MS) {
    setValves(false, false);
    Serial.println("# RUN COMPLETE, vent open");
    state = keyOn ? 1 : 0;
    holdStart = 0;
  }

  if (state == 3 && now - lastLog >= 20) {  // 50 Hz log
    lastLog = now;
    Serial.print(now); Serial.print(',');
    Serial.print(p1, 2); Serial.print(',');
    Serial.print(p2, 2); Serial.print(',');
    Serial.print(p3, 2); Serial.print(',');
    Serial.print(digitalRead(V1_PIN)); Serial.print(',');
    Serial.print(digitalRead(V2_PIN)); Serial.print(',');
    Serial.println(NAMES[state]);
  }
}
