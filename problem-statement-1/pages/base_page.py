
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
    
    def click_element(self, locator: str):
        self.page.locator(locator).click()
    
    def fill_text(self, locator: str, text: str):
        self.page.locator(locator).fill(text)
    

    
    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content()
    
    def wait_for_element(self, locator: str, timeout: int = 10000):
        self.page.wait_for_selector(locator, timeout=timeout)
    
    def is_element_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()

