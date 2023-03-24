from appium import webdriver

# Set up Appium connection
desired_caps = {
    'platformName': 'Android',
    'platformVersion': '7.1.1',
    'deviceName': 'Android Emulator',
    'appPackage': 'com.play.rosea',
    'appActivity': '.MainActivity'
}

# Print a message to indicate that the driver is being created
print("Creating Appium driver...")

# Create a new instance of the Appium driver
driver = webdriver.Remote('http://10.237.228.114:4723/wd/hub', desired_caps)

# Print a message to indicate that the driver has been created
print("Appium driver created.")

# Quit the driver
driver.quit()

# Print a message to indicate that the driver has been quit
print("Appium driver quit.")