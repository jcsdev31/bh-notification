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

def establish_appium_connection():
    # Set the driver settings for Appium Connection
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "autoGrantPermissions": False,
        "udid": "127.0.0.1:5625",  # Change this with device name found in "adb devices" cmd
        "noReset": True
    }

    # Establish the Appium connection and return the driver object
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    return driver

# Call the function to establish the Appium connection and assign the driver to a variable
driver = establish_appium_connection()


# Set the banner text to monitor for
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
    "Coelacanth w"]

# Check the full name of the boss in the banner
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
    'Coelacanth w': 'Coelacanth'
}

# Check the full name of the boss in the banner
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
}

# Define a dictionary for the boss status
boss_status = {
    0: 'Longer Time',
    1: 'Short Time',
    2: 'Refreshing Soon',
    3: 'Appeared'
}

# Define a dictionary for the bosses and their status
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
}

# Define a dictionary for the bosses and their status
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
}

# Load status images
longer_time_img = cv2.imread('images/boss-status/longer-time.png')
short_time_img = cv2.imread('images/boss-status/short-time.png')
refreshing_soon_img = cv2.imread('images/boss-status/refreshing-soon.png')
appeared_img = cv2.imread('images/boss-status/appeared.png')
boss_status_img = [longer_time_img, short_time_img, refreshing_soon_img, appeared_img]

# Pre-Process Image for OCR
def preprocess_image(image):

    width, height = image.size # Get the width and height of the image
    
    left = width * 0.307
    right = width * 0.74
    top = height * 0.1852
    bottom = height * 0.23148
    
    region = (left, top, right, bottom)
    image = image.crop(region)
    image = ImageOps.grayscale(image)
    image = image.point(lambda x: 0 if x < 210 else 255)

    return image

def check_in_image(boss):

    # Convert the images to grayscale
    boss_gray = cv2.cvtColor(boss, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

    # Find the image in the big image
    result = cv2.matchTemplate(current_gray, boss_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the small image was found
    if max_val > 0.9:
        # Get the coordinates of the small image in the big image
        top_left = max_loc
        bottom_right = (top_left[0] + boss.shape[1] + 100, top_left[1] + boss.shape[0])

        # Crop the area around the small image
        cropped_image = current_screen[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Save the cropped image to disk
        # cv2.imwrite('cropped_image.png', cropped_image)

        # Check if any of the global images are found in the cropped image
        for i, status in enumerate(boss_status_img):

            status_result = cv2.matchTemplate(cropped_image, status, cv2.TM_CCOEFF_NORMED)
            global_min_val, status_max_val, global_min_loc, global_max_loc = cv2.minMaxLoc(status_result)
            if status_max_val > 0.8:
                # The global image was found in the cropped image
                return i
                
    else:
        return "Image lookup failed!"

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

    # await asyncio.sleep(0.2)
    # if counter % 2 == 0:
    await check_for_banners('current-screen.png')

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


async def check_for_changes(boss, boss_image, status):
    if boss in mvps:
        if status != mvps[boss]:
            print(f"checkforchanges {status} : {mvps[boss]}")
            if mvps[boss] == -1:
                mvps[boss] = status
                print(f"{boss} = {boss_status[status]}", flush=True)
            elif status == 0:
                await capture_battle_results(boss, boss_image)
                mvps[boss] = 0
            elif status == 1:
                mvps[boss] = 1
                print(f"{boss} = {boss_status[status]}", flush=True)
            elif status == 2:
                mvps[boss] = 2
                print(f"{boss} = {boss_status[status]}", flush=True)
            elif status == 3:
                timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
                try:
                    await channel_boss_occurence.send(f"{emoji_id[boss]} **{boss}** - ***Appeared*** :green_circle: *{timestamp}*")
                except Exception as e:
                    print("wew i failed connecting to discord to send appeared", flush=True)
                    print(f"An exception occurred: {str(e)}")
                mvps[boss] = 3
                
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

async def check_for_banners(filename):

    # Open the captured screenshot using the PIL module
    with Image.open(filename) as screenshot:

        # Pre-Process the Image Object
        # image = screenshot.resize((screenshot.width * 3, screenshot.height * 3))
        image = preprocess_image(screenshot)

        # Extract text from the image using Tesseract 
        try:
            extracted_text = pytesseract.image_to_string(image, config="--psm 6")
            #print(extracted_text)
        except pytesseract.TesseractError as e:
            #print(f"Error: {e}")
            extracted_text = ""

        # Check if the banner text is present in the extracted text
        for banner_text in banner_texts:
            ratio = fuzz.partial_ratio(extracted_text, banner_text)
            if ratio >= 85:
                # Generate message sent to discord
                timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
                try:
                    await channel_banners.send(f"{emoji_id[banner_lookup[banner_text]]} **{banner_lookup[banner_text]}** ***will be spawning soon! Warriors, charge!*** *{timestamp}*")
                except Exception as e:
                    print("wew i failed connecting to discord to send banner", flush=True)
                    print(f"An exception occurred: {str(e)}")

                banner_close_x = random.randint(710, 720)
                banner_close_y = random.randint(96, 110)
                driver.tap([(banner_close_x, banner_close_y)])
                # Break out of the loop once a banner text is detected and a message is sent
                break
            
            ratio1 = fuzz.partial_ratio(extracted_text, 'Adventurer')
            ratio2 = fuzz.partial_ratio(extracted_text, 'The item')
            ratio3 = fuzz.partial_ratio(extracted_text, 'The next')
            ratio4 = fuzz.partial_ratio(extracted_text, 'Due to')
            ratio5 = fuzz.partial_ratio(extracted_text, 'only')
            ratio6 = fuzz.partial_ratio(extracted_text, 'has been')
            ratio6 = fuzz.partial_ratio(extracted_text, 'Congrat')
            if ratio1 >= 90 or ratio2 >= 90 or ratio3 >= 90 or ratio4 >= 90 or ratio5 >= 90 or ratio6 >= 90:
                banner_close_x = random.randint(710, 720)
                banner_close_y = random.randint(96, 110)
                driver.tap([(banner_close_x, banner_close_y)])
                break

    await check_if_interrupted()

async def check_if_interrupted():
    global current_boss, current_boss_type, current_screen
    if is_in('buttons/disconnected-button'):
        while is_in('buttons/disconnected-button'):
            await tap.disconnect()
        
        current_boss = TOP_MVP
        current_boss_type = 'MVP'
        await cycle()
    elif is_in('buttons/update-button'):
        while is_in('buttons/update-button'):
            await tap.update()
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

        current_boss = TOP_MVP
        current_boss_type = 'MVP'
        await cycle()
class Button:
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


        await save_image("current-screen.png")
        counter = counter + 1
        current_screen = cv2.imread('current-screen.png')
        # await asyncio.sleep(0.2)

        # if counter % 2 == 0:
        await check_for_banners('current-screen.png')

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

# Create an instance of the Button Class
tap = Button()

# Return True or False whether the "location" variable is in the current screen
def is_in(location):

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
    
# Return True or False whether the "boss_name" variable is in the current screen
def locate_boss(boss_name):

    filename = '-'.join(boss_name.lower().split()) + ".png"
    screen = cv2.imread(f"images/boss-sidebar/{filename}")

    # Convert the images to grayscale
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

    # Find the image in the big image
    try:
        result = cv2.matchTemplate(current_gray, screen_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if the image was found
        if max_val > 0.9:
            return True
        else:
            return False
    except Exception as e:
        print(f"An exception occurred in locate_boss: {str(e)}")

        

async def go_to_mvp_tab():
    global current_screen
    if is_in('screens/battle-result-screen'):
        await tap.close_battle_results()

    while not is_in('screens/mvp-tab-screen'):
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

async def capture_battle_results(boss, boss_image):
    global counter, current_screen

    filename = '-'.join(boss.lower().split())
    find_count = 0
    while True:
        if await check_game_restarted():

            swipe_count = 0

            if current_boss_type == 'MVP':
                await reset_bosses(TOP_MVP)
                print('MVP tab is reached', flush=True)
            elif current_boss_type == 'MINI':
                await reset_bosses(TOP_MINI)
                print('MINI tab is reached', flush=True)

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
    # Crop the image
    cropped_image = current_screen[130:410, 80:890]
    downscaled_image = cv2.resize(cropped_image, (700, 242), interpolation=cv2.INTER_AREA)
    cv2.imwrite('battle-results.png', downscaled_image)
    counter = counter + 1

    with open('battle-results.png', "rb") as image_file:
        timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
        try:
            await channel_boss_deaths.send(f"{emoji_id[boss]} **{boss}** ***was slain!*** *{timestamp}*", file=discord.File(image_file))
        except Exception as e:
            print("wew i failed connecting to discord to send deadpics", flush=True)
            print(f"An exception occurred: {str(e)}")

    while is_in('screens/battle-result-screen'):
        print(f'im in capture_battle_results and I sent battle result of {boss} to discord. I am closing now', flush=True)
        await tap.close_battle_results()

async def close_mvp_screen():
    while True:
        if is_in('screens/mvp-screen'):
            await tap.close()
        elif is_in('screens/map-screen'):
            await tap.close_map()
        else:
            break

async def check_game_restarted():
    if is_in('screens/map-screen'):
        await tap.close_map()
    if is_in('screens/kingdom-pass-screen'):
        await tap.close_kpass()
        
    if is_in('buttons/unhide-icons-button'):
        print(f'hey i reached check_game_restarted haha {current_boss_type} : {current_boss}', flush=True)
        if current_boss_type == 'MVP':
            await go_to_mvp_tab()
            print('MVP tab is reached', flush=True)
        elif current_boss_type == 'MINI':
            await go_to_mini_tab()
            print('MINI tab is reached', flush=True)
        return True
    return False

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

async def get_previous_y(boss_image, boss):
    global counter, current_screen, driver

    await save_image("current-screen.png")
    counter = counter + 1
    current_screen = cv2.imread('current-screen.png')

    # Convert the images to grayscale
    button_gray = cv2.cvtColor(boss_image, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_screen, cv2.COLOR_BGR2GRAY)

    # Find the button in the big image
    result = cv2.matchTemplate(current_gray, button_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the button was found
    if max_val > 0.8:
        # Get the coordinates of the button in the big image
        top_left = max_loc
        bottom_right = (top_left[0] + boss_image.shape[1], top_left[1] + boss_image.shape[0])

        y = random.randint(top_left[1], bottom_right[1])
        return y
        
    else:
        print(f"{boss} is not found in the image")

async def scan_mvps():
    global current_boss, current_boss_type, previous_boss
    if current_boss in mvps:
        for i, boss in enumerate(mvps):
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

                # Check if it's the last item
                if i == len(mvps) - 1:
                    # Handle the last item
                    current_boss = TOP_MINI
                    current_boss_type = 'MINI'
                else:
                    # Get the next item
                    current_boss = list(mvps.keys())[i + 1]

                previous_boss = boss

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

                # Check if it's the last item
                if i == len(minis) - 1:
                    # Handle the last item
                    current_boss = TOP_MVP
                    current_boss_type = 'MVP'
                else:
                    # Get the next item
                    current_boss = list(minis.keys())[i + 1]
                
                previous_boss = boss


intents = discord.Intents.default()

# Create a Discord client
client = discord.Client(intents=intents)

# Set the ID of the Discord channel to send messages to
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

    TOP_MVP = "Phreeoni"
    TOP_MINI = "Eclipse"
    
    counter = 0
    await save_image("current-screen.png")
    counter = counter + 1
    print(f"(initial) Count = {counter}", flush=True)

    current_screen = cv2.imread('current-screen.png')
    
    current_boss = TOP_MVP
    current_boss_type = 'MVP'

    await cycle()

async def cycle():
    while True:
        await go_to_mvp_tab() #
        await reset_bosses(TOP_MVP) #
        await scan_mvps()
        await close_mvp_screen()
        await go_to_mini_tab() #
        await reset_bosses(TOP_MINI) #
        await scan_minis()
        await close_mvp_screen() #

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