# AccuKnox Assessment - Problem Statement 2

## 📋 Overview
This repository contains solutions for **Problem Statement 2** of the AccuKnox QA Trainee Assessment.

**Objectives Completed:**
1. ✅ **System Health Monitoring Script** - Monitors CPU, memory, disk, and processes
2. ✅ **Application Health Checker** - Checks application uptime using HTTP status codes

---

## 📁 Project Structure

```
problem-statement-2/
├── system_health_monitor.py      # Script for system health monitoring
├── app_health_checker.py          # Script for application health checking
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── system_health_monitor.log      # Generated: System monitoring logs
├── system_health_alerts.log       # Generated: System alerts only
├── app_health_checker.log         # Generated: Application check logs
└── app_health_report.json         # Generated: JSON report
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Create project directory:**
```bash
mkdir problem-statement-2
cd problem-statement-2
```

2. **Create virtual environment (recommended):**
```bash
# On Windows
python -



cd problem-statement-2
pip install -r requirements.txt
python system_health_monitor.py
python app_health_checker.py