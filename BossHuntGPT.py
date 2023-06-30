from appium import webdriver
import os
import time
import cv2
import random
import discord
from discord import Intents
import asyncio
import datetime
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from fuzzywuzzy import fuzz

# This is for the Appium Connection
desired_caps = {
    "platformName": "Android",
    "deviceName": "Android Emulator",
    "autoGrantPermissions": False,
    "udid": "emulator-5554", # Change this with device name found in "adb devices" cmd
    "noReset": True
}

# Set the banner text to monitor for
banner_texts = [   
    "Storm Dragon w"
    "Orc Disaster w" 
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
    'Storm Dragon w': 'Storm Dragon',
    'Orc Disaster w': 'Orc Disaster',
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

# Define a dictionary for the boss status
boss_status = {
    0: 'Longer Time',
    1: 'Short Time',
    2: 'Refreshing Soon',
    3: 'Appeared'
}

# Define a dictionary for the bosses and their status
boss = {
    'Storm Dragon': 0,
    'Orc Disaster': 0,
    'Mistress': 0,
    'Phreeoni': 0,
    'Kraken': 0,
    'Eddga': 0,
    'Maya': 0,
    'Orc Hero': 0,
    'Pharaoh': 0,
    'Orc Lord': 0,
    'Amon Ra': 0,
    'Doppelganger': 0,
    'Overseer of Time': 0,
    'Morroc': 0,
    'Lost Dragon': 0,
    'Tao Gunka': 0,
    'Fallen Bishop': 0,
    'Lord of the Dead': 0,
    'Eclipse': 0,
    'Dragon Fly': 0,
    'Mastering': 0,
    'Ghostring': 0,
    'Toad': 0,
    'King Dramoh': 0,
    'Deviling': 0,
    'Angeling': 0,
    'Dark Priest': 0,
    'Vagabond Wolf': 0,
    'Chimera': 0,
    'Mysteltainn': 0,
    'Ogretooth': 0,
    'Necromancer': 0,
    'Naght Sieger': 0,
    'Coelacanth': 0,
}

# Load status images
longer_time_img = cv2.imread('lookup/longer-time.png')
short_time_img = cv2.imread('lookup/short-time.png')
refreshing_soon_img = cv2.imread('lookup/refreshing-soon.png')
appeared_img = cv2.imread('lookup/appeared.png')

boss_status_img = [longer_time_img, short_time_img, refreshing_soon_img, appeared_img]

# Set the Discord bot token
bot_token = "MTA4ODg1MTE1NjA4NTc4NDU4Nw.GRVcFc.rlcjEZihHK62zwMZxOvN1-ZGpCHwgB0k115Jik"

intents = discord.Intents.default()

# Create a Discord client
client = discord.Client(intents=intents)



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

def check_in_image(small, big):
    
    # Convert the images to grayscale
    small_gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    big_gray = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)

    # Find the small image in the big image
    result = cv2.matchTemplate(big_gray, small_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the small image was found
    if max_val > 0.8:
        # Get the coordinates of the small image in the big image
        top_left = max_loc
        bottom_right = (top_left[0] + small.shape[1] + 100, top_left[1] + small.shape[0])

        # Crop the area around the small image
        cropped_image = big[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Save the cropped image to disk
        cv2.imwrite('cropped_image.png', cropped_image)

        # Check if any of the global images are found in the cropped image
        for i, status in enumerate(boss_status_img):

            status_result = cv2.matchTemplate(cropped_image, status, cv2.TM_CCOEFF_NORMED)
            global_min_val, status_max_val, global_min_loc, global_max_loc = cv2.minMaxLoc(status_result)
            if status_max_val > 0.8:
                # The global image was found in the cropped image
                return boss_status[i]
                
                
    else:
        return "Image lookup failed!"

def swipeUp(start_y, end_y, duration):
    global driver
    start_x = random.randint(155, 420)
    end_x = start_x + random.randint(1,10)
    duration = 500
    driver.swipe(start_x, start_y, end_x, end_y, duration)

def save_image(screenshot_filename):
    global driver
    screenshot_filepath = os.path.join(os.getcwd(), screenshot_filename)
    driver.save_screenshot(screenshot_filepath)

def check_for_changes(boss_lookup, boss_group_filename, initialize):

    boss_group_img = cv2.imread(boss_group_filename)
    message_text = "" # initialize an empty string to store messages
    
    for boss_name in boss_lookup:
        filename = '-'.join(boss_name.lower().split()) + ".png"
        old_boss_status = boss_status[boss[boss_name]]
        boss_img = cv2.imread(f"lookup/{filename}")
        new_boss_status = check_in_image(boss_img, boss_group_img)

        if initialize == True:
            if new_boss_status == boss_status[0]:
                boss[boss_name] = 0
                message_text += f"```diff\n- {boss_name} : {boss_status[0]}\n```"
            elif new_boss_status == boss_status[1]:
                boss[boss_name] = 1
                message_text += f"```diff\n- {boss_name} : {boss_status[1]}\n```"
            elif new_boss_status == boss_status[2]:
                boss[boss_name] = 2
                message_text += f"```diff\n- {boss_name} : {boss_status[2]}\n```"
            elif new_boss_status == boss_status[3]:
                boss[boss_name] = 3
                message_text += f"```diff\n+ {boss_name} : {boss_status[3]}\n```"
            else:
                break

        if (new_boss_status != old_boss_status) and initialize == False:
            if new_boss_status == boss_status[0]:
                message_text += f"```diff\n- {boss_name} was killed!\n```" # add message to the string
                boss[boss_name] = 0
            elif new_boss_status == boss_status[1]:
                #message_text += f"{boss_name} will spawn within 30 minutes!\n" # add message to the string
                boss[boss_name] = 1
            elif new_boss_status == boss_status[2]:
                #message_text += f"{boss_name} will spawn within 15 minutes!\n" # add message to the string
                boss[boss_name] = 2
            elif new_boss_status == boss_status[3]:
                message_text += f"```diff\n+ {boss_name} appeared!\n```" # add message to the string
                boss[boss_name] = 3
            else:
                break    
            
    # Return the string containing all messages
    return message_text


def check_for_banners(filename):
    global last_detection_time, driver
    message_text = ""

    # Open the captured screenshot using the PIL module
    with Image.open(filename) as screenshot:

        # Pre-Process the Image Object
        # image = screenshot.resize((screenshot.width * 3, screenshot.height * 3))
        image = preprocess_image(screenshot)


        # Extract text from the image using Tesseract 
        try:
            extracted_text = pytesseract.image_to_string(image, config="--psm 6")
            print(extracted_text)
        except pytesseract.TesseractError as e:
            print(f"Error: {e}")
            extracted_text = ""

        # Check if the banner text is present in the extracted text
        for banner_text in banner_texts:
            ratio = fuzz.partial_ratio(extracted_text, banner_text)
            if ratio >= 85:
                # Calculate the time since the last detection
                time_since_last_detection = datetime.datetime.now() - last_detection_time

                # Only send a notification if enough time has elapsed since the last detection
                if time_since_last_detection > datetime.timedelta(seconds=10):
                    # Update the last detection time
                    last_detection_time = datetime.datetime.now()
    
                    # Generate message sent to discord
                    message_text += f"```\n {banner_lookup[banner_text]} will be spawning soon! Warriors, charge!\n```"
                    banner_close_x = random.randint(710, 720)
                    banner_close_y = random.randint(96, 110)
                    driver.tap([(banner_close_x, banner_close_y)])
                    # Break out of the loop once a banner text is detected and a message is sent
                    break
            
            ratio = fuzz.partial_ratio(extracted_text, 'Adventurer')
            if ratio >= 90:
                banner_close_x = random.randint(710, 720)
                banner_close_y = random.randint(96, 110)
                driver.tap([(banner_close_x, banner_close_y)])
                break

    return message_text

def check_cycle(initialize):
    global message_text, driver
    message_text = ""

    # Open MVP/Mini Screen
    bh_button_x = random.randint(595, 625)
    bh_button_y = random.randint(75, 100)
    driver.tap([(bh_button_x, bh_button_y)])

    time.sleep(0.5)
    save_image("mvp1-4.png")
    message_text += check_for_changes(['Lord of the Dead', 'Fallen Bishop', 'Tao Gunka', 'Lost Dragon'], 'mvp1-4.png', initialize)
    message_text += check_for_banners("mvp1-4.png")
    print(message_text, flush=True)

    swipeUp(185, 445, 500) # start_y, end_y, duration
    time.sleep(0.2)
    save_image("mvp5-8.png")
    message_text += check_for_changes(['Morroc', 'Overseer of Time', 'Doppelganger', 'Amon Ra'], 'mvp5-8.png', initialize)
    print(message_text, flush=True)

    swipeUp(185, 400, 500)
    time.sleep(0.2)
    save_image("mvp9-12.png")
    message_text += check_for_changes(['Orc Lord', 'Pharaoh', 'Orc Hero', 'Maya'], 'mvp9-12.png', initialize)
    message_text += check_for_banners("mvp9-12.png")
    print(message_text, flush=True)

    swipeUp(185, 429.3, 200)
    time.sleep(0.2)
    save_image("mvp13-16.png")
    message_text += check_for_changes(['Eddga', 'Kraken', 'Phreeoni', 'Mistress'], 'mvp13-16.png', initialize)
    print(message_text, flush=True)

    # Switch to Mini Tab
    mini_button_x = random.randint(205, 275)
    mini_button_y = random.randint(85, 108)
    driver.tap([(mini_button_x, mini_button_y)])

    time.sleep(0.5)
    save_image("mini1-4.png")
    message_text += check_for_changes(['Coelacanth', 'Naght Sieger', 'Necromancer', 'Ogretooth'], 'mini1-4.png', initialize)
    message_text += check_for_banners("mini1-4.png")
    print(message_text, flush=True)

    swipeUp(185, 445, 500)
    time.sleep(0.2)
    save_image("mini5-8.png")
    message_text += check_for_changes(['Mysteltainn', 'Chimera', 'Vagabond Wolf', 'Dark Priest'], 'mini5-8.png', initialize)
    print(message_text, flush=True)

    swipeUp(185, 400, 500)
    time.sleep(0.2)
    save_image("mini9-12.png")
    message_text += check_for_changes(['Angeling', 'Deviling', 'King Dramoh', 'Toad'], 'mini9-12.png', initialize)
    print(message_text, flush=True)

    swipeUp(185, 429.3, 200)
    time.sleep(0.2)
    save_image("mini13-16.png")
    message_text += check_for_changes(['Ghostring', 'Mastering', 'Dragon Fly', 'Eclipse'], 'mini13-16.png', initialize)
    message_text += check_for_banners("mini13-16.png")
    print(message_text, flush=True)

    # Switch back to MVP Tab
    mvp_button_x = random.randint(108, 180)
    mvp_button_y = random.randint(86, 110)
    driver.tap([(mvp_button_x, mvp_button_y)])

    time.sleep(0.5)

    # Close the MVP/Mini Screen
    close_button_x = random.randint(860, 890)
    close_button_y = random.randint(30, 58)
    driver.tap([(close_button_x, close_button_y)])

    return message_text

# Event listener for when the bot is ready
@client.event
async def on_ready():
    
    global driver, message_text, last_detection_time

    # Keep track of the last time the banner text was detected
    last_detection_time = datetime.datetime.now() - datetime.timedelta(seconds=3)

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    # Set the ID of the Discord channel to send messages to
    channel_id = 1087725231159914606

    # Find the channel to send messages to
    channel = client.get_channel(channel_id)

    #await channel.send("Boss Hunt Bulagan Bot is now live...!")
    check_cycle(True)
    #await channel.send(message_text)

    while True:
        check_cycle(False)
        if message_text != "":
            await channel.send(message_text)

        check_interval = random.randint(1,3)
        print(check_interval)
        # Wait for the specified interval before checking again
        await asyncio.sleep(check_interval)
    
    #driver.quit()
    
# Start the bot
client.run(bot_token)

