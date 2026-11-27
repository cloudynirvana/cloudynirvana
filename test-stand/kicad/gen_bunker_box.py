"""Generate the W-2750 test stand 'bunker box' (operator console) schematic for KiCad (7+).

Every pin gets a short wire and a net label, so the schematic is drawn from
the net list below. Change a net here and run again:
    python gen_bunker_box.py      (needs: pip install kiutils, KiCad symbol libraries)
Then check it:  kicad-cli sch erc bunker_box.kicad_sch
"""
import copy, os, sys, uuid
from kiutils.schematic import Schematic
from kiutils.symbol import SymbolLib
from kiutils.items.schitems import SchematicSymbol, LocalLabel, Connection, NoConnect, Text
from kiutils.items.common import Position, Property, Effects, Font, Justify

_cands = [os.environ.get("KICAD_SYMBOL_DIR", ""),
          os.path.expandvars(r"%LOCALAPPDATA%\Programs\KiCad\10.0\share\kicad\symbols"),
          r"C:\Program Files\KiCad\10.0\share\kicad\symbols", "/usr/share/kicad/symbols"]
SYMDIR = next(p for p in _cands if p and os.path.isdir(p))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bunker_box.kicad_sch")
FP_R = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
FP_D = "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal"
FP_TB2 = "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal"
FP_H = lambda n: f"Connector_PinSocket_2.54mm:PinSocket_1x{n:02d}_P2.54mm_Vertical"

_libs = {}
def libsym(lib, name):
    if lib not in _libs:
        _libs[lib] = SymbolLib.from_file(os.path.join(SYMDIR, lib + ".kicad_sym"))
    s = [x for x in _libs[lib].symbols if x.entryName == name][0]
    assert s.extends is None, f"{lib}:{name} is a derived symbol"
    return s

# ---------------- the circuit: (ref, lib, symbol, value, footprint, x, y, {pin: net}) ----------------
P = []
def part(ref, lib, sym, value, fp, x, y, nets): P.append((ref, lib, sym, value, fp, x, y, nets))

# ESP32-DevKitC v4 in two 19-pin sockets (same socket layout as the stand box)
# left: 3V3 EN VP VN 34 35 32 33 25 26 27 14 12 GND 13 D2 D3 CMD 5V
left = ["+3V3", None, None, None, "ARM_SENSE", None, "ARM_BTN", "FIRE_BTN", "LED_ARMED", "LED_LINK", "LED_RUN",
        "BUZZER", None, "GND", None, None, None, None, "+5V"]
# right: GND 23 22 TX RX 21 GND 19 18 5 17 16 4 0 2 15 D1 D0 CLK
right = ["GND", None, "I2C_SCL", None, None, "I2C_SDA", "GND", None, None, None,
         "RS485_DI", "RS485_RO_3V3", "RS485_DE_RE", None, None, None, None, None, None]
part("J1", "Connector_Generic", "Conn_01x19", "ESP32 DevKitC left (3V3..5V)", FP_H(19), 50.8, 76.2,
     {str(i + 1): n for i, n in enumerate(left)})
part("J2", "Connector_Generic", "Conn_01x19", "ESP32 DevKitC right (GND..CLK)", FP_H(19), 50.8, 147.32,
     {str(i + 1): n for i, n in enumerate(right)})

# Power: own 12 V battery + buck to 5 V (bunker and stand share no power, only RS-485 and the arm loop)
part("J3", "Connector", "Screw_Terminal_01x02", "12V battery in", FP_TB2, 106.68, 38.1, {"1": "+12V", "2": "GND"})
part("J5", "Connector_Generic", "Conn_01x04", "Buck 12V->5V module (IN+ IN- OUT+ OUT-)", FP_H(4), 106.68, 63.5,
     {"1": "+12V", "2": "GND", "3": "+5V", "4": "GND"})

# Arm loop: the stand's +12V comes down the cable, through the KEY and the E-STOP (NC), and goes back as ARM_RETURN.
# Turning the key off or hitting the E-stop drops the stand's arm relay in hardware, whatever the software does.
part("J4", "Connector", "Screw_Terminal_01x02", "Arm loop cable to stand (LOOP_12V, ARM_RETURN)", FP_TB2, 157.48, 38.1,
     {"1": "LOOP_12V", "2": "ARM_RETURN"})
part("J6", "Connector", "Screw_Terminal_01x02", "Panel KEY switch (SPST, key removable in OFF)", FP_TB2, 157.48, 63.5,
     {"1": "LOOP_12V", "2": "KEY_OUT"})
part("J7", "Connector", "Screw_Terminal_01x02", "Panel E-STOP (mushroom, NC contact)", FP_TB2, 157.48, 88.9,
     {"1": "KEY_OUT", "2": "ARM_RETURN"})
# Sense the loop at the bunker (12 V -> 2.8 V). Bunker GND is joined to stand GND by the cable's GND/shield core.
part("J8", "Connector", "Screw_Terminal_01x02", "Cable GND / shield to stand", FP_TB2, 157.48, 114.3,
     {"1": "GND", "2": "GND"})
part("R1", "Device", "R", "10k", FP_R, 205.74, 38.1, {"1": "ARM_RETURN", "2": "ARM_SENSE"})
part("R2", "Device", "R", "3.3k", FP_R, 205.74, 58.42, {"1": "ARM_SENSE", "2": "GND"})

# Operator buttons (normally open, active low, 10k pull-ups to 3V3)
part("J9", "Connector", "Screw_Terminal_01x02", "ARM button (NO)", FP_TB2, 106.68, 101.6, {"1": "ARM_BTN", "2": "GND"})
part("R3", "Device", "R", "10k", FP_R, 93.98, 116.84, {"1": "+3V3", "2": "ARM_BTN"})
part("J10", "Connector", "Screw_Terminal_01x02", "FIRE button (NO, guarded cover)", FP_TB2, 106.68, 132.08,
     {"1": "FIRE_BTN", "2": "GND"})
part("R4", "Device", "R", "10k", FP_R, 93.98, 147.32, {"1": "+3V3", "2": "FIRE_BTN"})

# Status lamps: GPIO -> 330R -> LED anode, cathode to GND (LED pin 1 = K, 2 = A)
for i, (net, col) in enumerate([("LED_ARMED", "red ARMED"), ("LED_LINK", "green LINK OK"), ("LED_RUN", "amber RUNNING")]):
    x = 205.74 + 25.4 * i
    part(f"R{5+i}", "Device", "R", "330", FP_R, x, 101.6, {"1": net, "2": f"{net}_A"})
    part(f"D{1+i}", "Device", "LED", col, "LED_THT:LED_D5.0mm", x, 127.0, {"2": f"{net}_A", "1": "GND"})

# Buzzer module (active, 5 V, logic input) for countdown and abort tones
part("J11", "Connector_Generic", "Conn_01x03", "Buzzer module (VCC GND IN)", FP_H(3), 106.68, 167.64,
     {"1": "+5V", "2": "GND", "3": "BUZZER"})
# OLED 128x64 I2C status display
part("J12", "Connector_Generic", "Conn_01x04", "OLED SSD1306 I2C (GND VCC SCL SDA)", FP_H(4), 137.16, 167.64,
     {"1": "GND", "2": "+3V3", "3": "I2C_SCL", "4": "I2C_SDA"})

# RS-485 module + link terminal (A/B twisted pair to the stand)
part("J13", "Connector_Generic", "Conn_01x08", "MAX485 module (RO RE DE DI VCC B A GND)", FP_H(8), 106.68, 213.36,
     {"1": "RS485_RO", "2": "RS485_DE_RE", "3": "RS485_DE_RE", "4": "RS485_DI", "5": "+5V", "6": "RS485_B",
      "7": "RS485_A", "8": "GND"})
part("R8", "Device", "R", "1k", FP_R, 132.08, 205.74, {"1": "RS485_RO", "2": "RS485_RO_3V3"})
part("R9", "Device", "R", "2k", FP_R, 132.08, 223.52, {"1": "RS485_RO_3V3", "2": "GND"})
part("R10", "Device", "R", "120", FP_R, 182.88, 205.74, {"1": "RS485_A", "2": "RS485_B"})
part("J14", "Connector", "Screw_Terminal_01x02", "RS-485 link to stand (A B)", FP_TB2, 157.48, 213.36,
     {"1": "RS485_A", "2": "RS485_B"})

# ---------------- build the schematic ----------------
def uid(): return str(uuid.uuid4())
sch = Schematic.create_new()
sch.paper.paperSize = "A3"
added = set()
OUTWARD = {0: (-1, 0), 180: (1, 0), 90: (0, 1), 270: (0, -1)}
LABEL_ANGLE = {0: 180, 180: 0, 90: 270, 270: 90}
STUB = 2.54
nets_seen = {}
for ref, lib, sym, value, fp, x, y, nets in P:
    s = libsym(lib, sym)
    key = f"{lib}:{sym}"
    if key not in added:
        c = copy.deepcopy(s); c.libraryNickname = lib; c.entryName = sym
        sch.libSymbols.append(c); added.add(key)
    pins = {p.number: p for u in s.units for p in u.pins}
    missing = set(nets) - set(pins)
    assert not missing, f"{ref}: pins {missing} not on {key}"
    ss = SchematicSymbol(); ss.libraryNickname = lib; ss.entryName = sym
    ss.position = Position(x, y, 0); ss.unit = 1; ss.inBom = True; ss.onBoard = True; ss.uuid = uid()
    ss.properties = [
        Property("Reference", ref, 0, Position(x, y - 12.7, 0), Effects(Font(height=1.27, width=1.27))),
        Property("Value", value, 1, Position(x, y + 12.7, 0), Effects(Font(height=1.27, width=1.27))),
        Property("Footprint", fp, 2, Position(x, y, 0), Effects(Font(height=1.27, width=1.27), hide=True)),
        Property("Datasheet", "~", 3, Position(x, y, 0), Effects(Font(height=1.27, width=1.27), hide=True)),
    ]
    ss.pins = {num: uid() for num in pins}
    sch.schematicSymbols.append(ss)
    for num, p in pins.items():
        px, py = round(x + p.position.X, 2), round(y - p.position.Y, 2)
        net = nets.get(num)
        if net is None:
            sch.noConnects.append(NoConnect(position=Position(px, py), uuid=uid()))
            continue
        dx, dy = OUTWARD[int(p.position.angle or 0)]
        ex, ey = round(px + dx * STUB, 2), round(py + dy * STUB, 2)
        sch.graphicalItems.append(Connection(type="wire", points=[Position(px, py), Position(ex, ey)], uuid=uid()))
        sch.labels.append(LocalLabel(text=net, position=Position(ex, ey, LABEL_ANGLE[int(p.position.angle or 0)]),
                                     effects=Effects(Font(height=1.27, width=1.27), justify=Justify(horizontally="right" if LABEL_ANGLE[int(p.position.angle or 0)] in (180, 270) else "left")),
                                     uuid=uid()))
        nets_seen.setdefault(net, []).append(f"{ref}.{num}")

lonely = {n: v for n, v in nets_seen.items() if len(v) < 2}
assert not lonely, f"nets with only one pin: {lonely}"
for i, line in enumerate(["W-2750 TEST STAND - BUNKER BOX / operator console (Phase 1 water tests). Generated by gen_bunker_box.py.",
                          "KEY and E-STOP are in series in the arm loop: either one drops the stand arm relay in hardware."]):
    sch.texts.append(Text(text=line, position=Position(25.4, 20.32 + 5.08 * i, 0),
                          effects=Effects(Font(height=2.0, width=2.0), justify=Justify(horizontally="left")), uuid=uid()))
sch.to_file(OUT)
print(f"wrote {OUT}: {len(P)} parts, {len(nets_seen)} nets")
