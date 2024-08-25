
from webDriverLib import WebDriverLibrary, ConfigReader
from selenium.webdriver.common.by import By

# Đường dẫn đến ChromeDriver và profile Chrome
target_url = "https://mail.google.com/mail/u/0/#inbox"  # Thay đổi URL này thành trang web bạn muốn điều hướng đến


# Đường dẫn đến file cấu hình JSON
config_path = "config.json"

# Đọc cấu hình từ file JSON
config = ConfigReader.read_config(config_path)

# Khởi tạo đối tượng WebDriverLibrary
driver = WebDriverLibrary(config['path_chrome_driver'], config['chrome_profile_path'])

# Mở trang web
driver.open_website(config["target_url"])

# Ví dụ sử dụng hàm wait_for_element để chờ đợi một phần tử xuất hiện
#element = driver.wait_for_element(By.XPATH, '//*[@id="example-element-id"]')
# print("Element found:", element)

# Đóng trình duyệt sau khi hoàn thành
# driver.quit_driver()