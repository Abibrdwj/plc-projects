# Smart Conveyor Monitoring System — CODESYS Ladder Logic

**Abhishek Raghunath** | M.Sc. Mechatronics & Robotics | Hochschule Schmalkalden  
[github.com/Abibrdwj/plc-projects](http://github.com/Abibrdwj/plc-projects)

---

## What This Is

Integrated PLC station controller built in CODESYS V3: motor safety interlock, rising-edge item counting with configurable batch limit, dual-threshold temperature alarming, and IEC 62061-aligned latched E-Stop fault circuit. Phase 2 adds OPC-UA server export and Python live dashboard.

---

## System Specifications

| Parameter | Value |
|---|---|
| Networks | 14 |
| Variables | 22 |
| Belt run timer (TON preset) | 30 seconds |
| Batch limit | 10 items (configurable PV) |
| High temp threshold | 80.0°C |
| Low temp threshold | 20.0°C |
| Safety variables | 5 (EStop, FaultLatch, SafetyOk, ResetBtn, FaultLight) |
| Fault types handled | E-Stop, high temp, low temp, batch complete |
| Build status | 0 errors, 0 warnings |
| Stop button default | NC — fail-safe by design |
| E-Stop default | NC — fail-safe by design |

---

## Engineering Decisions

**R_TRIG edge detection on item sensor**  
Standard NO contact counts every scan cycle while sensor is blocked — one item triggers hundreds of false counts at speed. R_TRIG fires one pulse per 0→1 transition regardless of dwell time. Correct industrial counting pattern.

**Latched fault circuit with mandatory manual reset**  
Direct E-Stop interlock allows immediate motor restart on release — a machine safety violation. Fault latch forces deliberate ResetBtn acknowledgment after E-Stop clears. Follows IEC 62061 / ISO 13849 manual reset requirement for safety functions.

**SafetyOk as centralized permissive signal**  
All safety conditions feed into a single SafetyOk rung. Adding a light curtain or door switch requires one change in one place — motor control logic stays untouched. Scalable architecture for multi-interlock stations.

**SystemReady composite status bit**  
SystemReady = SafetyOk AND NOT FaultLatch AND NOT AlarmLight. Single bit readable by SCADA or HMI to confirm production-ready state without polling multiple variables.

**NC stop button**  
Wire break = stop signal. Fail-safe by design. Standard on every industrial stop circuit.

---

## Key Outcomes

- Designed 14-network station controller integrating motor control, item counting, temperature monitoring, and safety interlock into a single cohesive PLC program
- Implemented IEC 62061-aligned E-Stop fault latching eliminating automatic restart after safety circuit activation
- Applied R_TRIG edge detection ensuring single-count-per-item accuracy regardless of sensor dwell time
- Architected modular SafetyOk permissive enabling future interlock expansion without modifying motor logic
- Structured composite SystemReady status bit for direct SCADA/HMI integration
- Fixed C0196 type mismatch — CurrentCount corrected from WORD to INT to match CTU.CV output type

---

## Python Automation — Industrial Data Layer

Supporting Python scripts for sensor data processing, alarm logic, and visualization — built as the data layer for Phase 2 OPC-UA dashboard integration.

| Day | Module | Outcome |
|---|---|---|
| 1–2 | Core logic | Alarm threshold functions handling multi-condition sensor states |
| 3 | Data structures | Dictionary-based sensor state management for multi-variable logging |
| 4 | CSV file handling | Persistent sensor data logging with file append and read-back |
| 5 | NumPy + Pandas | Statistical analysis pipeline on simulated temperature datasets |
| 6 | Matplotlib | Temperature trend charts with alarm threshold overlay visualization |

**Next:** OPC-UA client connecting to CODESYS server — live sensor data replacing simulated inputs.

---

## Current Gaps — Actively Addressing

| Gap | Status |
|---|---|
| Function Block encapsulation | Next priority — Motor FB in progress |
| OPC-UA variable mapping | Phase 2 — in development |
| Alarm management (code, timestamp, ACK) | Phase 2 |
| State machine (Idle/Running/Fault/Done) | Planned |

---

## Roadmap

**Phase A — Foundation** ✅ Complete  
14-network integrated station controller with full safety logic, 0 errors 0 warnings

**Phase B — Integration** 🔄 In Progress  
OPC-UA server in CODESYS → Python OPC-UA client → CSV logging → live dashboard

**Phase C — Differentiation** 📋 Planned  
Anomaly detection, predictive maintenance, TIA Portal migration

---

## Weekly Build Log

| Week | Module | Status |
|---|---|---|
| 1 | Motor ON/OFF with seal-in circuit | ✅ |
| 2 | Conveyor belt — TON timer + CTU counter | ✅ |
| 3 | Analog temperature monitoring | ✅ |
| 4 | Pick and Place sequence — 5-step BOOL state | ✅ |
| 5 | Safety circuit — E-Stop + fault latch | ✅ |
| 6 | Smart Conveyor v1 — full integration, 0 errors 0 warnings | ✅ |
| 7+ | OPC-UA + Python Smart Cell | 🔄 |

---

## Stack

CODESYS V3 · Ladder Logic IEC 61131-3 · Python · OPC-UA · Git