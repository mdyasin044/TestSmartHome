# 🏠 Smart Home IoT Attack Simulation
### Eclipse Ditto · MITRE ATT&CK Framework · Docker

A cybersecurity research project that simulates real-world IoT attacks on a smart home environment using **Eclipse Ditto** as the IoT digital twin platform. The project models four smart home devices and executes attack simulations based on the **MITRE ATT&CK framework**, collecting before/after logs for analysis.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Devices](#devices)
- [Attack Simulations](#attack-simulations)
- [Output](#output)
- [MITRE ATT&CK Coverage](#mitre-attck-coverage)

---

## Overview

This project simulates how an attacker could manipulate IoT devices in a smart home through an unsecured or compromised API. It uses **Eclipse Ditto** — an open-source IoT digital twin framework — to model smart devices and interact with them via REST API.

The simulation:
1. Creates four smart home devices as digital twins in Eclipse Ditto
2. Saves the **baseline (normal) state** of each device
3. Executes **attack simulations** against each device
4. Saves the **compromised state** after each attack
5. Generates a **comparison report** showing exactly what changed
6. Collects **Docker container logs** throughout the entire process

> ⚠️ This project is intended for **academic and research purposes only**. All attacks run against a local Docker instance and do not affect any real devices or networks.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              Smart Home Network              │
│                                              │
│   ┌─────────┐  ┌──────┐  ┌───────┐          │
│   │  Bulb   │  │  AC  │  │ Alexa │          │
│   └────┬────┘  └──┬───┘  └───┬───┘          │
│        │          │          │               │
│   ┌────┴──────────┴──────────┴────┐          │
│   │           Router              │          │
│   └───────────────┬───────────────┘          │
└───────────────────┼─────────────────────────-┘
                    │
         ┌──────────▼──────────┐
         │    Eclipse Ditto    │
         │   (Digital Twin)    │
         │   localhost:8080    │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │   Attack Scripts    │
         │  (Python / REST)    │
         └─────────────────────┘
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Eclipse Ditto](https://github.com/eclipse-ditto/ditto) running via Docker Compose
- Python 3.8+
- pip package: `requests`

### Install Python dependency
```bash
pip install requests
```

### Start Eclipse Ditto
```bash
cd path/to/ditto/deployment/docker
docker compose up -d
```

Verify Ditto is running at: `http://localhost:8080`

---

## Project Structure

```
SmartHome/
│
├── main.py                  # Master script — runs everything
├── cleanup.py               # Deletes all things and policies
├── create_devices.py        # Creates all 4 smart home devices
│
├── attack_bulb.py           # Attack simulations for Smart Bulb
├── attack_ac.py             # Attack simulations for Smart AC
├── attack_alexa.py          # Attack simulations for Alexa
├── attack_router.py         # Attack simulations for Router
│
├── compare_attacks.py       # Compares baseline vs attacked states
│
└── README.md
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/smarthome-iot-attack-simulation.git
cd smarthome-iot-attack-simulation
```

### 2. Install dependencies
```bash
pip install requests
```

### 3. Make sure Eclipse Ditto is running
```bash
docker ps --format "{{.Names}}"
```

You should see containers like:
```
docker-nginx-1
docker-gateway-1
docker-things-1
docker-policies-1
docker-connectivity-1
docker-mongodb-1
docker-ditto-ui-1
```

### 4. Update the Docker Compose path in `main.py`
Open `main.py` and update this line to match your Ditto installation path:
```python
COMPOSE_DIR = r"D:\your\path\to\ditto\deployment\docker"
```

---

## Usage

### Option A — Run everything at once (recommended)
```bash
python main.py
```

This automatically:
- Cleans up any existing devices
- Creates all 4 devices
- Runs all attack simulations
- Compares baseline vs attacked states
- Collects Docker logs at every stage

---

### Option B — Run scripts individually

#### Step 1: Clean up existing devices
```bash
python cleanup.py
```

#### Step 2: Create all devices
```bash
python create_devices.py
```

#### Step 3: Run attack simulations
```bash
python attack_bulb.py
python attack_ac.py
python attack_alexa.py
python attack_router.py
```

#### Step 4: Compare results
```bash
python compare_attacks.py bulb_baseline_TIMESTAMP bulb_attacks_TIMESTAMP
python compare_attacks.py ac_baseline_TIMESTAMP ac_attacks_TIMESTAMP
python compare_attacks.py alexa_baseline_TIMESTAMP alexa_attacks_TIMESTAMP
python compare_attacks.py router_baseline_TIMESTAMP router_attacks_TIMESTAMP
```

---

## Devices

| Device | Thing ID | Features |
|---|---|---|
| Smart Bulb | `smarthome:bulb01` | power, brightness, color, temperature |
| Smart AC | `smarthome:ac01` | power, temperature, mode, fan, timer, status |
| Alexa Echo Dot | `smarthome:alexa01` | power, audio, voice_assistant, smart_home_control, network, status |
| Home Router | `smarthome:router01` | network, wifi, connected_devices, firewall, traffic, status |

---

## Attack Simulations

### 🔦 Bulb Attacks (`attack_bulb.py`)

| # | MITRE ID | Attack | Action |
|---|---|---|---|
| 1 | T1565 | Data Manipulation | Force ON, max brightness, red color |
| 2 | T1499 | Denial of Service | Rapid power flipping 20 times |
| 3 | T1557 | Sensor Spoofing | Inject fake 999.9°C temperature |
| 4 | T1071 | Command & Control | Blackout — turn off, set color black |
| 5 | T1496 | Resource Hijacking | Strobe effect — rapid brightness flipping |

### ❄️ AC Attacks (`attack_ac.py`)

| # | MITRE ID | Attack | Action |
|---|---|---|---|
| 1 | T1565 | Data Manipulation | Force heat mode at max temperature |
| 2 | T1499 | Denial of Service | Rapid power and mode cycling |
| 3 | T1557 | Sensor Spoofing | Inject fake -10°C reading and error code |
| 4 | T1071 | Command & Control | Max heat, max fan, disable timer |
| 5 | T1485 | Data Destruction | Corrupt min/max temperature limits |

### 🔊 Alexa Attacks (`attack_alexa.py`)

| # | MITRE ID | Attack | Action |
|---|---|---|---|
| 1 | T1565 | Data Manipulation | Inject fake unlock door command |
| 2 | T1499 | Denial of Service | Spam volume and mute toggling |
| 3 | T1557 | Man in the Middle | Spoof network details and disconnect |
| 4 | T1071 | Command & Control | Hijack connected devices and wake word |
| 5 | T1489 | Service Stop | Shut down, enable do-not-disturb |

### 📡 Router Attacks (`attack_router.py`)

| # | MITRE ID | Attack | Action |
|---|---|---|---|
| 1 | T1565 | Data Manipulation | Change DNS to malicious servers |
| 2 | T1499 | Denial of Service | Flood bandwidth usage to 100% |
| 3 | T1557 | Man in the Middle | Disable firewall and encryption |
| 4 | T1071 | Command & Control | Block legitimate devices, hijack network |
| 5 | T1489 | Service Stop | Disable WiFi, take router offline |

---

## Output

After running `main.py` you will get the following output folders:

```
SmartHome/
│
├── bulb_baseline_TIMESTAMP/        # Normal bulb state
├── bulb_attacks_TIMESTAMP/         # Bulb states after each attack
│
├── ac_baseline_TIMESTAMP/          # Normal AC state
├── ac_attacks_TIMESTAMP/           # AC states after each attack
│
├── alexa_baseline_TIMESTAMP/       # Normal Alexa state
├── alexa_attacks_TIMESTAMP/        # Alexa states after each attack
│
├── router_baseline_TIMESTAMP/      # Normal router state
├── router_attacks_TIMESTAMP/       # Router states after each attack
│
└── docker_logs_TIMESTAMP/          # Docker container logs
    ├── 01_before_setup_ALL.txt
    ├── 02_after_device_creation_ALL.txt
    ├── 03_after_bulb_attacks_ALL.txt
    ├── 04_after_ac_attacks_ALL.txt
    ├── 05_after_alexa_attacks_ALL.txt
    ├── 06_after_router_attacks_ALL.txt
    └── 07_final_ALL.txt
```

### Sample Compare Report Output
```
===== ATTACK COMPARISON REPORT =====

Attack : T1565_data_manipulation.json
  CHANGED  power.is_on:       False → True
  CHANGED  brightness.level:  100   → 255
  CHANGED  color.rgb:         255,255,255 → 255,0,0

Attack : T1557_sensor_spoofing.json
  CHANGED  temperature.celsius: 25.0 → 999.9

Attack : T1071_command_and_control.json
  CHANGED  color.rgb:    255,255,255 → 0,0,0
  CHANGED  power.is_on:  False → False
```

---

## MITRE ATT&CK Coverage

| Technique ID | Name | Devices Targeted |
|---|---|---|
| T1565 | Data Manipulation | Bulb, AC, Alexa, Router |
| T1499 | Endpoint Denial of Service | Bulb, AC, Alexa, Router |
| T1557 | Man-in-the-Middle | Bulb, AC, Alexa, Router |
| T1071 | Application Layer Protocol (C2) | Bulb, AC, Alexa, Router |
| T1496 | Resource Hijacking | Bulb |
| T1485 | Data Destruction | AC |
| T1489 | Service Stop | Alexa, Router |

---

## ⚠️ Disclaimer

This project is developed strictly for **academic research and educational purposes**. All simulations run against a **local Docker environment** only. Do not run these scripts against any real devices, production systems, or networks you do not own. The authors are not responsible for any misuse of this project.

---

## 📄 License

MIT License — feel free to use and modify for research purposes.
