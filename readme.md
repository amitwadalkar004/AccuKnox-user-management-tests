# AccuKnox QA Trainee Assessment

## 📋 Overview
This repository contains solutions for the AccuKnox QA Trainee Practical Assessment.

**Candidate:** Amit Wadalkar  
**Date:** October 2025

---

## 📦 Project Structure

### Problem Statement 1: User Management E2E Flow
**Location:** `problem-statement-1/`

- ✅ Manual test cases for OrangeHRM User Management module
- ✅ Automated tests using Playwright with Python
- ✅ Page Object Model design pattern
- ✅ 8 automated test scenarios covering complete E2E flow

**Technologies:** Playwright 1.40.0, Python, Pytest

📄 [View Manual Test Cases](https://docs.google.com/spreadsheets/d/17S35EEyUwo6VgCOoG7RtykEjhgiQRF1F/edit?usp=sharing&ouid=107649500874813509280&rtpof=true&sd=true)  

📂 [View Code & Documentation](./problem-statement-1/)

---

### Problem Statement 2: System Monitoring & Health Checks
**Location:** `problem-statement-2/`

**Objective 1: System Health Monitoring**
- ✅ Monitors CPU, Memory, Disk, and Process metrics
- ✅ Threshold-based alerting system
- ✅ Detailed logging and reporting

**Objective 2: Application Health Checker**
- ✅ Checks application uptime using HTTP status codes
- ✅ Determines UP/DOWN status
- ✅ Continuous monitoring with statistics
- ✅ JSON report generation

**Technologies:** Python, psutil, requests

📂 [View Code & Documentation](./problem-statement-2/)

---

##  Quick Start

### Problem Statement 1
```bash
cd problem-statement-1
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
pytest tests/test_user_management.py -v