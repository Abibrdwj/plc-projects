# Smart Production Cell — PLC + OPC-UA + Python Integration

**Abhishek Raghunath** | M.Sc. Mechatronics & Robotics, Hochschule Schmalkalden
github.com/Abibrdwj/plc-projects

Cross-platform industrial automation build: safety-critical PLC logic implemented
on two platforms (CODESYS ST, Siemens TIA Portal SCL), paired with a Python
monitoring pipeline built to the same shape a live OPC-UA feed would need.
Simulation-based — PLCSIM V20 and CODESYS simulation, no physical hardware.

## Repository Map

```
smart-production-cell/
├── codesys/                  Canonical CODESYS ST implementation (FB_SmartConveyor)
│   ├── ladder-v1-superseded/ Earlier Ladder Diagram attempt — kept to show iteration
│   └── opcua-attempt/        CODESYS OPC-UA client scripts (asyncua)
├── tia-portal/                TIA Portal SCL port, S7-1200, PLCSIM-verified
└── python-monitoring/         Mock-data monitoring pipeline
    └── fixtures/              Known-answer test fixtures for dashboard/summary verification
```

## What This Is

An integrated station controller — motor safety interlock, edge-triggered item
counting with rollover protection, dual-threshold temperature alarming, and a
manual-reset E-Stop fault latch — built first in CODESYS (Structured Text), then
independently re-implemented in Siemens TIA Portal (SCL) targeting an S7-1200,
to prove the logic design travels across platforms rather than being tied to
one toolchain.

An earlier CODESYS Ladder Diagram attempt (`codesys/ladder-v1-superseded/`) is
kept in the repo rather than deleted — it documents the actual iteration path:
ladder prototype → proper function-block design in Structured Text → ported to
TIA/SCL.

On the monitoring side: a Python pipeline (data generation, persistent CSV
logging, a timed polling loop, a dashboard, and a summary analytics panel)
built to the exact interface shape a real OPC-UA feed will plug into — the
mock-data layer is the one thing standing between this and a live system, and
why it's still mock is a specific, root-caused finding, not an unfinished corner.

## Status at a Glance

| Layer | State |
|---|---|
| CODESYS ST — FB_SmartConveyor | Complete, simulation-tested, 0 errors / 0 warnings |
| TIA Portal SCL — ported FB1 | Complete, PLCSIM-verified end-to-end (safety-latch sequence, counter rollover, dual-threshold temp alarms), 0 errors / 0 warnings — two real bugs found and fixed during verification |
| Python monitoring pipeline | Complete on mock data — generation, logging, polling, dashboard, alarm summary |
| OPC-UA (CODESYS) | Attempted, blocked on unresolved auth error (`BadIdentityTokenInvalid`) — pivoted to TIA. Root-cause + live rebuild planned as Stage 2. |
| OPC-UA (TIA) | Blocked — root-caused, documented (see below). Not an open task. |

## Live PLCSIM Verification (17–28 Aug)

Full `FB_SmartConveyor` logic verified end-to-end on S7-PLCSIM V20, standard
tier, via forced watch-table inputs and single-scan stepping.

**Safety-latch sequence.** E-Stop tripped → `FaultActive` latches TRUE →
E-Stop released → `FaultActive` remains TRUE (confirms release alone does not
clear the fault) → `ResetButton` forced → `FaultActive` clears → `StartButton`
forced → `Motor_Run` goes TRUE. Full sequence matches hand-traced logic exactly.

**Counter rollover.** `ItemCounter` (CTU_INT) tested at `CountResetLimit = 5`
via single-scan stepping. Confirmed IEC 61131-3 reset-dominant behavior: CV
reaches the limit value, the next CU pulse is silently dropped in the same
scan the reset fires (not miscounted), CV then resets to 0.

**Temperature alarm boundary tests.** `TempAlarmHigh` and `TempAlarmLow`
verified independently at threshold-crossing values (85.0°C / 3.0°C against
80.0/5.0°C limits).

**Two real bugs found and fixed during this pass:**

- `FaultActive` self-assignment — originally `#FaultActive := #FaultActive`,
  never actually read `#FaultLatch`. Compiled clean at 0 errors/0 warnings
  despite never reporting real fault state.
- Missing `PartTrig` call — `R_TRIG` instance declared but never invoked in
  the code body, so `ItemCount` stayed stuck at 0 regardless of sensor
  activity. Also compiled clean. Root-caused via live CV-vs-ItemCount
  mismatch on PLCSIM, not from a compile error.

Both are documented as a general finding: **a 0-errors/0-warnings compile
confirms syntactic correctness, not completeness of design intent** — a
declared-but-uncalled instance is invisible to the compiler.

## OPC-UA: Attempted, Root-Caused, Deferred

Live OPC-UA is not running on either platform yet — but it wasn't for lack of
trying, and both dead ends are documented rather than glossed over.

**First attempt — CODESYS.** An OPC-UA server was brought up on CODESYS and
was visible to UaExpert, but the Python client repeatedly failed to
authenticate against it with `BadIdentityTokenInvalid`. The specific cause
(security policy mismatch, token type, or certificate trust) wasn't isolated
at the time — rather than sink further time into an undiagnosed auth failure
with no clear next debugging step, the project pivoted to Siemens' native
S7-1200 OPC-UA stack, which also matched the TIA port already underway.
Scripts from this attempt: `codesys/opcua-attempt/`.

**Second attempt — TIA / S7-1200.** Root-caused by direct testing, not
assumed from documentation:

> S7-PLCSIM V20 Standard does not support OPC-UA server functionality under
> any configuration. OPC-UA requires PLCSIM Advanced, a separate and
> higher-tier license not held for this project — and even under Advanced,
> OPC-UA server support is limited to S7-1500 CPUs; the S7-1200 CPU 1214C
> used here is excluded from that capability at any license tier.

So the TIA path is blocked by a licensing/hardware tier, not a design gap or
a repeat of the CODESYS auth problem. Stage 2 returns to CODESYS to actually
isolate and fix the `BadIdentityTokenInvalid` cause — rather than route
around it a second time — once the current mock-data Python pipeline
(Stage 1) is complete. Two independent blockers, two independent root causes
to chase down, one clear next step.

## Engineering Decisions

**R_TRIG edge detection on the item sensor.** A plain NO contact counts every
scan cycle while blocked — one item would register hundreds of false counts
at PLC scan speed. R_TRIG fires exactly one pulse per 0→1 transition,
independent of dwell time.

**Reset-dominant fault latch, mandatory manual reset.** A direct E-Stop
interlock lets the motor restart the instant E-Stop is released — a safety
violation. The latch requires a physically separate `ResetButton`
acknowledgment, with reset guaranteed to win on a simultaneous set/reset.
Designed around the manual-reset principles in IEC 62061 / ISO 13849
(portfolio project, not a certified safety implementation) — but it closes a
real scan-cycle hazard regardless: combining Reset and Start into one input
removes the operator's deliberate decision point between "fault cleared" and
"motor running."

**Counter rollover pinned to an explicit ceiling, not the type's max value.**
`ItemCount` resets at a defined limit (9999) rather than silently wrapping at
the INT boundary, so a long-running line can't wrap around undetected into a
plausible-looking low count.

**SystemReady composite status bit.** `SystemReady = NOT FaultLatch AND NOT
TempAlarmHigh AND NOT TempAlarmLow` — one bit a SCADA/HMI layer can poll
instead of querying multiple internal variables.

**Temperature alarms — advisory, not a motor interlock (open design
question).** `TempAlarmHigh`/`TempAlarmLow` feed the `SystemReady` composite
status bit for a supervisory (SCADA/HMI) layer, but nothing currently routes
them into `Motor_Run`'s stop condition. Found via live PLCSIM testing (28
Aug) — not a scrapped test, a design-boundary finding. Whether this is
correct depends on what the sensor measures: advisory-only fits
product/ambient monitoring (an immediate trip could itself cause harm, e.g.
abrupt mid-cycle stop); a hard interlock fits motor thermal protection. This
system's sensor role hasn't been pinned down, so the interlock question is an
open, documented extension point rather than a closed decision. If motor
thermal protection is required, the extension is mechanical: route
`TempAlarmHigh` into the same reset-dominant OR condition currently guarding
`FaultLatch`, so a temp trip requires the same deliberate `ResetButton`
acknowledgment as an E-Stop trip, rather than auto-clearing when temperature
drops back under threshold.

## Deferred Scope

**Sensor wire-break / fault detection — deferred, not attempted.** Requires
S7-1200 native analog diagnostic bits, which depend on the Analog Values
module (not yet completed) as a prerequisite. Scoped for a later hardening
pass once the OPC-UA/dashboard chain is live.

## Platform Port: CODESYS ST → TIA Portal SCL

Re-implemented on a second platform to prove the design travels, not just
that it compiles once.

| Issue hit during the port | Resolution |
|---|---|
| TIA's counter instruction is typed by variant | Used `CTU_INT` (not generic CTU) to match `ItemCount`'s INT type |
| `CTU_INT` requires an explicit PV parameter | Wired `PV := CountResetLimit` to keep both platforms' rollover ceiling aligned |
| Reset parameter naming differs across platforms | TIA's `CTU_INT` uses `R`; CODESYS uses `RESET` |
| `R_TRIG` instance placed in Temp instead of Static | Temp clears every scan; edge detection needs persistence — moved to Static |
| `PartTrig` (R_TRIG) declared but never called | `ItemCount` stuck at 0 despite a clean compile — found via logic review against the CODESYS baseline, fixed |
| `FaultActive` self-assigned instead of reading `FaultLatch` | Silently never reported fault state despite 0 errors/0 warnings — found and fixed during review |

Full station compiles clean, downloaded to a simulated S7-1200 CPU 1214C
(firmware V4.7) on PLCSIM V20. Full end-to-end safety-latch sequence verified
live: forced E-Stop → `FaultActive` correctly latched TRUE → forced Reset →
correctly cleared → forced Start → `Motor_Run` correctly triggered. Matches
hand-traced logic exactly.

## Python Monitoring Pipeline

| Component | What it does |
|---|---|
| `next_reading()` | Mock sensor data generator |
| `log_reading()` | CSV logger with real timestamping |
| `run_pipeline()` | Timed polling loop (`time.sleep()`-paced) tying generation and logging together |
| Dashboard | Matplotlib temperature trend vs. real timestamp, with HIGH/LOW sustained-alarm markers overlaid |
| Summary panel | Alarm counts, longest alarm streaks, uptime % — returned as a structured result |

Dashboard and summary panel are both verified against known-answer test
fixtures in `python-monitoring/fixtures/` (clean logs and hand-built
alarm-crossing fixtures), not just eyeballed.

Why mock data, by design: the pipeline is built to the interface shape a real
OPC-UA read will drop into — `next_reading()` is the single seam that gets
replaced. Nothing downstream (logging, dashboard, alarms) changes when that
happens.

## Roadmap

- **Phase A — CODESYS Foundation** ✅ Complete. Full safety logic, 0 errors/0 warnings.
- **Phase B — TIA Portal Port** ✅ Complete. PLCSIM-verified, 0 errors/0 warnings.
- **Phase C — Python Monitoring Pipeline (mock data)** ✅ Complete. Generation → logging → polling → dashboard → alarm summary.
- **Phase D — CODESYS-Live OPC-UA (retry)** 📋 Planned, not yet successful. First pass hit an unresolved `BadIdentityTokenInvalid` auth error on the `asyncua` client and was shelved in favor of the TIA path; this phase returns to actually root-cause it and get a live read/subscribe working. Adds a second PLC ecosystem (CODESYS-family: WAGO, Beckhoff/TwinCAT) to the toolchain shown here.
- **Phase E — Multi-Machine Handling** 📋 Planned. Extend the pipeline from single-source to multiple simulated machines/sensors feeding the same logging and alarm layer — not yet started.
- **Phase F — Reliability Hardening** 📋 Planned. Reconnect-on-disconnect, malformed-read handling, locked-file handling — the gap between "a script" and "a monitoring system."

## Stack

CODESYS V3 (IEC 61131-3, Structured Text) · Siemens TIA Portal V20 (SCL) ·
S7-1200 CPU 1214C · PLCSIM V20 · Python (pandas, NumPy, matplotlib) · Git

`asyncua` (first-pass client attempted against CODESYS, connection not yet
live — Phase D retries this)
