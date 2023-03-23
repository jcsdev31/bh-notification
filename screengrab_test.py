import win32gui
from PIL import ImageGrab, Image, ImageOps, ImageFilter

# Set the window title to capture
window_title = "Ready Player 1"


# Get the window handle
hwnd = win32gui.FindWindow(None, window_title)

# Get the dimensions of the client area of the window
client_rect = win32gui.GetClientRect(hwnd)

# Convert the client area dimensions to screen coordinates
left, top = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
right, bottom = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))

# Take a screenshot of the whole window
screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

screenshot.save("images/pc_raw.png")