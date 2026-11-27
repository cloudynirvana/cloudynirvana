// W-2750 stand controller v2: takes COMMANDS from the bunker and CALIBRATES its sensors.
// ESP32 DevKitC, pins match the KiCad stand box where Wokwi has the part:
//   V1 supply valve GPIO26, V2 vent valve GPIO33, ARM_SENSE GPIO25 (high = arm loop closed),
//   I2C SDA21/SCL22 -> MPU6050 IMU (GNC attitude reference on the stand / flight computer),
//   pressure P1/P2/P3 on ADC 34/35/32 (the real board reads them through the ADS1115).
// Commands (one per line, from the bunker over RS-485; here from the Serial monitor):
//   HB        heartbeat, bunker sends every 200 ms; none for 500 ms while counting/running = abort
//   STATUS    one-line report
//   CAL_P     zero the three pressure sensors (supply shut, vent open: sensors see 0 bar gauge)
//   CAL_IMU   gyro bias + level (stand still); rejected if moving, or during countdown/run
//   FIRE      start countdown + 5 s water run (needs ARMED, link OK, both calibrations valid)
//   ABORT     shut supply, open vent, latch until the arm key is cycled
// The hardware arm loop (key + E-stop) cuts valve power directly; software only mirrors it.
#include <Wire.h>
#define TEST_SCRIPT 0      // 1..4 = scripted test cases (commands injected on a timer), 0 = live

const int P_PIN[3] = {34, 35, 32};
const int ARM_PIN = 25, V1_PIN = 26, V2_PIN = 33;
const int MPU = 0x68;
const float REDLINE_BAR = 8.0;
const unsigned long RUN_MS = 5000, COUNTDOWN_MS = 3000, LINK_TIMEOUT_MS = 500;

enum { SAFE, ARMED, COUNTDOWN, RUNNING };
const char* NAMES[] = {"SAFE", "ARMED", "COUNTDOWN", "RUNNING"};
int state = SAFE;
bool latched = false, calP = false, calI = false;
unsigned long stateStart = 0, lastHB = 0, lastLog = 0, lastAtt = 0, lastImu = 0;
float pOff[3] = {0, 0, 0};
float gBias[3] = {0, 0, 0};        // deg/s
float levelRoll = 0, levelPitch = 0; // deg
float roll = 0, pitch = 0;           // complementary-filter attitude, deg

// ---- sensors ----
float rawBar(int i) {
  float v = analogRead(P_PIN[i]) * 10.0 / 4095.0;
#if TEST_SCRIPT
  const float zeroErr[3] = {0.31, -0.12, 0.22};   // stand-in for real transducer zero errors (Wokwi knobs read exactly 0)
  v += zeroErr[i];
#endif
  return v;
}
float bar(int i) { return rawBar(i) - pOff[i]; }

bool readImu(float a[3], float g[3]) {
  Wire.beginTransmission(MPU); Wire.write(0x3B);
  if (Wire.endTransmission(false) != 0) return false;
  Wire.requestFrom(MPU, 14);
  int16_t r[7];
  for (int k = 0; k < 7; k++) r[k] = (Wire.read() << 8) | Wire.read();
  for (int k = 0; k < 3; k++) { a[k] = r[k] / 16384.0; g[k] = r[k + 4] / 131.0; }
  return true;
}

// ---- valves ----
void setValves(bool supplyOpen, bool ventClosed) {
  digitalWrite(V1_PIN, supplyOpen ? HIGH : LOW);
  digitalWrite(V2_PIN, ventClosed ? HIGH : LOW);
}
void goSafe(const char* why) {
  setValves(false, false);
  if (state != SAFE || strcmp(why, "ABORT command") == 0) {
    Serial.print("# SAFE: "); Serial.println(why);
    latched = true;
    Serial.println("# cycle the ARM key to re-arm");
  }
  state = SAFE;
}

// ---- calibration ----
void calPressure() {
  if (state > ARMED) { Serial.println("NAK CAL_P: not during countdown/run"); return; }
  float s[3] = {0, 0, 0}, mx[3] = {-99, -99, -99}, mn[3] = {99, 99, 99};
  for (int n = 0; n < 200; n++) {
    for (int i = 0; i < 3; i++) { float v = rawBar(i); s[i] += v; mx[i] = max(mx[i], v); mn[i] = min(mn[i], v); }
    delay(2);
  }
  for (int i = 0; i < 3; i++) {
    float off = s[i] / 200.0;
    if (fabs(off) > 0.5 || mx[i] - mn[i] > 0.2) {
      Serial.print("NAK CAL_P: P"); Serial.print(i + 1); Serial.print(" offset "); Serial.print(off, 3);
      Serial.println(" bar is too large or noisy, check the sensor"); calP = false; return;
    }
    pOff[i] = off;
  }
  calP = true;
  Serial.print("ACK CAL_P offsets bar: "); Serial.print(pOff[0], 3); Serial.print(' ');
  Serial.print(pOff[1], 3); Serial.print(' '); Serial.println(pOff[2], 3);
}

void calImu() {
  if (state > ARMED) { Serial.println("NAK CAL_IMU: not during countdown/run"); return; }
  const int N = 400;
  double sa[3] = {0}, sg[3] = {0}, sg2[3] = {0};
  float a[3], g[3];
  for (int n = 0; n < N; n++) {
    if (!readImu(a, g)) { Serial.println("NAK CAL_IMU: no IMU on I2C"); calI = false; return; }
    for (int k = 0; k < 3; k++) { sa[k] += a[k]; sg[k] += g[k]; sg2[k] += g[k] * g[k]; }
    delay(2);
  }
  float gm = 0;
  for (int k = 0; k < 3; k++) {
    float m = sg[k] / N, var = sg2[k] / N - m * m;
    if (var > 0.25) { Serial.println("NAK CAL_IMU: stand is moving, hold still and retry"); calI = false; return; }
    gBias[k] = m;
  }
  float ax = sa[0] / N, ay = sa[1] / N, az = sa[2] / N;
  gm = sqrt(ax * ax + ay * ay + az * az);
  if (fabs(gm - 1.0) > 0.05) { Serial.print("NAK CAL_IMU: |g| = "); Serial.print(gm, 3); Serial.println(" g, accel scale fault"); calI = false; return; }
  levelRoll = atan2(ay, az) * 57.2958;
  levelPitch = atan2(-ax, sqrt(ay * ay + az * az)) * 57.2958;
  roll = pitch = 0;
  calI = true;
  Serial.print("ACK CAL_IMU gyro bias dps: "); Serial.print(gBias[0], 3); Serial.print(' ');
  Serial.print(gBias[1], 3); Serial.print(' '); Serial.print(gBias[2], 3);
  Serial.print("  level roll/pitch deg: "); Serial.print(levelRoll, 2); Serial.print(' '); Serial.print(levelPitch, 2);
  Serial.print("  |g| "); Serial.println(gm, 3);
}

void status() {
  Serial.print("STATUS "); Serial.print(NAMES[state]);
  Serial.print(" arm="); Serial.print(digitalRead(ARM_PIN));
  Serial.print(" link="); Serial.print(millis() - lastHB < LINK_TIMEOUT_MS ? "OK" : "LOST");
  Serial.print(" calP="); Serial.print(calP); Serial.print(" calIMU="); Serial.print(calI);
  Serial.print(" P bar="); for (int i = 0; i < 3; i++) { Serial.print(bar(i), 2); Serial.print(i < 2 ? "," : ""); }
  Serial.print(" att roll/pitch="); Serial.print(roll, 2); Serial.print('/'); Serial.println(pitch, 2);
}

void command(String c) {
  c.trim(); c.toUpperCase();
  if (c == "HB") { lastHB = millis(); return; }
  Serial.print("> "); Serial.println(c);
  if (c == "STATUS") status();
  else if (c == "CAL_P") calPressure();
  else if (c == "CAL_IMU") calImu();
  else if (c == "ABORT") goSafe("ABORT command");
  else if (c == "FIRE") {
    if (state != ARMED) Serial.println("NAK FIRE: not ARMED");
    else if (!calP || !calI) Serial.println("NAK FIRE: calibrate first (CAL_P, CAL_IMU)");
    else if (millis() - lastHB >= LINK_TIMEOUT_MS) Serial.println("NAK FIRE: no link");
    else { state = COUNTDOWN; stateStart = millis(); Serial.println("ACK FIRE: countdown 3 s"); }
  } else Serial.println("NAK unknown command");
}

#if TEST_SCRIPT
struct Step { unsigned long t; const char* cmd; };
// heartbeats are generated separately (see hbStopAt)
#if TEST_SCRIPT == 1   // normal: calibrate, then fire
Step steps[] = {{500, "STATUS"}, {800, "CAL_P"}, {1500, "CAL_IMU"}, {3500, "STATUS"}, {4000, "FIRE"}, {13000, "STATUS"}};
unsigned long hbStopAt = 99999999;
#elif TEST_SCRIPT == 2 // fire without calibration is refused
Step steps[] = {{500, "FIRE"}, {800, "CAL_P"}, {1200, "FIRE"}, {1500, "CAL_IMU"}, {3000, "FIRE"}, {6500, "CAL_IMU"}, {7000, "ABORT"}, {7500, "STATUS"}};
unsigned long hbStopAt = 99999999;
#elif TEST_SCRIPT == 3 // link lost during the run
Step steps[] = {{800, "CAL_P"}, {1500, "CAL_IMU"}, {3000, "FIRE"}, {9000, "STATUS"}};
unsigned long hbStopAt = 7000;
#else                  // calibration while armed is refused; uncalibrated attitude drifts
Step steps[] = {{300, "STATUS"}, {2300, "STATUS"}, {2500, "CAL_IMU"}, {6000, "STATUS"}};
unsigned long hbStopAt = 99999999;
#endif
int stepIdx = 0; unsigned long lastFakeHB = 0;
#endif

void setup() {
  Serial.begin(115200);
  pinMode(ARM_PIN, INPUT);
  pinMode(V1_PIN, OUTPUT); pinMode(V2_PIN, OUTPUT);
  setValves(false, false);
  Wire.begin(21, 22);
  Wire.beginTransmission(MPU); Wire.write(0x6B); Wire.write(0); Wire.endTransmission();
  Serial.println("# W-2750 stand controller v2 ready (commands: HB STATUS CAL_P CAL_IMU FIRE ABORT)");
}

String line;
void loop() {
  unsigned long now = millis();
#if TEST_SCRIPT
  if (now < hbStopAt && now - lastFakeHB >= 200) { lastFakeHB = now; command("HB"); }
  if (stepIdx < (int)(sizeof(steps) / sizeof(steps[0])) && now >= steps[stepIdx].t) command(steps[stepIdx++].cmd);
#endif
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n' || ch == '\r') { if (line.length()) command(line); line = ""; }
    else line += ch;
  }
  // attitude: complementary filter at 100 Hz (gyro bias and level removed once calibrated)
  if (now - lastImu >= 10) {
    float dt = (now - lastImu) / 1000.0; lastImu = now;
    float a[3], g[3];
    if (readImu(a, g) && dt < 0.1) {
      float ar = atan2(a[1], a[2]) * 57.2958 - levelRoll;
      float ap = atan2(-a[0], sqrt(a[1] * a[1] + a[2] * a[2])) * 57.2958 - levelPitch;
      roll = 0.995 * (roll + (g[0] - gBias[0]) * dt) + 0.005 * ar;
      pitch = 0.995 * (pitch + (g[1] - gBias[1]) * dt) + 0.005 * ap;
    }
  }
  bool armOn = digitalRead(ARM_PIN) == HIGH;
  bool linkOk = now - lastHB < LINK_TIMEOUT_MS;
  float p2 = bar(1);
  if (!armOn && state != SAFE) goSafe("arm loop open (key off / E-stop)");
  else if (!linkOk && state >= COUNTDOWN) goSafe("link lost > 500 ms");
  else if (p2 > REDLINE_BAR && state == RUNNING) goSafe("P2 over redline");
  if (!armOn) latched = false;
  if (state == SAFE && armOn && !latched) { state = ARMED; Serial.println("# ARMED"); }
  else if (state == COUNTDOWN && now - stateStart >= COUNTDOWN_MS) {
    state = RUNNING; stateStart = now; setValves(true, true);
    Serial.println("t_ms,P1_bar,P2_bar,P3_bar,roll_deg,pitch_deg,state");
  } else if (state == RUNNING && now - stateStart >= RUN_MS) {
    setValves(false, false); Serial.println("# RUN COMPLETE, vent open"); state = ARMED;
  }
  if (state == RUNNING && now - lastLog >= 100) {   // 10 Hz in the sim (50 Hz on hardware)
    lastLog = now;
    Serial.print(now); for (int i = 0; i < 3; i++) { Serial.print(','); Serial.print(bar(i), 2); }
    Serial.print(','); Serial.print(roll, 2); Serial.print(','); Serial.print(pitch, 2);
    Serial.print(','); Serial.println(NAMES[state]);
  }
}
