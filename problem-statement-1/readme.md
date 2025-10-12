# AccuKnox User Management Tests

##  Project Overview
This project contains automated test cases for the OrangeHRM User Management module using Playwright with Python and Page Object Model (POM) design pattern.

##  Test Coverage
The automation covers the following scenarios:
1. Login to OrangeHRM application
2. Navigate to Admin Module
3. Add a new user
4. Search for the created user
5. Edit user details (User Role, Status)
6. Validate updated details
7. Delete the user
8. Verify user deletion

## 🛠️ Technologies Used
- **Playwright**: v1.40.0
- **Python**: 3.8+
- **Pytest**: v7.4.3
- **Design Pattern**: Page Object Model (POM)

##  Project Structure
```
AccuKnox-user-management-tests/
problem-statement-1
├── pages/
│   ├── __init__.py
│   ├── base_page.py              # Base page with common methods
│   ├── login_page.py              # Login page object
│   ├── dashboard_page.py          # Dashboard page object
│   └── user_management_page.py    # User management page object
├── tests/
│   ├── __init__.py
│   └── test_user_management.py    # All test cases
├── utils/
│   ├── __init__.py
│   └── test_data.py               # Test data and configuration
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Project dependencies
└── README.md                      # This file
```

##  Setup Instructions

### Prerequisites
- Python 3.8 or higher installed
- pip package manager
- Git installed

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/amitwadalkar004/AccuKnox-user-management-tests.git
   cd AccuKnox-user-management-tests
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

##  Running Tests

### Run All Tests
```bash
cd problem-statement-1
pytest tests/test_user_management.py -v
```

### Run Specific Test
```bash
cd problem-statement-1
pytest tests/test_user_management.py::TestUserManagement::test_03_add_new_user -v
```

### Run Tests in Headless Mode
```bash
cd problem-statement-1
pytest tests/test_user_management.py --headed=false
```

### Run Tests with HTML Report
```bash
cd problem-statement-1
pytest tests/test_user_management.py --html=report.html --self-contained-html
```

### Run Tests with Different Browser
```bash
cd problem-statement-1
# Chrome (default)
pytest tests/test_user_management.py --browser chromium