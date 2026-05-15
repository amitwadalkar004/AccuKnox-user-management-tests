from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import time

class DashboardPage(BasePage):
    # Locators
    ADMIN_MENU = "//span[text()='Admin']"
    DASHBOARD_HEADER = "h6:has-text('Dashboard')"
    ADMIN_PAGE_HEADER = "//h6[text()='Admin']"
    SYSTEM_USERS_TABLE = ".oxd-table"
    ADD_BUTTON = "button:has-text('Add')"
    
    def __init__(self, page: Page):
        super().__init__(page)
    


    
    def navigate_to_admin(self):
        """Navigate to Admin module and wait for page to load"""
        self.wait_for_element(self.ADMIN_MENU, timeout=10000)
        self.click_element(self.ADMIN_MENU)
        time.sleep(2)  # Wait for page transition
        
        # Wait for Admin page to load - check for System Users table or Add button
        self.wait_for_element(self.ADD_BUTTON, timeout=15000)
    

    def verify_admin_page_loaded(self):
        """Verify Admin page is loaded successfully"""
        expect(self.page.locator(self.ADMIN_PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.ADD_BUTTON)).to_be_visible()