
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.user_management_page import UserManagementPage
from utils.test_data import TestData



# Global variable to store username across tests
created_username = None

@pytest.fixture(scope="function")
def setup(page: Page):
    # Navigate to application
    page.goto(TestData.BASE_URL)
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    # Login
    login_page = LoginPage(page)
    login_page.login(TestData.USERNAME, TestData.PASSWORD)
    
    # Navigate to Admin module
    dashboard_page = DashboardPage(page)
    dashboard_page.navigate_to_admin()
    return page

class TestUserManagement:
    
    def test_01_login_to_application(self, page: Page):
        '''Test Case 1: Verify successful login'''
        page.goto(TestData.BASE_URL)
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        login_page = LoginPage(page)
        login_page.login(TestData.USERNAME, TestData.PASSWORD)
        login_page.verify_login_successful()
        
        print("✓ Login successful")
    
    def test_02_navigate_to_admin_module(self, page: Page):
        '''Test Case 2: Verify navigation to Admin module'''
        page.goto(TestData.BASE_URL)
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        login_page = LoginPage(page)
        login_page.login(TestData.USERNAME, TestData.PASSWORD)
        
        dashboard_page = DashboardPage(page)
        dashboard_page.navigate_to_admin()
        dashboard_page.verify_admin_page_loaded()
        
        print("✓ Navigated to Admin module")
    
    def test_03_add_new_user(self, setup):
        '''Test Case 3: Add a new user'''
        global created_username
        
        page = setup
        user_management_page = UserManagementPage(page)
        
        # Generate unique username
        created_username = TestData.generate_random_username()
        test_user = TestData.TEST_USER.copy()
        test_user['username'] = created_username
        
        # Add new user
        user_management_page.add_new_user(test_user)
        
        # Verify success message
        user_management_page.verify_success_message()
        
        print(f"✓ User created successfully: {created_username}")
    
    def test_04_search_created_user(self, setup):
        '''Test Case 4: Search for the newly created user'''
        global created_username
        
        page = setup
        user_management_page = UserManagementPage(page)
        
        # Use username from previous test or create new one
        if created_username is None:
            created_username = TestData.generate_random_username()
            test_user = TestData.TEST_USER.copy()
            test_user['username'] = created_username
            user_management_page.add_new_user(test_user)
        
        # Search for user
        user_management_page.search_user(created_username)
        
        # Verify user exists in search results
        user_data = user_management_page.verify_user_exists(created_username)
        assert user_data['username'] == created_username
        
        print(f"✓ User found in search: {created_username}")
    
    def test_05_edit_user_details(self, setup):
        '''Test Case 5: Edit user details'''
        global created_username
        
        page = setup
        user_management_page = UserManagementPage(page)
        
        # Ensure user exists
        if created_username is None:
            created_username = TestData.generate_random_username()
            test_user = TestData.TEST_USER.copy()
            test_user['username'] = created_username
            user_management_page.add_new_user(test_user)
        
        # Search for user
        user_management_page.search_user(created_username)
        
        # Click edit
        user_management_page.click_edit_user(created_username)
        
        # Update user details
        user_management_page.update_user(
            user_role=TestData.EDITED_USER['user_role'],
            status=TestData.EDITED_USER['status']
        )
        
        # Verify success message
        user_management_page.verify_success_message()
        
        print(f"✓ User updated successfully: {created_username}")
    
    def test_06_validate_updated_details(self, setup):
        '''Test Case 6: Validate updated user details'''
        global created_username
        
        page = setup
        user_management_page = UserManagementPage(page)
        
        # Search for user
        user_management_page.search_user(created_username)
        
        # Get user data and verify
        user_data = user_management_page.verify_user_exists(created_username)
        assert user_data['user_role'] == TestData.EDITED_USER['user_role']
        assert user_data['status'] == TestData.EDITED_USER['status']
        
        print(f"✓ User details validated: Role={user_data['user_role']}, Status={user_data['status']}")
    
    def test_07_delete_user(self, setup):
        '''Test Case 7: Delete user'''
        global created_username
        
        page = setup
        user_management_page = UserManagementPage(page)
        
        # Search for user
        user_management_page.search_user(created_username)
        
        # Click delete
        user_management_page.click_delete_user(created_username)
        
        # Confirm delete
        user_management_page.confirm_delete()
        
        # Verify success message
        user_management_page.verify_success_message()
        
        print(f"✓ User deleted successfully: {created_username}")
    
    def test_08_verify_user_deleted(self, setup):
        '''Test Case 8: Verify user is removed after deletion'''
        global created_username
        
        page = setup
        user_management_page = UserManagementPage(page)
        
        # Search for deleted user
        user_management_page.search_user(created_username)
        
        # Verify user does not exist
        user_management_page.verify_user_not_exists(created_username)
        
        print(f"✓ Verified user is deleted: {created_username}")
        
        # Reset for cleanup
        created_username = None
