import random
import cv2
import asyncio
from connections.driver_connect import establish_appium_connection

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