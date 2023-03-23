import pytesseract
import os
import time
import datetime
import requests
import json
from PIL import Image, ImageOps, ImageFilter

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/data/data/com.termux/files/usr/bin/tesseract"

# Set the banner text to monitor for
banner_texts = [    
    "Mistress will",    
    "Phreeoni will",    
    "Kraken will",    
    "Eddga will",    
    "Maya will",    
    "Orc Hero will",    
    "Pharaoh will",    
    "Orc Lord will",    
    "Amon Ra will",    
    "Doppelganger will",    
    "Overseer of Time",    
    "Morroc will",    
    "Lost Dragon will",    
    "Tao Gunka will",    
    "Fallen Bishop will",
    "Lord of the Dead will",
    "Eclipse will",
    "Dragon Fly will",
    "Mastering will",
    "Ghostring will",
    "Toad will",
    "King Dramoh will",
    "Deviling will",
    "Angeling will",
    "Dark Priest will",
    "Vagabond Wolf will",
    "Chimera will",
    "Mysteltainn will",
    "Ogretooth will",
    "Necromancer will",
    "Naght Sieger will",
    "Coelacanth will",]


# Set the Discord webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1088430658579333123/zNvkUs4BPl7jFhfCgG00H9dwAnPydUvJUTvyJSiffcnD484QHeUESNtpDAmV1jexGBMv"

# Set the interval in seconds to check the game screen
check_interval = 3

# Keep track of the last time the banner text was detected
last_detection_time = datetime.datetime.now() - datetime.timedelta(seconds=check_interval)

# Pre-Process Image for OCR
def preprocess_image(image):

    width, height = image.size # Get the width and height of the image
    
    left = width * 0.307
    right = width * 0.74
    top = height * 0.1852
    bottom = height * 0.23148
    
    region = (left, top, right, bottom)
    image = image.crop(region)
    # image = ImageOps.grayscale(image)
    # image = image.point(lambda x: 0 if x < 210 else 255)

    return image


# Loop indefinitely
while True:
    # Get the current time
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Capture a screenshot of the device screen using the screencap command
    os.system('screencap /storage/emulated/0/screenshot.png')

    # Open the captured screenshot using the PIL module
    with Image.open('/storage/emulated/0/screenshot.png') as screenshot:

        # Pre-Process the Image Object
        # image = screenshot.resize((screenshot.width * 3, screenshot.height * 3))
        image = preprocess_image(screenshot)

        image.save('/storage/emulated/0/screenshot_processed.png')


        # Extract text from the image using Tesseract 
        try:
            extracted_text = pytesseract.image_to_string(image, config="--psm 6")
            print(extracted_text)
        except pytesseract.TesseractError as e:
            print(f"Error: {e}")
            extracted_text = ""

        # Check if the banner text is present in the extracted text
        for banner_text in banner_texts:
            if banner_text in extracted_text:
                # Calculate the time since the last detection
                time_since_last_detection = datetime.datetime.now() - last_detection_time

                # Only send a notification if enough time has elapsed since the last detection
                if time_since_last_detection > datetime.timedelta(seconds=10):
                    # Update the last detection time
                    last_detection_time = datetime.datetime.now()
    
                    # Choose a message to send based on the detected banner text
                    if banner_text == "Mistress will":
                        message_text = "Mistress will be spawning soon! Warriors, charge!"
                    elif banner_text == "Phreeoni will":
                        message_text = "Phreeoni will be spawning soon! Warriors, charge!"
                    elif banner_text == "Kraken will":
                        message_text = "Kraken will be spawning soon! Warriors, charge!"
                    elif banner_text == "Eddga will":
                        message_text = "Eddga will be spawning soon! Warriors, charge!"
                    elif banner_text == "Maya will":
                        message_text = "Maya will be spawning soon! Warriors, charge!"
                    elif banner_text == "Orc Hero will":
                        message_text = "Orc Hero will be spawning soon! Warriors, charge!"
                    elif banner_text == "Pharaoh will":
                        message_text = "Pharaoh will be spawning soon! Warriors, charge!"
                    elif banner_text == "Orc Lord will":
                        message_text = "Orc Lord will be spawning soon! Warriors, charge!"
                    elif banner_text == "Amon Ra will":
                        message_text = "Amon Ra will be spawning soon! Warriors, charge!"
                    elif banner_text == "Doppelganger will":
                        message_text = "Doppelganger will be spawning soon! Warriors, charge!"
                    elif banner_text == "Overseer of Time":
                        message_text = "Overseer of Time will be spawning soon! Warriors, charge!"
                    elif banner_text == "Morroc will":
                        message_text = "Morroc will be spawning soon! Warriors, charge!"
                    elif banner_text == "Lost Dragon will":
                        message_text = "Lost Dragon will be spawning soon! Warriors, charge!"
                    elif banner_text == "Tao Gunka will":
                        message_text = "Tao Gunka will be spawning soon! Warriors, charge!"
                    elif banner_text == "Fallen Bishop will":
                        message_text = "Fallen Bishop will be spawning soon! Warriors, charge!"
                    elif banner_text == "Lord of the Dead will":
                        message_text = "Lord of the Dead will be spawning soon! Warriors, charge!"
                    elif banner_text == "Eclipse will":
                        message_text = "Eclipse will be spawning soon! Warriors, charge!"
                    elif banner_text == "Dragon Fly will":
                        message_text = "Dragon Fly will be spawning soon! Warriors, charge!"
                    elif banner_text == "Mastering will":
                        message_text = "Mastering will be spawning soon! Warriors, charge!"
                    elif banner_text == "Ghostring will":
                        message_text = "Ghostring will be spawning soon! Warriors, charge!"
                    elif banner_text == "Toad will":
                        message_text = "Toad will be spawning soon! Warriors, charge!"
                    elif banner_text == "King Dramoh will":
                        message_text = "King Dramoh will be spawning soon! Warriors, charge!"
                    elif banner_text == "Deviling will":
                        message_text = "Deviling will be spawning soon! Warriors, charge!"
                    elif banner_text == "Angeling will":
                        message_text = "Angeling will be spawning soon! Warriors, charge!"
                    elif banner_text == "Dark Priest will":
                        message_text = "Dark Priest will be spawning soon! Warriors, charge!"
                    elif banner_text == "Vagabond Wolf will":
                        message_text = "Vagabond Wolf will be spawning soon! Warriors, charge!"
                    elif banner_text == "Chimera will":
                        message_text = "Chimera will be spawning soon! Warriors, charge!"
                    elif banner_text == "Mysteltainn will":
                        message_text = "Mysteltainn will be spawning soon! Warriors, charge!"
                    elif banner_text == "Ogretooth will":
                        message_text = "Ogretooth will be spawning soon! Warriors, charge!"
                    elif banner_text == "Necromancer will":
                        message_text = "Necromancer will be spawning soon! Warriors, charge!"
                    elif banner_text == "Naght Sieger will":
                        message_text = "Naght Sieger will be spawning soon! Warriors, charge!"
                    elif banner_text == "Coelacanth will":
                        message_text = "Coelacanth will be spawning soon! Warriors, charge!"

                    # Create the Discord notification message
                    message = {
                        "content": f"{message_text} Announcement Banner Detected at:{current_time}"
                    }

                    # Send the notification to the Discord webhook
                    response = requests.post(discord_webhook_url, data=json.dumps(message), headers={"Content-Type": "application/json"})

                    # Check if the notification was sent successfully
                    if response.status_code == 204:
                        print(f"Notification sent at {current_time}")

                    # Break out of the loop once a banner text is detected and a message is sent
                    break

    # Wait for the specified interval before checking again
    time.sleep(check_interval)
