"""Generate the W-2750 test stand 'stand box' schematic for KiCad (7+).

Every pin gets a short wire and a net label, so the schematic is drawn from
the net list below. Change a net here and run again:
    python gen_stand_box.py      (needs: pip install kiutils, KiCad symbol libraries)
Then check it:  kicad-cli sch erc stand_box.kicad_sch
"""
import copy, os, sys, uuid
from kiutils.schematic import Schematic
from kiutils.symbol import SymbolLib
from kiutils.items.schitems import SchematicSymbol, LocalLabel, Connection, NoConnect, Text
from kiutils.items.common import Position, Property, Effects, Font, Justify

SYMDIR = os.environ.get("KICAD_SYMBOL_DIR", "/usr/share/kicad/symbols")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stand_box.kicad_sch")
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

# ESP32-DevKitC v4 plugs into two 19-pin sockets
left = ["+3V3", None, None, None, None, None, None, "V2_CMD", "ARM_SENSE", "V1_CMD", "FLOW", "ONEWIRE",
        None, "GND", "CAM_CMD", None, None, None, "+5V"]
right = ["GND", "SD_MOSI", "I2C_SCL", None, None, "I2C_SDA", "GND", "SD_MISO", "SD_SCK", "SD_CS",
         "RS485_DI", "RS485_RO_3V3", "RS485_DE_RE", None, None, None, None, None, None]
part("J1", "Connector_Generic", "Conn_01x19", "ESP32 DevKitC left (3V3..5V)", FP_H(19), 50.8, 76.2,
     {str(i + 1): n for i, n in enumerate(left)})
part("J2", "Connector_Generic", "Conn_01x19", "ESP32 DevKitC right (GND..CLK)", FP_H(19), 50.8, 147.32,
     {str(i + 1): n for i, n in enumerate(right)})

# Power in, arm loop, arm relay
part("J3", "Connector", "Screw_Terminal_01x02", "12V battery in", FP_TB2, 106.68, 38.1, {"1": "+12V", "2": "GND"})
part("J4", "Connector", "Screw_Terminal_01x02", "Arm loop to bunker key + E-stop", FP_TB2, 106.68, 63.5,
     {"1": "+12V", "2": "ARM_RETURN"})
part("K1", "Relay", "G5LE-1", "Arm relay 12V", "Relay_THT:Relay_SPDT_Omron-G5LE-1", 157.48, 50.8,
     {"5": "ARM_RETURN", "2": "GND", "1": "+12V", "4": "+12V_ARMED", "3": None})
part("D1", "Device", "D", "1N4007", FP_D, 190.5, 38.1, {"1": "ARM_RETURN", "2": "GND"})
part("J5", "Connector_Generic", "Conn_01x04", "Buck 12V->5V module (IN+ IN- OUT+ OUT-)", FP_H(4), 106.68, 91.44,
     {"1": "+12V", "2": "GND", "3": "+5V", "4": "GND"})
part("R1", "Device", "R", "10k", FP_R, 220.98, 38.1, {"1": "+12V_ARMED", "2": "ARM_SENSE"})
part("R2", "Device", "R", "3.3k", FP_R, 220.98, 58.42, {"1": "ARM_SENSE", "2": "GND"})

# Valve drivers: V1 supply (normally closed), V2 vent (normally open)
for i, (x, name) in enumerate([(157.48, "V1 supply valve (NC)"), (220.98, "V2 vent valve (NO)")]):
    n, y = i + 1, 101.6
    part(f"R{10+n}", "Device", "R", "100", FP_R, x - 20.32, y + 15.24, {"1": f"V{n}_CMD", "2": f"V{n}_GATE"})
    part(f"R{12+n}", "Device", "R", "10k", FP_R, x - 10.16, y + 30.48, {"1": f"V{n}_GATE", "2": "GND"})
    part(f"Q{n}", "Device", "Q_NMOS_GDS", "IRLZ44N", "Package_TO_SOT_THT:TO-220-3_Vertical", x, y + 15.24,
         {"1": f"V{n}_GATE", "2": f"V{n}_DRAIN", "3": "GND"})
    part(f"D{1+n}", "Device", "D", "1N4007", FP_D, x + 15.24, y - 7.62, {"1": "+12V_ARMED", "2": f"V{n}_DRAIN"})
    part(f"J{5+n}", "Connector", "Screw_Terminal_01x02", name, FP_TB2, x + 20.32, y + 10.16,
         {"1": "+12V_ARMED", "2": f"V{n}_DRAIN"})

# Camera trigger through an optocoupler
part("R15", "Device", "R", "330", FP_R, 106.68, 167.64, {"1": "CAM_CMD", "2": "CAM_LED"})
part("U1", "Isolator", "PC817", "PC817", "Package_DIP:DIP-4_W7.62mm", 127.0, 167.64,
     {"1": "CAM_LED", "2": "GND", "3": "CAM_E", "4": "CAM_C"})
part("J8", "Connector", "Screw_Terminal_01x02", "Camera trigger out", FP_TB2, 149.86, 167.64, {"1": "CAM_C", "2": "CAM_E"})

# ADS1115 module + 3 pressure transducers (0.5-4.5 V) through 10k/20k dividers (max 3.0 V)
part("J9", "Connector_Generic", "Conn_01x10", "ADS1115 module (VDD GND SCL SDA ADDR ALRT A0-A3)", FP_H(10),
     190.5, 167.64, {"1": "+3V3", "2": "GND", "3": "I2C_SCL", "4": "I2C_SDA", "5": "GND", "6": None,
                     "7": "P1_ADC", "8": "P2_ADC", "9": "P3_ADC", "10": None})
for k in (1, 2, 3):
    x = 210.82 + 25.4 * (k - 1)
    part(f"J{9+k}", "Connector_Generic", "Conn_01x03", f"P{k} pressure sensor (5V GND SIG)", FP_H(3), x + 12.7, 200.66,
         {"1": "+5V", "2": "GND", "3": f"P{k}_SIG"})
    part(f"R{20+k}", "Device", "R", "10k", FP_R, x, 218.44, {"1": f"P{k}_SIG", "2": f"P{k}_ADC"})
    part(f"R{23+k}", "Device", "R", "20k", FP_R, x, 236.22, {"1": f"P{k}_ADC", "2": "GND"})

# Flow meter, two DS18B20 temperature probes
part("J13", "Connector_Generic", "Conn_01x03", "F1 flow meter (5V GND PULSE)", FP_H(3), 106.68, 200.66,
     {"1": "+5V", "2": "GND", "3": "FLOW"})
part("R27", "Device", "R", "10k", FP_R, 93.98, 218.44, {"1": "+3V3", "2": "FLOW"})
part("J14", "Connector_Generic", "Conn_01x03", "T1 DS18B20 (3V3 GND DATA)", FP_H(3), 137.16, 200.66,
     {"1": "+3V3", "2": "GND", "3": "ONEWIRE"})
part("J15", "Connector_Generic", "Conn_01x03", "T2 DS18B20 (3V3 GND DATA)", FP_H(3), 162.56, 200.66,
     {"1": "+3V3", "2": "GND", "3": "ONEWIRE"})
part("R28", "Device", "R", "4.7k", FP_R, 124.46, 218.44, {"1": "+3V3", "2": "ONEWIRE"})

# microSD module and RS-485 module + bunker link terminal
part("J16", "Connector_Generic", "Conn_01x06", "microSD module (GND VCC MISO MOSI SCK CS)", FP_H(6), 106.68, 129.54,
     {"1": "GND", "2": "+5V", "3": "SD_MISO", "4": "SD_MOSI", "5": "SD_SCK", "6": "SD_CS"})
part("J17", "Connector_Generic", "Conn_01x08", "MAX485 module (RO RE DE DI VCC B A GND)", FP_H(8), 106.68, 251.46,
     {"1": "RS485_RO", "2": "RS485_DE_RE", "3": "RS485_DE_RE", "4": "RS485_DI", "5": "+5V", "6": "RS485_B",
      "7": "RS485_A", "8": "GND"})
part("R29", "Device", "R", "1k", FP_R, 132.08, 243.84, {"1": "RS485_RO", "2": "RS485_RO_3V3"})
part("R30", "Device", "R", "2k", FP_R, 132.08, 261.62, {"1": "RS485_RO_3V3", "2": "GND"})
part("J18", "Connector", "Screw_Terminal_01x02", "RS-485 link to bunker (A B)", FP_TB2, 157.48, 251.46,
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
for i, line in enumerate(["W-2750 TEST STAND - STAND BOX (Phase 1 water tests). Generated by gen_stand_box.py.",
                          "Valve power (+12V_ARMED) exists only while the bunker key + E-stop loop holds K1 closed."]):
    sch.texts.append(Text(text=line, position=Position(25.4, 20.32 + 5.08 * i, 0),
                          effects=Effects(Font(height=2.0, width=2.0), justify=Justify(horizontally="left")), uuid=uid()))
sch.to_file(OUT)
print(f"wrote {OUT}: {len(P)} parts, {len(nets_seen)} nets")
