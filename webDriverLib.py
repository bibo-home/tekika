import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

class ConfigReader:
    @staticmethod
    def read_config(config_path):
        """
        Đọc file cấu hình JSON và trả về nội dung dưới dạng dictionary.
        
        :param config_path: Đường dẫn đến file cấu hình JSON
        :return: Dictionary chứa các thông tin cấu hình
        """
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config

class WebDriverLibrary:
    def __init__(self, path_chrome_driver, chrome_profile_path):
        self.path_chrome_driver = path_chrome_driver
        self.chrome_profile_path = chrome_profile_path
        self.driver = self.init_driver()

    def init_driver(self):
        # Initialize Chrome options
        print ("init Options")
        options = webdriver.ChromeOptions()
        service = Service(self.path_chrome_driver)
        #options.add_argument("user-data-dir=" + self.chrome_profile_path)
        options.add_argument("start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình
        options.add_argument("--no-sandbox")  # Bỏ qua mô hình bảo mật của hệ điều hành
        
        options.add_argument("--disable-dev-shm-usage")  # Khắc phục vấn đề tài nguyên hạn chế
       # Detect operating system
        os_name = platform.system()
        if os_name == "Windows":
            options.add_argument("--disable-gpu")  # Áp dụng cho hệ điều hành Windows
            # User's data path
            options.add_argument('--user-data-dir='+ self.chrome_profile_path)
            # Profile directory
            options.add_argument('--profile-directory=Profile 3')
            
        else:
            options.add_argument("user-data-dir=" + self.chrome_profile_path)
        print ("init driver")

        driver = webdriver.Chrome(service=service, options=options)
        print ("init sucess")
        return driver

    def wait_for_element(self, by, value, timeout=10):
        """
        Chờ đợi phần tử xuất hiện trong một khoảng thời gian nhất định.
        
        :param by: Loại selector (By.XPATH, By.ID, By.CSS_SELECTOR, v.v.)
        :param value: Giá trị của selector
        :param timeout: Thời gian chờ đợi tối đa (mặc định là 10 giây)
        :return: Phần tử đã tìm thấy
        """
        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except Exception as e:
            print("Element not found:", e)
            
    def wait_for_element_to_be_clickable(self, by, value, timeout=30):
        """
        Chờ đợi phần tử trở nên có thể click được trong một khoảng thời gian nhất định.
        
        :param by: Loại selector (By.XPATH, By.ID, By.CSS_SELECTOR, v.v.)
        :param value: Giá trị của selector
        :param timeout: Thời gian chờ đợi tối đa (mặc định là 10 giây)
        :return: Phần tử đã tìm thấy
        """
        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.element_to_be_clickable((by, value)))
            return element
        except Exception as e:
            print( "Timeout waiting for element to be clickable:", e)
            return None
    def wait_for_window_open(self, currentWindowNumber, timeout=10):
        """
        Chờ đợi một cửa sổ mới được mở ra trong một khoảng thời gian nhất định.
        
        :param driver: Đối tượng WebDriver
        :param timeout: Thời gian chờ đợi tối đa (mặc định là 10 giây)
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: len(self.driver.window_handles) > currentWindowNumber)
    
    def reload_page(self):  
        self.driver.refresh()
        time.sleep(5)  # Đợi 5 giây để trang web tải hoàn toàn

    def open_website(self, url):
        self.driver.get(url)
        time.sleep(5)  # Đợi 5 giây để trang web tải hoàn toàn

    def get_number_of_windows(self):
        """
        Returns the number of windows currently open in the WebDriver session.
        
        :param driver: The WebDriver instance
        :return: The number of open windows
        """
        return len(self.driver.window_handles)   
    def switch_to_window(self, window_index):
        """
        Chuyển sang cửa sổ trình duyệt khác.
        
        :param driver: Đối tượng WebDriver
        :param window_index: Chỉ số của cửa sổ cần chuyển sang
        """
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def close_window(self):
        """
        Đóng cửa sổ trình duyệt hiện tại.
        
        :param driver: Đối tượng WebDriver
        """
        self.driver.close()

    # def click_at_coordinates(self, x, y):
    #     action = ActionChains(self.driver)
    #     action.move_by_offset(x, y).click().perform()
    #     print(f"Clicked at coordinates ({x}, {y})")

    def click_at_coordinates(self, x, y):
        # Maximize the browser window
        self.driver.maximize_window()

        # Get the window size
        window_size = self.driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']

        # Check if the coordinates are within the bounds of the window
        if 0 <= x <= window_width and 0 <= y <= window_height:
            action = ActionChains(self.driver)
            action.move_by_offset(x, y).click().perform()
            print(f"Clicked at coordinates ({x}, {y})")
        else:
            print(
                f"Coordinates ({x}, {y}) are out of bounds for the window size ({window_width}, {window_height})")


    def click_dropdown_and_select_option_by_XPATH(self, locatorDropDown, textFind):
        # Click the dropdown to open it
        dropdown = self.wait_for_element(By.XPATH, locatorDropDown)
        dropdown.click()
        print("Dropdown clicked")

        search = self.wait_for_element(By.XPATH, '//input[@name="tokenSearchInput"]')
        search.send_keys(textFind)
        print("enter search text")

        # Wait for the option to be visible and click it
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER).perform()
        print("Option selected")   

    def get_attribute_value(self, by, locator, attribute_name):
        element = self.wait_for_element(by, locator)
        if element:
            return element.get_attribute(attribute_name)
        else:
            print("get_attribute_value: Element not found")

    def get_title_of_all_windows(self):
        currentWindow = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            print(self.driver.title)

        self.driver.switch_to.window(currentWindow)

    def quit_driver(self):
        self.driver.quit()

    def click_claim_buttons(self):
        try:
            # Find all buttons with the specified class
            buttons = self.driver.find_elements(By.CLASS_NAME, "chakra-button")
            
            for button in buttons:
                # Check the text of each button
                if button.text == "Claim":
                    button.click()
                    print("Clicked a 'Claim' button")
                    time.sleep(5)  # Wait for 5 seconds after each click
                    return True
                    
            return False
        except Exception as e:
            print("No daily claim:", e)
            return False
                
    def click_buttons_and_confirm(self):
        likeAndReTweet = "/html/body/div[4]/div[3]/div/section/footer/button[2]"
        try:
            # Find all buttons with the specified class
            buttons = self.driver.find_elements(By.CLASS_NAME, "chakra-button")
            
            # Print all buttons found
            for button in buttons:
                print(button.text)
                
            clicked_any = False
            
            for button in buttons:
                # Check the text of each button
                if button.text in ["Like tweet", "Re-tweet"]:
                    button.click()
                    print(f"Clicked '{button.text}' button")
                    time.sleep(random.uniform(2, 5))  # Wait for 2 seconds for the pop-up to appear

                    # Wait for the specific button in the pop-up and click it
                    confirm_button = self.wait_for_element(By.XPATH, likeAndReTweet)
                    confirm_button.click()
                    print(f"Clicked '{confirm_button.text}' button in the pop-up")
                    time.sleep(random.uniform(2, 5))  # Wait for 5 seconds after each confirm click
                    clicked_any = True
                time.sleep(random.uniform(2, 5))  # Wait for 2 seconds after each click
                    
            return clicked_any
        except Exception as e:
            print("No daily quest:", e)
            return False
