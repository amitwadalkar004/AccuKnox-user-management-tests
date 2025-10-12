
import random
import string

class TestData:
    BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    USERNAME = "Admin"
    PASSWORD = "admin123"
    
    @staticmethod
    def generate_random_username():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"TestUser_{random_string}"
    
    @staticmethod
    def generate_random_password():
        return "Test@123456"
    
    # Test user data
    TEST_USER = {
        "user_role": "ESS",
        "employee_name": "a",  # Type 'a' to get suggestions
        "status": "Enabled",
        "username": "",  # Will be generated dynamically
        "password": "Test@123456"
    }
    
    EDITED_USER = {
        "user_role": "Admin",
        "status": "Enabled"
    }
