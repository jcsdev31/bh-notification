from appium import webdriver

driver = None

# Function to establish Appium connection with the emulator/device
def establish_appium_connection():
    # Set the capabilities for the Appium connection
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "autoGrantPermissions": False,
        "udid": "127.0.0.1:5625",  # This is the device ID, replace this with your device ID
        "noReset": True
    }

    # Establish the Appium connection and return the driver object
    return webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

def start_an_appium_session():
    global driver
    
    try:
        driver.quit()
        print("CLOSING PREVIOUS DRIVER TO RESTART A NEW ONE")
    except:
        print("NO DRIVER SESSION DETECTED")
    
    # Establish the Appium connection and assign the driver to a global variable
    driver = establish_appium_connection()
    
start_an_appium_session()
start_an_appium_session()