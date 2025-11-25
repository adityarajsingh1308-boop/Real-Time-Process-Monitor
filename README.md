![Python](https://img.shields.io/badge/Python-3.10-blue)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-green)
![Psutil](https://img.shields.io/badge/Psutil-5.x-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux-lightgrey)

<p align="center">
  <img src="screenshots/dashboard.png" width="700" alt="Dashboard screenshot">
</p>

# Real-Time Process Monitor

A polished, user-friendly desktop dashboard to monitor system resources and manage processes in real time.  
Built with **Python**, **psutil**, **CustomTkinter** and **Matplotlib**.

## 📑 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [How It Works](#how-it-works)
- [Future Scope](#future-scope)
- [License](#license)

---

## 🔍 Project Overview
This tool displays real-time CPU & RAM usage, shows active processes (PID, name, CPU%, RAM%) and allows process control actions (Kill, Suspend, Resume). Ideal for learning OS concepts or monitoring a development machine.

---

## ⚡ Features
- 🔴 Real-time CPU & RAM monitoring (smooth animated values)  
- 🔵 Live CPU utilization graph (historical, moving window)  
- 🧾 Process table with PID, Process Name, CPU Usage (%) and RAM Usage (%)  
- 🛑 Kill / ⏸ Suspend / ▶ Resume process controls  
- ⏱ Adjustable refresh rate slider to balance load vs. responsiveness

---

## 🧰 Tech Stack
- **Language:** Python 3.10+  
- **GUI:** CustomTkinter (modern themed Tkinter)  
- **Process info:** psutil  
- **Plotting:** Matplotlib + FigureCanvasTkAgg  
- **Extras:** numpy

---

## 🛠 Installation

### Using Python script
```bash
git clone https://github.com/adityarajsingh1308-boop/Real-Time-Process-Monitor.git
cd Real-Time-Process-Monitor
pip install -r requirements.txt
python process_monitor.py
