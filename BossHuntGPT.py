# Import the necessary libraries
import time
from appium import webdriver
import os
import cv2
import random
import discord
from discord import Intents
import asyncio
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from fuzzywuzzy import fuzz
import config

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
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    return driver

# Establish the Appium connection and assign the driver to a global variable
driver = establish_appium_connection()


# Define the words/phrases that you want to look for in the banner
banner_texts = [   
    "Mistress w",
    "Phreeoni w",
    "Kraken w",
    "Eddga w",
    "Maya w",
    "Orc Hero w",
    "Pharaoh w",
    "Orc Lord w",
    "Amon Ra w",
    "ganger w",
    "Time w",
    "Morroc w",
    "Lost Dragon w",
    "Tao Gunka w",
    "Bishop w",
    "Dead w",
    "Arc Ang",
    "Gioia w",
    "Eclipse w",
    "Dragon Fly w",
    "Mastering w",
    "Ghostring w",
    "Toad w",
    "Dramoh w",
    "Deviling w",
    "Angeling w",
    "Priest w",
    "Wolf w",
    "Chimera w",
    "Mysteltainn w",
    "Ogretooth w",
    "Necromancer w",
    "Sieger w",
    "Coelacanth w",
    "Skeggiold w",
    "Observation w",]

# Define a lookup dictionary that maps lookup boss words/phrases from the banner to their actual names
banner_lookup = {
    'Mistress w': 'Mistress',
    'Phreeoni w': 'Phreeoni',
    'Kraken w': 'Kraken',
    'Eddga w': 'Eddga',
    'Maya w': 'Maya',
    'Orc Hero w': 'Orc Hero',
    'Pharaoh w': 'Pharaoh',
    'Orc Lord w': 'Orc Lord',
    'Amon Ra w': 'Amon Ra',
    'ganger w': 'Doppelganger',
    'Time w': 'Overseer of Time',
    'Morroc w': 'Morroc',
    'Lost Dragon w': 'Lost Dragon',
    'Tao Gunka w': 'Tao Gunka',
    'Bishop w': 'Fallen Bishop',
    'Dead w': 'Lord of the Dead',
    'Arc Ang': 'Arc Angeling',
    'Gioia w': 'Gioia',
    'Eclipse w': 'Eclipse',
    'Dragon Fly w': 'Dragon Fly',
    'Mastering w': 'Mastering',
    'Ghostring w': 'Ghostring',
    'Toad w': 'Toad',
    'Dramoh w': 'King Dramoh',
    'Deviling w': 'Deviling',
    'Angeling w': 'Angeling',
    'Priest w': 'Dark Priest',
    'Wolf w': 'Vagabond Wolf',
    'Chimera w': 'Chimera',
    'Mysteltainn w': 'Mysteltainn',
    'Ogretooth w': 'Ogretooth',
    'Necromancer w': 'Necromancer',
    'Sieger w': 'Naght Sieger',
    'Coelacanth w': 'Coelacanth',
    'Skeggiold w': 'Skeggiold',
    'Observation w': 'Observation',
}

# Define a dictionary that maps full boss names to their corresponding emoji IDs
emoji_id = {
    'Mistress' : '<:mistress:1128500941654601758>',
    'Phreeoni' : '<:phreeoni:1128500973225136200>',
    'Kraken' : '<:kraken:1128500912948776970>',
    'Eddga' : '<:eddga:1128500904291729408>',
    'Maya' : '<:maya:1128500937917481044>',
    'Orc Hero' : '<:orchero:1128500955172851732>',
    'Pharaoh' : '<:pharaoh:1128500967042732163>',
    'Orc Lord' : '<:orclord:1128500958037540916>',
    'Amon Ra' : '<:amonra:1128500895320113293>',
    'Doppelganger' : '<:doppelganger:1128500900659470438>',
    'Overseer of Time' : '<:overseeroftime:1128500962076663878>',
    'Morroc' : '<:morroc:1128500946008277103>',
    'Lost Dragon' : '<:lostdragon:1128500935195369533>',
    'Tao Gunka' : '<:taogunka:1128500987758391326>',
    'Fallen Bishop' : '<:fallenbishop:1128500908431527956>',
    'Lord of the Dead' : '<:lordofthedead:1128500924466331678>',
    'Arc Angeling' : '<:arcangeling:1156347567530070077>',
    'Gioia' : '<:gioia:1156347569920815165>',
    'Eclipse' : '<:eclipse:1128501089814192250>',
    'Dragon Fly' : '<:dragonfly:1128501085783457833>',
    'Mastering' : '<:mastering:1128501105152761936>',
    'Ghostring' : '<:ghostring:1128501095765909615>',
    'Toad' : '<:toad:1128501130767368283>',
    'King Dramoh' : '<:kingdramoh:1128501100933304340>',
    'Deviling' : '<:deviling:1128501081677250632>',
    'Angeling' : '<:angeling:1128501060651204688>',
    'Dark Priest' : '<:darkpriest:1128501077571022879>',
    'Vagabond Wolf' : '<:vagabondwolf:1128501134886182955>',
    'Chimera' : '<:chimera:1128501071283753020>',
    'Mysteltainn' : '<:mysteltainn:1128501109095399504>',
    'Ogretooth' : '<:ogretooth:1128501126266892379>',
    'Necromancer' : '<:necromancer:1128501119723769918>',
    'Naght Sieger' : '<:naghtsieger:1128501113625268424>',
    'Coelacanth' : '<:coelacanth:1128501073599008770>',
    'Skeggiold' : '<:skeggiold:1156347499091599463>',
    'Observation' : '<:observation:1156347494511415316>',
}

# Define a dictionary for the status of bosses
boss_status = {
    0: 'Longer Time',
    1: 'Short Time',
    2: 'Refreshing Soon',
    3: 'Appeared',
}

# Define a dictionary for the status of mini bosses
# The initial status is set to -1 which might represent 'unknown' or 'not yet checked'
minis = {
    'Eclipse': -1,
    'Dragon Fly': -1,
    'Ghostring': -1,
    'Mastering': -1,
    'King Dramoh': -1,
    'Toad': -1,
    'Deviling': -1,
    'Angeling': -1,
    'Dark Priest': -1,
    'Vagabond Wolf': -1,
    'Chimera': -1,
    'Mysteltainn': -1,
    'Ogretooth': -1,
    'Necromancer': -1,
    'Naght Sieger': -1,
    'Coelacanth': -1,
    'Skeggiold': -1,
    'Observation': -1,
}

# Define a dictionary for the status of MVP bosses
# The initial status is set to -1 which might represent 'unknown' or 'not yet checked'
mvps = {
    'Phreeoni': -1,
    'Mistress': -1,
    'Eddga': -1,
    'Kraken': -1,
    'Maya': -1,
    'Orc Hero': -1,
    'Pharaoh': -1,
    'Orc Lord': -1,
    'Amon Ra': -1,
    'Doppelganger': -1,
    'Morroc': -1,
    'Overseer of Time': -1,
    'Lost Dragon': -1,
    'Tao Gunka': -1,
    'Lord of the Dead': -1,
    'Fallen Bishop': -1,
    'Arc Angeling': -1,
    'Gioia': -1,
}

# Load status images for each boss status
# These images are used to identify the status of a boss in the game
longer_time_img = cv2.imread('images/boss-status/longer-time.png')
short_time_img = cv2.imread('images/boss-status/short-time.png')
refreshing_soon_img = cv2.imread('images/boss-status/refreshing-soon.png')
appeared_img = cv2.imread('images/boss-status/appeared.png')

# The list of all status images for easy access later
boss_status_img = [longer_time_img, short_time_img, refreshing_soon_img, appeared_img]

# Function to pre-process an image for OCR (Optical Character Recognition)
# This function prepares an image to be used with pytesseract for extracting text from it
def preprocess_image(image):
    # Get the dimensions of the image
    width, height = image.size
    
    # Define the left, right, top and bottom boundaries for cropping the image
    # The values you see here were manually tested with a resolution of (960x540). 
    # This uses a percentage of the image's width, meaning it should adapt to different image sizes
    left = width * 0.307
    right = width * 0.74
    top = height * 0.1852
    bottom = height * 0.23148
    
    # Define the region to crop
    region = (left, top, right, bottom)

    # Crop the image to the defined region
    image = image.crop(region)

    # Convert the image to grayscale
    image = ImageOps.grayscale(image)

    # Apply a threshold to the image to make it binary (black and white)
    # Pixels with a value less than 210 become 0 (black), and others become 255 (white)
    image = image.point(lambda x: 0 if x < 210 else 255)

    return image

# Function to check if a small image (boss) is in a larger image (current_screen)
def check_in_image(boss):
    # Convert the images to grayscale
    boss_gray = cv2.cvtColor(boss, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

    # Find the small image in the larger image
    result = cv2.matchTemplate(current_gray, boss_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the small image was found in the larger image
    # The value used for max_val in the following code is (0.9) which means it needs a 90% accuracy rate to execute the code block
    if max_val > 0.9:
        # Get the coordinates of the small image in the larger image
        top_left = max_loc
        bottom_right = (top_left[0] + boss.shape[1] + 100, top_left[1] + boss.shape[0])

        # Crop the area around the small image
        cropped_image = current_screen[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Check if any of the boss status lookup images are found in the cropped image
        for i, status in enumerate(boss_status_img):

            status_result = cv2.matchTemplate(cropped_image, status, cv2.TM_CCOEFF_NORMED)

            # Spread the tuple to its own variable
            # Only one of the variables are used but the others are still necessary for the values to be stored correctly
            global_min_val, status_max_val, global_min_loc, global_max_loc = cv2.minMaxLoc(status_result)
            
            # This is similar to the previous implementation but uses an 80% accuracy value
            if status_max_val > 0.8:
                # Return whichever boss status lookup image is found in the cropped image
                return i       
    else:
        return "Image lookup failed!"

# Function to perform a swipe action in the game
async def swipe(start_y, end_y, duration, capture_speed):
    global counter, current_screen, driver

    start_x = random.randint(155, 420)
    end_x = start_x + random.randint(1,10)
    duration = 500
    try:
        driver.swipe(start_x, start_y, end_x, end_y, duration)
    except Exception as e:
        print("wiwoweeee button tap interrupted weewoo", flush=True)
        print(f"An exception occurred: {str(e)}")
        driver = establish_appium_connection()
        await cycle()

    await asyncio.sleep(capture_speed)

    await save_image("current-screen.png")
    counter = counter + 1
    current_screen = cv2.imread('current-screen.png')

    await check_for_banners('current-screen.png')

# Function to save a screenshot of the current game state
async def save_image(screenshot_filename):
    global driver
    screenshot_filepath = os.path.join(os.getcwd(), screenshot_filename)

    try:
        driver.save_screenshot(screenshot_filepath)
    except Exception as e:
        print("wiwoweeee screenshot failed weewoo", flush=True)
        print(f"An exception occurred: {str(e)}")
        driver = establish_appium_connection()
        await cycle()

# Function to check for changes in the status of a boss
async def check_for_changes(boss, boss_image, status):
    # If the boss is in the MVPs list
    if boss in mvps:
        # If the new status is different from the current status
        if status != mvps[boss]:
            print(f"checkforchanges {status} : {mvps[boss]}")
            # If the current status is -1 (unknown or not yet checked)
            if mvps[boss] == -1:
                # Update the status in the MVPs dictionary
                mvps[boss] = status
                print(f"{boss} = {boss_status[status]}", flush=True)
            # If the new status is 0 (longer time)
            elif status == 0:
                # Capture the battle results, send it to discord, and update the status in the MVPs dictionary
                await capture_battle_results(boss, boss_image)
                mvps[boss] = 0
            # If the new status is 1 (short time), update the status in the MVPs dictionary
            elif status == 1:
                mvps[boss] = 1
                print(f"{boss} = {boss_status[status]}", flush=True)
            # If the new status is 2 (refreshing soon), update the status in the MVPs dictionary
            elif status == 2:
                mvps[boss] = 2
                print(f"{boss} = {boss_status[status]}", flush=True)
            # If the new status is 3 (appeared)
            elif status == 3:
                # Get the current timestamp
                timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
                
                # Send a message to the discord with the timestamp added
                try:
                    await channel_boss_occurence.send(f"{emoji_id[boss]} **{boss}** - ***Appeared*** :green_circle: *{timestamp}*")
                except Exception as e:
                    print("wew i failed connecting to discord to send appeared", flush=True)
                    print(f"An exception occurred: {str(e)}")
                mvps[boss] = 3
    
    # If the boss is in the MINIs list
    # Performs the same as the previous block of code
    elif boss in minis:
        if status != minis[boss]:
            print(f"checkforchanges {status} : {minis[boss]}")
            if minis[boss] == -1:
                minis[boss] = status
                print(f"{boss} = {boss_status[status]}", flush=True)
            elif status == 0:
                await capture_battle_results(boss, boss_image)
                minis[boss] = 0
            elif status == 1:
                minis[boss] = 1
                print(f"{boss} = {boss_status[status]}", flush=True)
            elif status == 2:
                minis[boss] = 2
                print(f"{boss} = {boss_status[status]}", flush=True)
            elif status == 3:
                timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
                try:
                    await channel_boss_occurence.send(f"{emoji_id[boss]} **{boss}** - ***Appeared*** :green_circle: *{timestamp}*")
                except Exception as e:
                    print("wew i failed connecting to discord to send appeared", flush=True)
                    print(f"An exception occurred: {str(e)}")
                minis[boss] = 3

# Function to check for banners in the game
async def check_for_banners(filename):

    # Open the screenshot
    with Image.open(filename) as screenshot:

        # Preprocess the image for OCR
        image = preprocess_image(screenshot)

        # Extract text from the image
        try:
            extracted_text = pytesseract.image_to_string(image, config="--psm 6")
        except pytesseract.TesseractError as e:
            extracted_text = ""

        # Check if any of the banner texts are in the extracted text
        for banner_text in banner_texts:
            ratio = fuzz.partial_ratio(extracted_text, banner_text)
            if ratio >= 85:
                # If a banner text is found, send a message to the Discord server
                timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
                try:
                    await channel_banners.send(f"{emoji_id[banner_lookup[banner_text]]} **{banner_lookup[banner_text]}** ***will be spawning soon! Warriors, charge!*** *{timestamp}*")
                except Exception as e:
                    print("wew i failed connecting to discord to send banner", flush=True)
                    print(f"An exception occurred: {str(e)}")
                # Tap the close button on the banner
                banner_close_x = random.randint(710, 720)
                banner_close_y = random.randint(96, 110)
                driver.tap([(banner_close_x, banner_close_y)])
                # Break out of the loop once a banner text is detected and a message is sent
                break
            
            # Check for various other texts that might indicate a banner
            ratio1 = fuzz.partial_ratio(extracted_text, 'Adventurer')
            ratio2 = fuzz.partial_ratio(extracted_text, 'The item')
            ratio3 = fuzz.partial_ratio(extracted_text, 'The next')
            ratio4 = fuzz.partial_ratio(extracted_text, 'Due to')
            ratio5 = fuzz.partial_ratio(extracted_text, 'only')
            ratio6 = fuzz.partial_ratio(extracted_text, 'has been')
            ratio6 = fuzz.partial_ratio(extracted_text, 'Congrat')
            # If one of these texts is found, tap the close button on the banner
            if ratio1 >= 90 or ratio2 >= 90 or ratio3 >= 90 or ratio4 >= 90 or ratio5 >= 90 or ratio6 >= 90:
                banner_close_x = random.randint(710, 720)
                banner_close_y = random.randint(96, 110)
                driver.tap([(banner_close_x, banner_close_y)])
                break
    
    # Check if the game was interrupted
    await check_if_interrupted()

# Function to check if the game was interrupted (e.g., by a disconnection or update)
async def check_if_interrupted():
    global current_boss, current_boss_type, current_screen
    # If the disconnected button is visible
    if is_in('buttons/disconnected-button'):
        # While the disconnected button is visible, tap it
        while is_in('buttons/disconnected-button'):
            await tap.disconnect()
        # Reset the current boss and boss type, then start the cycle again
        current_boss = TOP_MVP
        current_boss_type = 'MVP'
        await cycle()
    # If the update button is visible, tap it until it's no longer visible
    elif is_in('buttons/update-button'):
        while is_in('buttons/update-button'):
            await tap.update()
    # If the home screen button is visible, tap the open app button until the app is launched
    elif is_in('buttons/home-screen-button'):
        is_app_launched = False
        while not is_app_launched:
            while is_in('buttons/home-screen-button'):
                print("im about to click rox app", flush=True)
                try:
                    await tap.open_app()
                except Exception as e:
                    print(f"An exception occured: {str(e)}")
            while is_in('screens/welcome-popup-screen'):
                print("im about to close welcome popup", flush=True)
                try:
                    await tap.close()
                except Exception as e:
                    print(f"An exception occured: {str(e)}")
            while is_in('buttons/enter-game-button'):
                print("im about to click enter character select", flush=True)
                try:
                    await tap.enter_character_select()
                except Exception as e:
                    print(f"An exception occured: {str(e)}")
            while is_in('buttons/select-character-button'):
                print("im about to select character", flush=True)
                try:
                    await tap.select_character()
                except Exception as e:
                    print(f"An exception occured: {str(e)}")
            while is_in('screens/in-game-popup-screen'):
                print("im about to close popup", flush=True)
                try:
                    await tap.close()
                except Exception as e:
                    print(f"An exception occured: {str(e)}")
            while is_in('screens/retrieve-screen'):
                print("im about to close retrieve screen", flush=True)
                try:
                    await tap.close()
                except Exception as e:
                    print(f"An exception occured: {str(e)}")
                is_app_launched = True
            if is_in('buttons/unhide-icons-button'):
                is_app_launched = True
            if is_in('screens/mvp-screen'):
                is_app_launched = True
            await asyncio.sleep(2)
            await save_image("current-screen.png")
            current_screen = cv2.imread('current-screen.png')
        # Reset the current boss and boss type, then start the cycle again
        current_boss = TOP_MVP
        current_boss_type = 'MVP'
        await cycle()

# The Button class represents a button in the game
class Button:
    # The find_and_tap method tries to find the given button in the current game state
    # and then simulates a tap on that button
    async def find_and_tap(self, button, button_name, capture_speed):

        global counter, current_screen, driver

        # Convert the images to grayscale
        button_gray = cv2.cvtColor(button, cv2.COLOR_BGR2GRAY)
        current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

        # Find the button in the big image
        result = cv2.matchTemplate(current_gray, button_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if the button was found
        if max_val > 0.8:
            # Get the coordinates of the button in the big image
            top_left = max_loc
            bottom_right = (top_left[0] + button.shape[1], top_left[1] + button.shape[0])

            # Tap the button
            x = random.randint(top_left[0], bottom_right[0])
            y = random.randint(top_left[1], bottom_right[1])
            try:
                driver.tap([(x, y)])
            except Exception as e:
                print("wiwoweeee button tap interrupted weewoo", flush=True)
                print(f"An exception occurred: {str(e)}")
                driver = establish_appium_connection()
                await cycle()
            await asyncio.sleep(capture_speed)
        else:
            print(f"{button_name} is not found in the image")

        # Save a screenshot of the current game state
        await save_image("current-screen.png")
        counter = counter + 1
        current_screen = cv2.imread('current-screen.png')

        # Check for banners in the current screen
        await check_for_banners('current-screen.png')

    # The following methods are for interacting with specific buttons
    # They load the image for the button, then call find_and_tap to tap it
    async def banner_close(self):
        button = cv2.imread('images/buttons/banner-close-button.png')
        await self.find_and_tap(button, "banner-close-button", 0.5)

    async def battle_screen(self):
        button = cv2.imread('images/buttons/battle-screen-button.png')
        await self.find_and_tap(button, "battle-screen-button", 0.5)
    
    async def close(self):
        button = cv2.imread('images/buttons/close-button.png')
        await self.find_and_tap(button, "close-button", 0.5)
    
    async def mini_tab(self):
        button = cv2.imread('images/buttons/mini-tab-button.png')
        await self.find_and_tap(button, "mini-tab-button", 0.2)

    async def mvp_screen(self):
        button = cv2.imread('images/buttons/mvp-screen-button.png')
        await self.find_and_tap(button, "mvp-screen-button", 0.5)
    
    async def mvp_tab(self):
        button = cv2.imread('images/buttons/mvp-tab-button.png')
        await self.find_and_tap(button, "mvp-tab-button", 0.2)

    async def unhide_icons(self):
        button = cv2.imread('images/buttons/unhide-icons-button.png')
        await self.find_and_tap(button, "unhide-icons-button", 0.5)

    async def close_battle_results(self):
        button = cv2.imread('images/screens/mvp-screen.png')
        await self.find_and_tap(button, "mvp-screen", 0)
    
    async def close_map(self):
        button = cv2.imread('images/buttons/map-close-button.png')
        await self.find_and_tap(button, "map-close-button", 0.5)

    async def close_kpass(self):
        button = cv2.imread('images/buttons/kpass-close-button.png')
        await self.find_and_tap(button, "kpass-close-button", 0.5)
    
    async def disconnect(self):
        button = cv2.imread('images/buttons/disconnected-button.png')
        await self.find_and_tap(button, "disconnected-button", 1)

    async def update(self):
        button = cv2.imread('images/buttons/update-button.png')
        await self.find_and_tap(button, "update-button", 1)
    
    async def open_app(self):
        button = cv2.imread('images/buttons/home-screen-button.png')
        await self.find_and_tap(button, "home-screen-button", 0.5)

    async def enter_character_select(self):
        button = cv2.imread('images/buttons/enter-game-button.png')
        await self.find_and_tap(button, "enter-character-select-button", 0.5)
    
    async def select_character(self):
        button = cv2.imread('images/buttons/select-character-button.png')
        await self.find_and_tap(button, "select-character-button", 0.5)

# Create an instance of the Button class
tap = Button()

# Function to check if a certain image (represented by 'location') is present in the current screen
def is_in(location):
    # Read in the image file
    screen = cv2.imread(f"images/{location}.png")

    # Convert the images to grayscale
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

    # Find the image in the big image
    result = cv2.matchTemplate(current_gray, screen_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the image was found
    if max_val > 0.8:
        return True
    else:
        return False
    
# Function to check if a certain boss (represented by 'boss_name') is present in the current screen
def locate_boss(boss_name):
    # Read in the image file for the boss
    filename = '-'.join(boss_name.lower().split()) + ".png"
    screen = cv2.imread(f"images/boss-sidebar/{filename}")

    # Convert the images to grayscale
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

    # Find the boss in the big image
    try:
        result = cv2.matchTemplate(current_gray, screen_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if the boss was found
        if max_val > 0.9:
            return True
        else:
            return False
    except Exception as e:
        print(f"An exception occurred in locate_boss: {str(e)}")

# Function to navigate to the MVP tab in the game
async def go_to_mvp_tab():
    global current_screen
    # If the battle result screen is open, close it
    if is_in('screens/battle-result-screen'):
        await tap.close_battle_results()

    # While the MVP tab screen isn't open
    while not is_in('screens/mvp-tab-screen'):
        # While the MVP screen isn't open
        while not is_in('screens/mvp-screen'):
            # While the MVP button on the home screen is hidden
            while not is_in('screens/mvp-button-screen'):
                # If the MVP button is hidden, unhide the icons
                # If the map screen or kingdom pass screen is open, close them
                if not is_in('screens/mvp-screen'):
                    await tap.unhide_icons()
                    if is_in('screens/map-screen'):
                        await tap.close_map()
                    if is_in('screens/kingdom-pass-screen'):
                        await tap.close_kpass()
                    await save_image("current-screen.png")
                    current_screen = cv2.imread('current-screen.png')
                else: 
                    break
            await tap.mvp_screen()
        if is_in('screens/battle-result-screen'):
            await tap.close_battle_results()
        await tap.mvp_tab()

async def go_to_mini_tab():
    global current_screen
    if is_in('screens/battle-result-screen'):
        await tap.close_battle_results()

    while not is_in('screens/mini-tab-screen'):
        while not is_in('screens/mvp-screen'):
            while not is_in('screens/mvp-button-screen'):
                if not is_in('screens/mvp-screen'):
                    await tap.unhide_icons()
                    if is_in('screens/map-screen'):
                        await tap.close_map()
                    if is_in('screens/kingdom-pass-screen'):
                        await tap.close_kpass()
                    await save_image("current-screen.png")
                    current_screen = cv2.imread('current-screen.png')
                else: 
                    break
            await tap.mvp_screen()
        if is_in('screens/battle-result-screen'):
            await tap.close_battle_results()
        await tap.mini_tab()

# Function to capture battle results of a boss
async def capture_battle_results(boss, boss_image):
    global counter, current_screen

    filename = '-'.join(boss.lower().split())
    find_count = 0
    # Keep running the loop until the boss is found
    while True:
        # Check if the game has restarted
        if await check_game_restarted():
            swipe_count = 0
            # Depending on the type of the current boss, reset the list of bosses and print a message
            if current_boss_type == 'MVP':
                await reset_bosses(TOP_MVP)
                print('MVP tab is reached', flush=True)
            elif current_boss_type == 'MINI':
                await reset_bosses(TOP_MINI)
                print('MINI tab is reached', flush=True)

            # While the boss isn't located, keep swiping
            while not locate_boss(boss):
                await check_game_restarted()
                if is_in('screens/battle-result-screen'):
                    await tap.close_battle_results()
                y = random.randint(235, 435)
                await swipe(y, y - 150, 100, 0.5)
                swipe_count = swipe_count + 1
                print(f'im in capture_battle_results coming from restart and this is my loop #{swipe_count}, {boss}', flush=True)
                if swipe_count == 10:
                    if is_in('screens/battle-result-screen'):
                        await tap.close_battle_results()
                    print(f"I couldn't find {boss} and its loop #{swipe_count} so i am closing up again", flush=True)
                    await close_mvp_screen()
                    swipe_count = 0

        # If the boss isn't in the screen, tap the sidebar image to make it appear
        if not is_in(f'boss-image/{filename}-wallpaper'):
            await tap.find_and_tap(boss_image, "boss-sidebar-image", 0)
        else:
            break
        
        find_count = find_count + 1
        print(f'im in capture_battle_results and this is my loop #{find_count}, {boss}', flush=True)
        if find_count == 5:
            if is_in('screens/battle-result-screen'):
                await tap.close_battle_results()
            print(f'im in capture_battle_results and this is my loop #{find_count}, {boss}. I am closing mvp screen now', flush=True)
            await close_mvp_screen()
            find_count = 0
    
    # Wait until the battle result screen is visible
    while True:
        await check_game_restarted()
        await save_image("current-screen.png")
        current_screen = cv2.imread('current-screen.png')
        if is_in(f'buttons/mvp-tab-button') or is_in(f'buttons/mini-tab-button') or is_in(f'screens/mvp-tab-screen') or is_in(f'screens/mini-tab-screen'):
            await tap.battle_screen()
        if is_in('screens/battle-result-screen'):
            break
    
    await asyncio.sleep(1)

    await save_image("current-screen.png")
    current_screen = cv2.imread('current-screen.png')
    # Crop the image to get only the part with the battle result
    cropped_image = current_screen[130:410, 80:890]
    # Downscale the image and save it
    downscaled_image = cv2.resize(cropped_image, (700, 242), interpolation=cv2.INTER_AREA)
    cv2.imwrite('battle-results.png', downscaled_image)
    counter = counter + 1

    # Send the battle result image to the Discord server
    with open('battle-results.png', "rb") as image_file:
        timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
        try:
            await channel_boss_deaths.send(f"{emoji_id[boss]} **{boss}** ***was slain!*** *{timestamp}*", file=discord.File(image_file))
        except Exception as e:
            print("wew i failed connecting to discord to send deadpics", flush=True)
            print(f"An exception occurred: {str(e)}")
    # Close the battle result screen
    while is_in('screens/battle-result-screen'):
        print(f'im in capture_battle_results and I sent battle result of {boss} to discord. I am closing now', flush=True)
        await tap.close_battle_results()

# Function to close the MVP screen
async def close_mvp_screen():
    while True:
        # If the MVP screen is open, close it
        # If the map screen is open, close it
        if is_in('screens/mvp-screen'):
            await tap.close()
        elif is_in('screens/map-screen'):
            await tap.close_map()
        else:
            break

# Function to check if the game has restarted
async def check_game_restarted():
    # If the map screen or kingdom pass screen is open, close them
    if is_in('screens/map-screen'):
        await tap.close_map()
    if is_in('screens/kingdom-pass-screen'):
        await tap.close_kpass()
    
    # If current game state is in the home screen
    if is_in('buttons/unhide-icons-button'):
        print(f'hey i reached check_game_restarted haha {current_boss_type} : {current_boss}', flush=True)
        # Depending on the type of the current boss, go back to the appropriate tab
        if current_boss_type == 'MVP':
            await go_to_mvp_tab()
            print('MVP tab is reached', flush=True)
        elif current_boss_type == 'MINI':
            await go_to_mini_tab()
            print('MINI tab is reached', flush=True)
        return True
    return False

# Function to reset the list of bosses, by swiping until the anchor boss is visible
async def reset_bosses(anchor_boss):
    if locate_boss(anchor_boss):
        return
    else:
        while not locate_boss(anchor_boss):
            await check_game_restarted()
            y = random.randint(150, 200)
            await swipe(y, y + 300, 100, 0)

        filename = '-'.join(anchor_boss.lower().split())
        boss_image = cv2.imread(f"images/boss-sidebar/{filename}.png")
        while True:
            if await check_game_restarted():
                await reset_bosses(anchor_boss)
            if not is_in(f'boss-image/{filename}-wallpaper'):
                await tap.find_and_tap(boss_image, "boss-sidebar-image", 0)
            else:
                break

# Function to get the y coordinate of the previous boss in the list
async def get_previous_y(boss_image, boss):
    global counter, current_screen, driver

    # Save the current screen and update the counter
    await save_image("current-screen.png")
    counter = counter + 1
    current_screen = cv2.imread('current-screen.png')

    # Convert the images to grayscale
    button_gray = cv2.cvtColor(boss_image, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

    # Find the button in the big image
    result = cv2.matchTemplate(current_gray, button_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the boss was found, return the y coordinate
    if max_val > 0.8:
        top_left = max_loc
        bottom_right = (top_left[0] + boss_image.shape[1], top_left[1] + boss_image.shape[0])
        y = random.randint(top_left[1], bottom_right[1])
        return y
    else:
        print(f"{boss} is not found in the image")

# Function to scan for MVPs
async def scan_mvps():
    global current_boss, current_boss_type, previous_boss
    # If the current boss is in the list of MVPs
    if current_boss in mvps:
        # Iterate over all the MVPs
        for i, boss in enumerate(mvps):
            # Determine which boss to lookout for
            if boss == current_boss:
                # Keep looping until the boss is found
                while True:
                    # If the boss is located
                    if locate_boss(boss):
                        filename = '-'.join(boss.lower().split()) + ".png"
                        boss_image = cv2.imread(f"images/boss-sidebar/{filename}")
                        # Check the status of the boss
                        status = check_in_image(boss_image)
                        # If the status has changed, handle it
                        await check_for_changes(boss, boss_image, status)
                        break
                    # Else if the boss is not located in the screen
                    else:
                        swipe_count = 0
                        # Keep trying to locate the boss until it is found
                        while not locate_boss(boss):
                            # Check if the game has restarted
                            await check_game_restarted()
                            # If the battle result screen is open, close it
                            if is_in('screens/battle-result-screen'):
                                print('i am now in scan but i detected battle-result-screen so i am closing it now', flush=True)
                                await tap.close_battle_results()

                            # Get the y coordinate of the previous boss in the list
                            filename = '-'.join(previous_boss.lower().split()) + ".png"
                            boss_image = cv2.imread(f"images/boss-sidebar/{filename}")
                            y = await get_previous_y(boss_image, previous_boss)
                            try:
                                # Swipe up to scroll down the list
                                await swipe(y, y - 150, 100, 0)
                            except Exception as e:
                                print(f"An exception occurred in get_previous_y: {str(e)}")
                                y = random.randint(235, 435)
                                await swipe(y, y - 150, 100, 0.5)
                            # Increase the swipe count
                            swipe_count = swipe_count + 1
                            # If the swipe count reaches 10, it might have run into a problem. Close the MVP screen and reset the swipe count
                            if swipe_count == 10:
                                if is_in('screens/battle-result-screen'):
                                    await tap.close_battle_results()
                                await close_mvp_screen()
                                swipe_count = 0

                # If it's the last item in the list
                if i == len(mvps) - 1:
                    # Handle the last item: Switch to scanning for MINIs
                    current_boss = TOP_MINI
                    current_boss_type = 'MINI'
                # Otherwise, set the current boss to the next one in the list
                else:
                    current_boss = list(mvps.keys())[i + 1]

                previous_boss = boss

# The function for scanning for MINIs is similar to the function for scanning for MVPs
# The main difference is that it switches to scanning for MVPs after scanning all the MINIs
async def scan_minis():
    global current_boss, current_boss_type, previous_boss
    if current_boss in minis:
        for i, boss in enumerate(minis):
            if boss == current_boss:
                while True:
                    if locate_boss(boss):
                        filename = '-'.join(boss.lower().split()) + ".png"
                        boss_image = cv2.imread(f"images/boss-sidebar/{filename}")
                        status = check_in_image(boss_image)
                        await check_for_changes(boss, boss_image, status)
                        break
                    else:
                        swipe_count = 0
                        while not locate_boss(boss):

                            await check_game_restarted()
                            if is_in('screens/battle-result-screen'):
                                print('i am now in scan but i detected battle-result-screen so i am closing it now', flush=True)
                                await tap.close_battle_results()

                            filename = '-'.join(previous_boss.lower().split()) + ".png"
                            boss_image = cv2.imread(f"images/boss-sidebar/{filename}")

                            y = await get_previous_y(boss_image, previous_boss)
                            try:
                                await swipe(y, y - 150, 100, 0)
                            except Exception as e:
                                print(f"An exception occurred in get_previous_y: {str(e)}")
                                y = random.randint(235, 435)
                                await swipe(y, y - 150, 100, 0.5)

                            swipe_count = swipe_count + 1

                            if swipe_count == 10:
                                if is_in('screens/battle-result-screen'):
                                    await tap.close_battle_results()
                                await close_mvp_screen()
                                swipe_count = 0

                # If it's the last item in the list
                if i == len(minis) - 1:
                    # Handle the last item: Switch to scanning for MVPs
                    current_boss = TOP_MVP
                    current_boss_type = 'MVP'
                # Otherwise, set the current boss to the next one in the list
                else:
                    current_boss = list(minis.keys())[i + 1]
                
                previous_boss = boss

# Create a Discord client with default intents
intents = discord.Intents.default()

# Create a Discord client
client = discord.Client(intents=intents)

# Set the IDs of the Discord channels to send messages to
channel_banners_id = 1131350310284185631
channel_boss_occurence_id = 1131350326855880734
channel_boss_deaths_id = 1131350334908932197

# Event listener for when the bot is ready
@client.event
async def on_ready():
    global channel_banners, channel_boss_occurence, channel_boss_deaths, counter, current_screen, current_boss, current_boss_type, TOP_MVP, TOP_MINI

    # Find the channel to send messages to
    channel_banners = client.get_channel(channel_banners_id)
    channel_boss_occurence = client.get_channel(channel_boss_occurence_id)
    channel_boss_deaths = client.get_channel(channel_boss_deaths_id)

    # Set the first boss (anchor boss) to be scanned for each type
    TOP_MVP = "Mistress"
    TOP_MINI = "Dragon Fly"
    
    # Initialize the counter and save the current screen
    counter = 0
    await save_image("current-screen.png")
    counter = counter + 1
    print(f"(initial) Count = {counter}", flush=True)

    current_screen = cv2.imread('current-screen.png')
    
    # Set the current boss and boss type
    current_boss = TOP_MVP
    current_boss_type = 'MVP'

    # Start the cycle of scanning for bosses
    await cycle()

# Function to perform a cycle of scanning for bosses
async def cycle():
    arr = []
    while True:
        start_time = time.time()
        # Go to the MVP tab and reset the list of MVPs
        await go_to_mvp_tab()
        await reset_bosses(TOP_MVP)
        # Scan for MVPs and then close the MVP screen
        await scan_mvps()
        await close_mvp_screen()
        # Go to the MINI tab and reset the list of MINIs
        await go_to_mini_tab()
        await reset_bosses(TOP_MINI)
        # Scan for MINIs and then close the MVP screen
        await scan_minis()
        await close_mvp_screen()
        end_time = time.time()
        print(f"Time for 1 cycle: {end_time - start_time:.2f} seconds", flush=True)
        arr.append(end_time - start_time)
        average = sum(arr) / len(arr)
        print(f"Average: {average:.2f} seconds", flush=True)
# Start the bot
while True:
    try:
        client.run(config.BOT_TOKEN)
    except Exception as e:
        print("ooo exception in client.run don't know why", flush=True)
        print(f"An exception occurred: {str(e)}")
        
        driver = establish_appium_connection()
        # Perform any necessary cleanup or error handling
        # before restarting the client