import cv2 as cv
import numpy as np
import subprocess
import pyautogui

def swipe_basketball_into_hoop(basketball_x, basketball_y, hoop_x, hoop_y):
    # Implement the swipe action to move the basketball into the hoop
    # Adjust the coordinates and perform the appropriate mouse actions
    # Example code using pyautogui:
    pyautogui.moveTo(basketball_x, basketball_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(hoop_x, hoop_y, duration=0.2)
    pyautogui.mouseUp()

def perform_other_action():
    # Implement the logic for the condition when the basketball is not close enough to the hoop
    # Add your custom code here
    # For example, you can print a message or perform a different action
    print("Basketball is not close enough to the hoop. Performing other action...")

# Define the swipe threshold distance (adjust as needed)
threshold = 60

# Define the URL of the web page
url = 'https://www.facebook.com/gaming/play/800772590062226/?source=www_homepage_shortcut'

# Launch Chrome using subprocess with zoom option
chrome_cmd = [
    "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe",
    "--log-level=3",
    f"--user-data-dir=C:\\Users\\AVAYB\\AppData\\Local\\Google\\Chrome Beta\\User Data",
    "--force-device-scale-factor=1.33",  # Add 33% zoom
    url
]
subprocess.Popen(chrome_cmd)

# Create a loop to continuously capture and process frames in real-time
while True:
    # Take a screenshot of the web page
    screenshot_path = 'screenshot.png'
    pyautogui.screenshot(screenshot_path,)

    # Load the main image and the template images
    main_image = cv.imread(screenshot_path)
    hoop_template = cv.imread("./hoop.jpg", 0)  # Load as grayscale
    basketball_template = cv.imread("./basketball.jpg", 0)  # Load as grayscale

    # Convert the main image to grayscale
    gray_main = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY,)

    # Perform template matching for hoop
    hoop_result = cv.matchTemplate(gray_main, hoop_template, cv.TM_CCOEFF_NORMED)
    hoop_threshold = 0.8
    hoop_locations = np.where(hoop_result >= hoop_threshold)

    # Perform template matching for basketball
    basketball_result = cv.matchTemplate(gray_main, basketball_template, cv.TM_CCOEFF_NORMED)
    basketball_threshold = 0.8
    basketball_locations = np.where(basketball_result >= basketball_threshold)

    # Get hoop center coordinates
    hoop_height = hoop_template.shape[0]  # Retrieve height only

    # Find the center of the basketball and hoop
    if len(hoop_locations[0]) > 0 and len(basketball_locations[0]) > 0:
        hoop_x = hoop_locations[1][0] + hoop_template.shape[1] // 2
        hoop_y = hoop_locations[0][0] + hoop_template.shape[0] // 2

        basketball_x = basketball_locations[1][0] + basketball_template.shape[1] // 2
        basketball_y = basketball_locations[0][0] + basketball_template.shape[0] // 2

        # Display the main image with bounding boxes
        for basketball_loc in zip(*basketball_locations[::-1]):
            cv.rectangle(main_image, basketball_loc, (basketball_loc[0] + basketball_template.shape[1], basketball_loc[1] + basketball_template.shape[0]), (0, 255, 0), 2)

        for hoop_loc in zip(*hoop_locations[::-1]):
            cv.rectangle(main_image, hoop_loc, (hoop_loc[0] + hoop_template.shape[1], hoop_loc[1] + hoop_height), (0, 255, 0), 2)

        cv.imshow('Template Matching Result', main_image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # Perform the click action on the basketball
        pyautogui.click(basketball_x, basketball_y , 1, 1)
        pyautogui.dragTo(hoop_x, hoop_y , 1, button='left')
        pyautogui.mouseUp()

    else:
        perform_other_action()  # Call your custom logic if basketball and hoop are not found

# Close the OpenCV window
cv.destroyAllWindows()
