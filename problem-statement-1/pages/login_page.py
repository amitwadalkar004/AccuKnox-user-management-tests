
from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    DASHBOARD_HEADER = "h6:has-text('Dashboard')"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str):
        self.wait_for_element(self.USERNAME_INPUT)
        self.fill_text(self.USERNAME_INPUT, username)
        self.fill_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        
        # Wait for dashboard to load
        self.wait_for_element(self.DASHBOARD_HEADER, timeout=15000)
    
    def verify_login_successful(self):
        expect(self.page.locator(self.DASHBOARD_HEADER)).to_be_visible()
