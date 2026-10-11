# ✈️ SkyLedger-Aero
> Enterprise-Grade Aviation MRO & AOG Operations Intelligence Platform

## 📖 Overview
**SkyLedger-Aero** is a modular operations intelligence platform built for aviation engineering, Maintenance, Repair, and Overhaul (MRO), and Aircraft-on-Ground (AOG) mitigation. It incorporates a **90/10 AI-Human-in-the-Loop (HITL)** automation framework to optimize supply chains, prevent part stockouts, and drastically reduce aircraft downtime.

---

## 🚀 Key Features & Architecture
- **FastAPI Backend:** High-performance, asynchronous REST API architecture built using Python.
- **Robust Data Seeding:** Fully seeded with **3,000 synthetic production-style records**, including:
  - **Fleet & Aircraft:** Real-time tracking of tail numbers, stations (DXB, LHR, JFK, etc.), and operational status (`AOG`, `RISK`, `OPERATIONAL`).
  - **Parts Inventory:** Categorized across critical classifications: **BFE** (Buyer Furnished Equipment), **E-class** (Engine/Expendable), **R-class** (Repairable), and **T-class** (Tools).
  - **AI HITL Queue:** Automated intelligent decision recommendations with confidence scores, cost impact calculations, and downtime savings metrics.
- **Database Engine:** SQLite backend utilizing absolute pathing for seamless cloud and container deployment.

---

## 🔌 API Endpoints
| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/v1/aog/active` | `GET` | Fetches all currently grounded aircraft (AOG status). |
| `/api/v1/inventory/` | `GET` | Filterable inventory search by part class and station. |
| `/api/v1/hitl/queue` | `GET` | Retrieves pending AI-driven operational recommendation queue. |
| `/api/v1/docs` | `GET` | Interactive Swagger UI documentation. |

---

## 🛠️ Quick Start Guide
1. Clone the repository:
   ```bash
   git clone [https://github.com/syed-amjad65/SkyLedger-Aero.git](https://github.com/syed-amjad65/SkyLedger-Aero.git)
