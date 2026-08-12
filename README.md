# Smart Conveyor Monitoring System — PLC + OPC UA + Python

**Abhishek Raghunath** | M.Sc. Mechatronics & Robotics | Hochschule Schmalkalden
github.com/Abibrdwj/plc-projects

Cross-platform industrial automation project using CODESYS ST, Siemens TIA Portal SCL, S7-1200, OPC UA and Python.

## What This Is

Integrated PLC station controller — motor safety interlock, rising-edge item counting with auto-rollover, dual-threshold temperature alarming, and a latched E-Stop fault circuit designed around manual-reset safety principles. Built in CODESYS V3 (Structured Text), then ported to Siemens TIA Portal (SCL), targeting a Siemens S7-1200 CPU 1214C, to prove platform-independent logic design. Phase 2 adds a live OPC UA server and Python monitoring dashboard.

**Proven:** CODESYS logic · Siemens SCL port · S7-1200 CPU configuration (PLCSIM-verified) · Python data processing · CSV logging · alarm logic · visualization
**In progress:** live OPC UA server · PLC → Python live data flow · live dashboard · alarm acknowledgment/history

**Architecture (target — see Proven/In progress above for what's live today):**

PLC logic (CODESYS ST → TIA Portal SCL)
↓
PLCSIM / S7-1200 CPU simulation
↓
OPC UA server (onboard S7-1200)
↓
Python OPC UA client (asyncua)
↓
CSV logging + alarm detection
↓
Dashboard

## System Specifications

| Parameter | Value |
|---|---|
| Networks (CODESYS baseline) | 14 |
| Variables | 22 |
| Item counter | R_TRIG + CTU_INT, auto-rollover at 9999 |
| High temp threshold | 80.0°C |
| Low temp threshold | 5.0°C |
| Safety I/O | EStopButton, StartButton, StopButton, ResetButton |
| Fault types handled | E-Stop, high temp, low temp |
| CODESYS build status | 0 errors, 0 warnings |
| TIA Portal (SCL) build status | 0 errors, 0 warnings |
| Target CPU (configured, PLCSIM-verified) | Siemens S7-1200 CPU 1214C DC/DC/DC (6ES7 214-1AG40-0XB0), firmware V4.7 |

## Engineering Decisions

**R_TRIG edge detection on item sensor**
A standard NO contact counts every scan cycle while the sensor is blocked — one physical item can register hundreds of false counts at PLC scan speed. R_TRIG fires exactly one pulse per 0→1 transition regardless of dwell time, giving accurate single-count-per-item behavior at any belt speed.

**Reset-dominant fault latch with mandatory manual reset**
A direct E-Stop interlock would allow the motor to restart automatically the instant the E-Stop is released — a safety violation. The fault latch forces a deliberate, physically separate ResetButton acknowledgment after the E-Stop condition clears, with Reset guaranteed to win under simultaneous Set/Reset. The latch/reset behavior is designed in accordance with the manual-reset principles described in IEC 62061 / ISO 13849; this is a portfolio project, not a certified safety implementation. It closes a scan-cycle-level hazard regardless: combining Reset and Start into one input removes the operator's deliberate decision point between "fault cleared" and "motor running."

**Counter rollover pinned to an explicit limit, not the type's max value**
ItemCount resets at a defined ceiling (9999) rather than silently wrapping at the INT type boundary — preventing an undetected wraparound from masquerading as a valid low count on a long-running line.

**SystemReady composite status bit**
`SystemReady = NOT FaultLatch AND NOT TempAlarmHigh AND NOT TempAlarmLow` — a single bit a SCADA/HMI layer can poll to confirm production-ready state without querying multiple internal variables.

**Explicit default values on safety-relevant outputs — as an audit discipline, not a safety mechanism**
TIA's compiler flagged four output variables without explicit defaults. Setting them is a documentation choice, not a safety fix: an unset BOOL and an explicit FALSE resolve identically, so this doesn't change first-scan risk. It exists to make the assumed startup state auditable, distinct from the real first-scan hazard (a physical E-Stop already tripped at power-on, before the output has caught up) — a separate concern this doesn't address.

## Platform Port: CODESYS ST → TIA Portal SCL

The core control logic (`FB_SmartConveyor`) was deliberately re-implemented on a second industrial platform to validate that the design travels — not just that it compiles once.

| Issue hit during the port | Resolution |
|---|---|
| First block was accidentally created as an FC | Caught before variable entry — an FC has no instance memory, which would have silently broken every `Static` variable in the design |
| R_TRIG placed under the Temp interface section | Rejected — Temp memory clears every scan, and edge detection requires persistence across scans. Moved to Static |
| TIA's counter instruction is typed by variant | Used `CTU_INT` (not generic CTU) to match `ItemCount`'s INT type |
| `CTU_INT` requires an explicit PV parameter | Wired `PV := CountResetLimit` to keep both platforms' rollover ceiling aligned |
| Reset parameter naming differs across platforms | TIA's `CTU_INT` uses `R`; CODESYS uses `RESET` |

Result: `FB_SmartConveyor` ported to SCL (block FB1), compiled clean at 0 errors / 0 warnings, committed to GitHub with interface and code-body screenshots.

## CODESYS OPC UA — Attempted, Root-Caused, Migrated

CODESYS OPC UA integration was initially attempted but abandoned after persistent `BadIdentityTokenInvalid` authentication failures — UaExpert could detect the server endpoint, but the Python client could not authenticate against it. After isolating the issue to the authentication layer, the project was migrated to Siemens' native S7-1200 OPC UA stack to reduce integration risk and align with the Siemens industrial ecosystem already in use for the TIA Portal port.

## Python Data Layer

Supporting Python modules for sensor data processing, alarm logic, and visualization — the data layer Phase 2's OPC UA client will feed live values into.

| Day | Module | Outcome |
|---|---|---|
| 1–2 | Core logic | Alarm threshold functions handling multi-condition sensor states |
| 3 | Data structures | Dictionary-based sensor state management for multi-variable logging |
| 4 | CSV file handling | Persistent sensor data logging with file append and read-back |
| 5 | NumPy + pandas | Statistical analysis pipeline on simulated temperature datasets |
| 6 | Matplotlib | Temperature trend charts with alarm-threshold overlay visualization |

**Next:** `asyncua` Python client connecting to the live S7-1200 OPC UA endpoint, replacing simulated inputs with real PLC data — currently blocked on PLCSIM export-control approval (see Current Gaps).

## Current Gaps — Actively Addressing

| Gap | Status |
|---|---|
| S7-PLCSIM V20 install | Blocked — export-control review submitted (German/EU regulated software), multi-day turnaround |
| Live OPC UA endpoint verification | Blocked behind PLCSIM — the server only exists on a running CPU instance; no compile-only equivalent |
| OPC UA variable mapping (Python ↔ PLC) | Phase 2 — scaffolding against a mock endpoint now, to be ready the moment PLCSIM is approved |
| Alarm management (code, timestamp, ACK) | Phase 2 |
| Analog wire-break / sensor-fault detection | Deferred — will use S7-1200 native analog diagnostic bits, needs IEC Timers/Counters + Analog Values modules first |

## Roadmap

**Phase A — CODESYS Foundation ✅ Complete**
14-network integrated station controller, full safety logic, 0 errors / 0 warnings.

**Phase B — TIA Portal Port ✅ Complete**
`FB_SmartConveyor` re-implemented in SCL, targeting a Siemens S7-1200 CPU 1214C, 0 errors / 0 warnings, committed.

**Phase C — OPC UA + Dashboard 🔄 In Progress**
PLCSIM approval pending → live OPC UA server → Python `asyncua` client → CSV logging + alarm detection → dashboard.

**Phase D — Differentiation 📋 Planned**
Analog wire-break/sensor-fault detection, dual-latch NEG_EDGE energy-saving extension, anomaly detection.

## Stack

CODESYS V3 (IEC 61131-3, Structured Text) · Siemens TIA Portal V20 (SCL) · S7-1200 · OPC UA · Python (pandas, NumPy, matplotlib, asyncua) · Git
