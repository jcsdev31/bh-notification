from appium import webdriver
import discord_connect as dc
import waitlist as wl

driver = None

# Function to establish Appium connection with the emulator/device
def establish_appium_connection(udid):
    # Set the capabilities for the Appium connection
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "autoGrantPermissions": False,
        "udid": udid,  # This is the device ID, replace this with your device ID
        "noReset": True
    }

    # Establish the Appium connection and return the driver object
    return webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

async def start_appium_session(udid):
    global driver
    
    try:
        driver.quit()
        print("CLOSING PREVIOUS DRIVER TO START A NEW ONE")
    except:
        print("No open drivers detected. Safe to proceed!")
    
    # Establish the Appium connection and assign the driver to a global variable
    try:
        driver = establish_appium_connection(udid)
    except Exception as e:
        dc.set_is_running(False)
        await wl.set_error_waitlist("Cannot connect to a driver!", str(e))
        await wl.set_type_waitlist("error")
        await dc.alert_shutdown()
        
    return driver
    
    
def stop_appium_session():
    try:
        driver.quit()
        print("CLOSING OPEN APPIUM DRIVERS")
    except:
        print("No open drivers running!")