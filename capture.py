import mss
import cv2
import numpy as np
import threading
from PIL import ImageGrab

def capture_region():
    # Create a monitor dictionary for the specified region
    
    with mss.mss() as sct:
        # Capture the specified region as a numpy array
        screenshot = np.array(sct.grab(monitor))
        
        # # Display the screenshot using OpenCV
        # cv2.imshow("Screen Capture", screenshot)
        
        # # Break the loop when the 'q' key is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     pass

    return screenshot

def get_region():
    # Set the path to the reference image
    reference_image_path = "sample.png"

    # Load the reference image in BGR format
    reference_img = cv2.imread(reference_image_path)

    # Convert the reference image to RGB
    reference_img_rgb = cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB)

    # Capture the current screen
    screen = np.array(ImageGrab.grab())
    
    # Match the reference image in the current screen
    result = cv2.matchTemplate(screen, reference_img_rgb, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    # Get the coordinates of the matched region
    top_left = max_loc
    h, w, _ = reference_img.shape

    top = top_left[1] + h
    left = top_left[0]
    width = w
    height = 540
    
    return {"top": top, "left":left, "width":width, "height":height}

monitor = get_region()
print(f"MONITOR: {monitor}")

# # Create a thread for the capture function
# capture_thread = threading.Thread(target=capture_region, args=())

# # Start the thread to continuously capture the specified region
# capture_thread.start()
    