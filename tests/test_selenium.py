from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import time

class TestSchoolManagement(unittest.TestCase):
    def setUp(self):
        try:
            # Setup Chrome driver with proper service
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
            self.driver.get("http://localhost:3000")
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 20)  # Increased timeout to 20 seconds
            print("Browser opened successfully")
        except Exception as e:
            print(f"Error in setup: {str(e)}")
            raise

    def test_student_login_flow(self):
        """Test complete student login flow"""
        try:
            print("Starting student login flow test")
            # Navigate to role selection
            self.driver.get("http://localhost:3000/choose")
            time.sleep(2)  # Wait for page load

            # Click on Student card
            student_card = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//h2[contains(text(), 'Student')]/ancestor::div[contains(@class, 'MuiPaper-root')]"))
            )
            student_card.click()
            print("Clicked Student card")
            time.sleep(2)  # Wait for navigation

            # Verify we're on student login page
            self.assertTrue("/Studentlogin" in self.driver.current_url)
            print("On student login page")

            # Enter student credentials
            roll_number = self.wait.until(
                EC.presence_of_element_located((By.NAME, "rollNumber"))
            )
            roll_number.send_keys("123")
            print("Entered roll number")

            student_name = self.driver.find_element(By.NAME, "studentName")
            student_name.send_keys("Akshay")
            print("Entered student name")

            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys("12345678")
            print("Entered password")

            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            print("Clicked login button")
            time.sleep(3)  # Wait for navigation

            # Verify we're on student dashboard
            self.assertTrue("/Student/dashboard" in self.driver.current_url)
            print("URL verified")

            # Verify dashboard elements
            # Check for dashboard title
            dashboard_title = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'Student Dashboard')]"))
            )
            self.assertTrue(dashboard_title.is_displayed())
            print("Dashboard title found")

            # Check for sidebar
            sidebar = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "nav.MuiDrawer-root"))
            )
            self.assertTrue(sidebar.is_displayed())
            print("Sidebar found")

            # Check for main content area
            main_content = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "main.MuiBox-root"))
            )
            self.assertTrue(main_content.is_displayed())
            print("Main content area found")

            print("Successfully verified student dashboard")

        except TimeoutException as e:
            print(f"Timeout waiting for element: {str(e)}")
            raise
        except NoSuchElementException as e:
            print(f"Element not found: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

    def tearDown(self):
        try:
            self.driver.quit()
            print("Browser closed successfully")
        except Exception as e:
            print(f"Error closing browser: {str(e)}")

if __name__ == "__main__":
    unittest.main()
