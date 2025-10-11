
from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import time

class UserManagementPage(BasePage):
    # Locators
    ADD_BUTTON = "button:has-text('Add')"
    USER_ROLE_DROPDOWN = "//label[text()='User Role']/parent::div/following-sibling::div//div[@class='oxd-select-text-input']"
    EMPLOYEE_NAME_INPUT = "//label[text()='Employee Name']/parent::div/following-sibling::div//input"
    STATUS_DROPDOWN = "//label[text()='Status']/parent::div/following-sibling::div//div[@class='oxd-select-text-input']"
    USERNAME_INPUT = "//label[text()='Username']/parent::div/following-sibling::div//input"
    PASSWORD_INPUT = "//label[text()='Password']/parent::div/following-sibling::div//input"
    CONFIRM_PASSWORD_INPUT = "//label[text()='Confirm Password']/parent::div/following-sibling::div//input"
    SAVE_BUTTON = "button[type='submit']:has-text('Save')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    
    # Search locators
    SEARCH_USERNAME_INPUT = "//label[text()='Username']/parent::div/following-sibling::div//input"
    SEARCH_BUTTON = "button[type='submit']:has-text('Search')"
    RESET_BUTTON = "button:has-text('Reset')"
    
    # Table locators
    TABLE_ROWS = ".oxd-table-body .oxd-table-card"
    USERNAME_COLUMN = ".oxd-table-cell:nth-child(2)"
    USER_ROLE_COLUMN = ".oxd-table-cell:nth-child(3)"
    EMPLOYEE_NAME_COLUMN = ".oxd-table-cell:nth-child(4)"
    STATUS_COLUMN = ".oxd-table-cell:nth-child(5)"
    EDIT_ICON = "i.bi-pencil-fill"
    DELETE_ICON = "i.bi-trash"
    
    # Edit page locators
    EDIT_USER_HEADER = "h6:has-text('Edit User')"
    EDIT_USER_ROLE_DROPDOWN = "//label[text()='User Role']/parent::div/following-sibling::div//div[@class='oxd-select-text-input']"
    EDIT_STATUS_DROPDOWN = "//label[text()='Status']/parent::div/following-sibling::div//div[@class='oxd-select-text-input']"
    
    # Delete confirmation
    DELETE_CONFIRMATION_DIALOG = ".orangehrm-modal-footer"
    CONFIRM_DELETE_BUTTON = "button:has-text('Yes, Delete')"
    CANCEL_DELETE_BUTTON = "button:has-text('No, Cancel')"
    SUCCESS_MESSAGE = ".oxd-toast-content--success"
    
    # Dropdown options
    DROPDOWN_OPTION = "div[role='option']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def click_add_button(self):
        self.wait_for_element(self.ADD_BUTTON)
        self.click_element(self.ADD_BUTTON)
        time.sleep(1)
    
    def select_user_role(self, role: str):
        self.wait_for_element(self.USER_ROLE_DROPDOWN)
        self.click_element(self.USER_ROLE_DROPDOWN)
        time.sleep(0.5)
        
        # Select from dropdown
        option_locator = f"{self.DROPDOWN_OPTION}:has-text('{role}')"
        self.page.locator(option_locator).click()
        time.sleep(0.5)
    
    def enter_employee_name(self, name_hint: str):
        self.wait_for_element(self.EMPLOYEE_NAME_INPUT)
        self.fill_text(self.EMPLOYEE_NAME_INPUT, name_hint)
        time.sleep(2)  # Wait for autocomplete suggestions
        
        # Select first suggestion
        first_suggestion = f"{self.DROPDOWN_OPTION}:first-child"
        self.page.locator(first_suggestion).click()
        time.sleep(0.5)
    
    def select_status(self, status: str):
        self.wait_for_element(self.STATUS_DROPDOWN)
        self.click_element(self.STATUS_DROPDOWN)
        time.sleep(0.5)
        
        # Select from dropdown
        option_locator = f"{self.DROPDOWN_OPTION}:has-text('{status}')"
        self.page.locator(option_locator).click()
        time.sleep(0.5)
    
    def enter_username(self, username: str):
        self.wait_for_element(self.USERNAME_INPUT)
        self.fill_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str):
        self.wait_for_element(self.PASSWORD_INPUT)
        self.fill_text(self.PASSWORD_INPUT, password)
    
    def enter_confirm_password(self, password: str):
        self.wait_for_element(self.CONFIRM_PASSWORD_INPUT)
        self.fill_text(self.CONFIRM_PASSWORD_INPUT, password)
    
    def click_save_button(self):
        self.click_element(self.SAVE_BUTTON)
        time.sleep(2)  # Wait for save operation
    
    def add_new_user(self, user_data: dict):
        self.click_add_button()
        self.select_user_role(user_data['user_role'])
        self.enter_employee_name(user_data['employee_name'])
        self.select_status(user_data['status'])
        self.enter_username(user_data['username'])
        self.enter_password(user_data['password'])
        self.enter_confirm_password(user_data['password'])
        self.click_save_button()
    
    def search_user(self, username: str):
        self.wait_for_element(self.SEARCH_USERNAME_INPUT)
        self.fill_text(self.SEARCH_USERNAME_INPUT, username)
        self.click_element(self.SEARCH_BUTTON)
        time.sleep(2)  # Wait for search results
    
    def get_user_from_table(self, username: str):
        rows = self.page.locator(self.TABLE_ROWS)
        count = rows.count()
        
        for i in range(count):
            row = rows.nth(i)
            row_username = row.locator(self.USERNAME_COLUMN).text_content()
            
            if username in row_username:
                return {
                    'username': row_username.strip(),
                    'user_role': row.locator(self.USER_ROLE_COLUMN).text_content().strip(),
                    'employee_name': row.locator(self.EMPLOYEE_NAME_COLUMN).text_content().strip(),
                    'status': row.locator(self.STATUS_COLUMN).text_content().strip(),
                    'row': row
                }
        return None
    
    def click_edit_user(self, username: str):
        user_data = self.get_user_from_table(username)
        if user_data:
            user_data['row'].locator(self.EDIT_ICON).click()
            time.sleep(1)
            self.wait_for_element(self.EDIT_USER_HEADER)
    
    def edit_user_role(self, role: str):
        self.wait_for_element(self.EDIT_USER_ROLE_DROPDOWN)
        self.click_element(self.EDIT_USER_ROLE_DROPDOWN)
        time.sleep(0.5)
        
        option_locator = f"{self.DROPDOWN_OPTION}:has-text('{role}')"
        self.page.locator(option_locator).click()
        time.sleep(0.5)
    
    def edit_status(self, status: str):
        self.wait_for_element(self.EDIT_STATUS_DROPDOWN)
        self.click_element(self.EDIT_STATUS_DROPDOWN)
        time.sleep(0.5)
        
        option_locator = f"{self.DROPDOWN_OPTION}:has-text('{status}')"
        self.page.locator(option_locator).click()
        time.sleep(0.5)
    
    def update_user(self, user_role: str = None, status: str = None):
        if user_role:
            self.edit_user_role(user_role)
        if status:
            self.edit_status(status)
        self.click_save_button()
    
    def click_delete_user(self, username: str):
        user_data = self.get_user_from_table(username)
        if user_data:
            user_data['row'].locator(self.DELETE_ICON).click()
            time.sleep(0.5)
            self.wait_for_element(self.DELETE_CONFIRMATION_DIALOG)
    
    def confirm_delete(self):
        self.click_element(self.CONFIRM_DELETE_BUTTON)
        time.sleep(2)
    
    def verify_user_exists(self, username: str):
        user_data = self.get_user_from_table(username)
        assert user_data is not None, f"User {username} not found in table"
        return user_data
    
    def verify_user_not_exists(self, username: str):
        user_data = self.get_user_from_table(username)
        assert user_data is None, f"User {username} still exists in table"
    
    def verify_success_message(self):
        expect(self.page.locator(self.SUCCESS_MESSAGE)).to_be_visible(timeout=5000)
    
    def click_reset_button(self):
        self.click_element(self.RESET_BUTTON)
        time.sleep(1)
