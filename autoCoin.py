
import platform
import time
import os
import json
from webDriverLib import WebDriverLibrary, ConfigReader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Đường dẫn đến file cấu hình JSON
config_path = "config.json"

# Đường dẫn đến ChromeDriver và profile Chrome
target_url = "https://mail.google.com/mail/u/0/#inbox"  # Thay đổi URL này thành trang web bạn muốn điều hướng đến

# Đọc cấu hình từ file JSON
config = ConfigReader.read_config(config_path)

# Get the current user's home directory
home_dir = os.path.expanduser("~")
username = os.path.basename(home_dir)

# Replace the placeholder with the actual username
config['chrome_profile_path'] = config['chrome_profile_path'].replace('{username}', username)

#time to wait for action
timeWait = config["timeWait"]

# Khởi tạo đối tượng WebDriverLibrary
os_name = platform.system()
if (os_name == "Windows"):
    driver = WebDriverLibrary(config['path_Chrome_window'], config['profile_path_windows'])
else:
    driver = WebDriverLibrary(config['path_chrome_driver'], config['chrome_profile_path'])
time.sleep(timeWait)

# Mở trang web
print ("open wwebsite")
driver.open_website(config["target_url"])


# connect wallet
button = connect_wallet_button = driver.wait_for_element(By.XPATH, config["connectWallet"])
print("Connect Wallet button found:", connect_wallet_button)

button.click()
print("Connect Wallet button clicked")
time.sleep(timeWait)

#click on metamask
button = driver.wait_for_element(By.XPATH, config["metaMask"])
print("MetaMask button found:", button)
button.click()
print("MetaMask button clicked")
time.sleep(timeWait)


# Wait for Metamask pop-up window to appear
def wait_for_metamask_popup():
    all_windows = driver.driver.window_handles

    # Wait until the number of windows increases
    while len(all_windows) == 1:
        time.sleep(1)
        all_windows = driver.driver.window_handles

    # Switch to the new window
    for window in all_windows:
        if window != tekika_window:
            print(">> Metamask popup")
            driver.driver.switch_to.window(window)
            time.sleep(timeWait)
            print(">> Switched to Metamask window")
            break

def wait_for_metamask_altural_popup(timeout=10):
    all_windows = driver.driver.window_handles

    # Wait until the number of windows increases
    count = 0
    while len(all_windows) == 2 and count < timeout:
        time.sleep(1)
        all_windows = driver.driver.window_handles
        count = count + 1

    # Switch to the new window
    for window in all_windows:
        if (window != tekika_window) and (window != altura_window):
            print(">> Metamask popup")
            driver.driver.switch_to.window(window)
            time.sleep(timeWait)
            print(">> Switched to Metamask window")
            break


if (driver.get_number_of_windows() > 1):
    current_window_handle = driver.driver.current_window_handle
    driver.get_title_of_all_windows()
    try:
        driver.switch_to_window(1)
        windowMetamask = driver.driver.current_window_handle
        time.sleep(timeWait)
        print("Switched to MetaMask window")

        password = driver.wait_for_element(By.ID, config["passwordId"])
        password.send_keys(config["passMetamask"])
        print("Password entered")
        time.sleep(timeWait)

        
        button = driver.wait_for_element(By.XPATH, config["unlockBtn"])
        button.click()
        print("Unlock button clicked")
        time.sleep(timeWait)
	
        if driver.get_number_of_windows() > 1:
            button = driver.wait_for_element(By.XPATH, config["nextBtn"])
            button.click()
            print("Next button clicked")
            time.sleep(timeWait)

            button = driver.wait_for_element(By.XPATH, config["confirmBtn"])
            button.click()
            print("Confirm button clicked")
            time.sleep(timeWait)
        else:
                print("MetaMask window closed before completing actions")
        
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print ("close metamask window")
        try:
            driver.close_window()
        except Exception as e:
            print ("close metamask window closed before completing actions")
        driver.switch_to_window(1)
        driver.close_window()
        print("close MetaMask Offscreen window ")
        print("Switched back to main window")
        driver.switch_to_window(0)
else:
    print("MetaMask window not found")

try:
    print("linh")
    button = driver.wait_for_element(By.XPATH, config["signinBtn"],timeout=1)
    button.click()
    print("Signin button clicked")
    time.sleep(timeWait)
    tekika_window = driver.driver.current_window_handle
    
    all_windows = driver.driver.window_handles

    # Wait until the number of windows increases
    count = 0
    while len(all_windows) == 1 and count < 10:
        time.sleep(1)
        all_windows = driver.driver.window_handles
        count = count + 1

    # Switch to the new window
    for window in all_windows:
        if (window != tekika_window):
            print(">> Metamask popup")
            driver.driver.switch_to.window(window)
            time.sleep(timeWait)
            print(">> Switched to Metamask window")
            break
    
    
    signBtn_extra = "/html/body/div[1]/div/div/div/div/div[3]/button[2]"

    # button = driver.wait_for_element(By.XPATH, '//button[text()="Confirm"]',timeout=1)
    button = driver.wait_for_element(By.XPATH, signBtn_extra, timeout=1)
    button.click()
    time.sleep(timeWait)
    driver.switch_to_window(tekika_window)

except Exception as e:
    print(f"An error occurred: {e}")
    print ("not need sign in")
    
# Ensure to switch back to tekika window   
time.sleep(3)
driver.switch_to_window(0)
button = driver.wait_for_element(By.XPATH, config["avatarBtn"])
button.click()
print("Avatar button clicked")
time.sleep(timeWait)

button = driver.wait_for_element(By.XPATH, config["progressBtn"])
button.click()
print("Progress button clicked")
time.sleep(timeWait)

x = 100
y = 100
driver.click_at_coordinates(x, y)

# Ensure everything is loaded
time.sleep(5)

tekika_window = driver.driver.current_window_handle

button = driver.wait_for_element(By.XPATH, config["relic3Btn"])
button.click()
print("Relic 3 button clicked")
time.sleep(timeWait)

# Ensure new windows is open
if (driver.get_number_of_windows() > 1):
    current_window_handle = driver.driver.current_window_handle
    driver.get_title_of_all_windows()
    driver.switch_to_window(1)
    altura_window = driver.driver.current_window_handle
    time.sleep(timeWait)
    print("Switched to NFT window")

altura_window = driver.driver.current_window_handle
    
try:
    wait_for_metamask_altural_popup()
    button = driver.wait_for_element(By.XPATH, config["alturaMetaSignBtn"])
    button.click()
    print("Altura Meta Sign clicked")
    time.sleep(1)

    all_windows = driver.driver.window_handles
    # Wait until the number of windows decreases
    while len(all_windows) == 1:
        time.sleep(1)
        all_windows = driver.driver.window_handles

    driver.switch_to_window(1)
    print("Switched back to NFT window")
    time.sleep(2)
    # Reload the page to ensure can click on the button
    driver.driver.refresh()
    print("Refresh NFT window")
    time.sleep(5)
except Exception as e:
    print(f"No metamask popup: {e}")

while (1):
    try:
        button = driver.wait_for_element(By.XPATH, config["buyNowBtn"])
        button.click()
        print("Buy NOW clicked")
        time.sleep(5)
    except Exception as e:
        print("Buy NOW button not found")

    time.sleep(100000)

    mint_new_section = driver.driver.find_elements(By.XPATH, "/html/body/div[3]/div[3]/div/div/div[2]/h4[1]")
    if mint_new_section:
        print("Mint New section found")
    else:
        print("Mint New section not found")

    if mint_new_section:
        button = driver.wait_for_element(By.XPATH, config["buyFreeBtn"])
        button.click()
        print("Buy Free clicked")
        
        button = driver.wait_for_element(By.XPATH, config["buyMaxBtn"])
        button.click()
        print("Maximize number clicked")
        time.sleep(timeWait)

        button = driver.wait_for_element(By.XPATH, config["purchaseBtn"])
        button.click()
        print("Purchase clicked")
        time.sleep(timeWait)

        wait_for_metamask_altural_popup()

        button = driver.wait_for_element(By.XPATH, config["confirmBtn1"])
        button.click()
        print("Confirm buy clicked")
        time.sleep(timeWait)
        break;
    else:
        print("Not mintable yet")
        time.sleep(300)

    driver.driver.refresh()
    print("Refresh NFT window")

time.sleep(10000)
# Ví dụ sử dụng hàm wait_for_element để chờ đợi một phần tử xuất hiện
#element = driver.wait_for_element(By.XPATH, '//*[@id="example-element-id"]')
# print("Element found:", element)

# Đóng trình duyệt sau khi hoàn thành
# driver.quit_driver()
