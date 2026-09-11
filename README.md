# Abhishek Raghunath — Automation & Controls Portfolio

M.Sc. Mechatronics & Robotics, Hochschule Schmalkalden
Industrial automation systems: PLC control, safety logic, and Python-based
industrial monitoring — built and verified in simulation (CODESYS, TIA
Portal/PLCSIM), no physical hardware.

## Featured Project

**[Smart Production Cell](projects/smart-production-cell/)** — safety-critical
conveyor control logic implemented on two PLC platforms (CODESYS ST, Siemens
TIA Portal SCL), verified end-to-end on PLCSIM, paired with a Python
monitoring pipeline (data generation, logging, alarms, dashboarding). Includes
a root-caused architectural finding on why live OPC-UA isn't possible on the
current TIA/PLCSIM toolchain — a licensing/hardware-tier restriction, not a
design gap.

## Repository Structure

```

plc-projects/
├── projects/
│   └── smart-production-cell/   Flagship project — see its README for full detail
└── learning/
    ├── plc/                     CODESYS exercises: motor control, timers/counters,
    │                            analog sensors, sequencing, safety circuits, function blocks
    ├── python/                  Python fundamentals through file handling, NumPy/Pandas,
    │                            Matplotlib, and timestamps
    └── siemens-sce/             Reference notes (see folder for official Siemens SCE links)

```

## Stack

CODESYS V3 (Structured Text) · Siemens TIA Portal (SCL) · S7-1200 / PLCSIM ·
Python (pandas, NumPy, matplotlib) · Git