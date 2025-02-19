import keyboard  # Requires 'pip install keyboard'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome WebDriver
chrome_driver_path = "chromedriver.exe"  # Replace with actual path
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()

# Use existing Chrome profile
options.add_argument("--user-data-dir=C:\\Users\\Anil\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=Profile 21")  # Change if needed

options.add_experimental_option("detach", True)  # Keeps browser open
driver = webdriver.Chrome(service=service, options=options)

# Open the Google Sheet in a pinned tab
google_sheet_url = "https://docs.google.com/spreadsheets/d/1INHWRsxmdni7TW2knWXSvgu8sXJlMH1mgppa19aybpk/edit?gid=0#gid=0"
driver.execute_script(f"window.open('{google_sheet_url}', '_blank');")

# Switch back to the first tab and open the website
driver.switch_to.window(driver.window_handles[0])
driver.get("https://ops.urbanclap.com/lead")

# Wait for elements to load
wait = WebDriverWait(driver, 10)

# Get all elements at the start
elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ant-table-row")))

# Iterate through each element in order
for i in range(len(elements)):
    try:
        # Refresh elements list to avoid stale references
        elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ant-table-row")))

        if i >= len(elements):
            break  # Avoid index error if the list changes dynamically

        # Click the current element
        element = elements[i]
        ActionChains(driver).move_to_element(element).click().perform()

        # Wait for the new tab to open
        time.sleep(3)
        tabs = driver.window_handles

        # If a new tab opened, switch to it
        if len(tabs) > 2:  # Ensure it doesn't switch to Google Sheet
            driver.switch_to.window(tabs[-1])  # The last tab should be the new one

            # Wait for the "Connect" button and click it
            try:
                connect_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ant-btn-primary') and span[text()='Connect']]"))
                )
                connect_button.click()
                print(f"Clicked 'Connect' button for lead {i + 1}")

            except Exception as e:
                print(f"Could not click 'Connect' button: {e}")

            # Wait for the user to press the space key after the call
            print("Waiting for call to end... Press 'space' after disconnecting.")
            while True:
                if keyboard.is_pressed("space") and driver.current_window_handle == tabs[-1]:
                    print("Space key detected. Proceeding to call details.")
                    break
                time.sleep(0.1)

            # Click "Show My Call Details" button after the call ends
            try:
                call_details_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ant-btn-primary') and span[text()='Show My Call Details']]"))
                )
                call_details_button.click()
                print("Clicked 'Show My Call Details' button.")

            except Exception as e:
                print(f"Could not click 'Show My Call Details' button: {e}")

            # Handle form submission
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "COMPONENT-Form__CLASSNAME-container__1OZm2")))

                # Check if "Call Connection Status" is disabled (meaning call was NOT connected)
                call_not_connected = False
                try:
                    driver.find_element(By.CLASS_NAME, "ant-select-disabled")  # Will throw an error if not found
                    call_not_connected = True
                except:
                    pass  # If element is not found, call was connected

                if call_not_connected:
                    print("Call not connected. Selecting lead status automatically.")

                    # Click the Lead Status dropdown
                    lead_status_dropdown = driver.find_element(By.XPATH, "(//div[contains(@class, 'ant-select-enabled')])[1]")
                    lead_status_dropdown.click()
                    # time.sleep(1)

                    # Select the first option
                    first_option = driver.find_element(By.XPATH, "//li[@role='option'][1]")
                    first_option.click()

                    # Auto-submit the form
                    submit_button = driver.find_element(By.XPATH, "//button[span[text()='Submit']]")
                    submit_button.click()
                    print("Form submitted successfully.")

                else:
                    print("Call was connected. Please fill the form manually.")
                    print("Press 'space' when you are done.")

                # Wait until the user presses space to close the tab
                while True:
                    if keyboard.is_pressed("alt") and driver.current_window_handle == tabs[-1]:
                        print("Space key detected. Closing tab.")
                        driver.close()
                        break
                    time.sleep(0.1)

                # Switch back to the main tab after closing the current tab
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Form handling error: {e}")

        # Switch back to the main tab
        driver.switch_to.window(driver.window_handles[0])

        print(f"Processed {i + 1}/{len(elements)} leads")

    except Exception as e:
        print(f"Error processing lead {i + 1}: {e}")
        continue  # Move to the next element even if there's an error

print("All leads processed.")
driver.quit()
