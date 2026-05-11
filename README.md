\# PLC Automation Portfolio — Abhishek Raghunath



M.Sc. Mechatronics \& Robotics — Hochschule Schmalkalden, Germany

Focus: Industrial automation, PLC programming, Industry 4.0 integration

GitHub: github.com/Abibrdwj



\---



\## About This Repository



Structured PLC automation projects built in CODESYS V3, progressing from

basic motor control to full industrial system integration with OPC-UA and

Python dashboards.



All projects are simulation-tested and documented to industry standards.



\---



\## Projects



\### Week 1 — Motor ON/OFF Control

\- Start/stop motor control with seal-in circuit

\- Normally Closed stop button — fail-safe design

\- BOOL variables, ladder logic fundamentals

\- Simulated and tested in CODESYS Control Win V3



\### Week 2 — Conveyor Belt Simulation

\- TON timer — belt runs for set duration

\- CTU counter — counts items passing sensor

\- Auto stop after 10 items

\- Modular 4-rung logic structure



\### Week 3 — Analog Temperature Monitoring

\- REAL data type for analog sensor values

\- High and low temperature alarms

\- Comparison expressions in ladder contacts

\- Boundary condition testing



\### Week 4 — Pick and Place Robot Sequence

\- 5-step sequence using BOOL step flags

\- SET and RESET coils for state management

\- TON timer for grip hold delay

\- Full cycle simulation — pick, grip, place, release, home



\### Week 5 — Safety Circuit with E-Stop

\- Emergency stop with fault latching

\- Operator-initiated safety reset

\- SafetyOK condition preventing automatic restart

\- Fault indicator light

\- IEC 62061 / ISO 13849 safety principles applied



\---



\## Flagship Project — Smart Conveyor Monitoring System



\### Version 1 — Integrated PLC Program (Week 6)

Full integration of all weekly modules into one industrial program:

\- Motor latch with safety interlock

\- Conveyor belt with TON timer monitoring

\- Accurate item counting using R\_TRIG edge detection

\- Analog temperature monitoring with high/low alarms

\- E-Stop safety circuit with fault latch and operator reset

\- SystemReady indicator — all conditions healthy



Status: PLC layer complete — OPC-UA integration next



\---



\## Current Roadmap



\### Phase A — Foundation (Weeks 1–5) ✅ COMPLETE

Core PLC logic: motor control, timers, counters, analog, sequencing, safety



\### Phase B — Integration (Week 6 onwards) 🔄 IN PROGRESS

\- OPC-UA server setup in CODESYS

\- Python OPC-UA client

\- CSV data logging

\- Alarm architecture

\- Live dashboard



\### Phase C — Differentiation (Future)

\- Anomaly detection

\- Predictive maintenance integration

\- TIA Portal migration (Siemens S7-1200)

\- Full Smart Production Cell simulation



\---



\## Tools \& Technologies

\- CODESYS V3 — PLC simulation

\- Ladder Logic (LD) — IEC 61131-3 standard

\- Python — OPC-UA client, dashboard

\- Siemens TIA Portal — SCE training modules (S7-1200)

\- Git / GitHub — version control



\---



\## Contact

Abhishek Raghunath

M.Sc. Mechatronics \& Robotics

Hochschule Schmalkalden, Germany

