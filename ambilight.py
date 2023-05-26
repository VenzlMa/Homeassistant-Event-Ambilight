import json
import argparse
import numpy as np
import mss
import mss.tools
import keyboard
import requests

# Create argument parser
parser = argparse.ArgumentParser(description='Ambilight Script')
parser.add_argument('--event-api-url', type=str, help='Event API URL')
parser.add_argument('--ha-token', type=str, help='HA Token')
parser.add_argument('--offset', type=int, help='Offset value')

# Parse the command-line arguments
args = parser.parse_args()

# Assign the provided values
EVENT_API_URL = args.event_api_url
HA_TOKEN = args.ha_token
offset = args.offset

HEADERS = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(HA_TOKEN)}

def calculate_average_rgb(rgb_array):
     return np.ceil(np.mean(rgb_array, axis=0)).astype(np.uint8)  # Use np.uint8 for integer values

def fire_event(event_type, payload):

    payload_str = json.dumps(payload)
    requests.post(EVENT_API_URL + event_type, headers=HEADERS, data=payload_str)

def getRgbArray(region):
    # Capture the screenshot of the region
    screenshot = np.array(sct.grab(region))
    # Get the RGB values from the captured image
    rgb_values = screenshot[:, :, :3]
    # Reshape the RGB values to a flat array
    rgb_array = np.reshape(rgb_values, (-1, 3))
    return rgb_array   

def get_screen_resolution():
    with mss.mss() as sct:
        monitor_info = sct.monitors[1]  # Assuming the target monitor is index 1
        resolution = {
            "width": monitor_info["width"],
            "height": monitor_info["height"]
        }
        return resolution

def get_region_coordinates(region_width, region_height, screen_width, screen_height, top_offset, left_offset):
    region = {
        "top": top_offset,
        "left": left_offset,
        "width": region_width,
        "height": region_height
    }
    return region

# Calculate screen resolution
screen_resolution = get_screen_resolution()
screen_width = screen_resolution["width"]
screen_height = screen_resolution["height"]

# Calculate region size and offsets
region_width = screen_width // 2  # Teilen Sie die Breite des Bildschirms durch 2
region_height = screen_height
top_offset = offset  # Der obere Teil beginnt am oberen Rand des Bildschirms

# Calculate left and right offsets
left_offset_l = offset  # Linker Teil beginnt am linken Rand des Bildschirms
left_offset_r = region_width - offset  # Rechter Teil beginnt nach der Breite des linken Teils

# Create the regions
region_l = get_region_coordinates(region_width, region_height, screen_width, screen_height, top_offset, left_offset_l)
region_r = get_region_coordinates(region_width, region_height, screen_width, screen_height, top_offset, left_offset_r)


# Create a flag to control the loop
running = True

def on_key_press(event):
    global running
    if event.name == '^':
        running = False

keyboard.on_press(on_key_press)

# Start the loop
with mss.mss() as sct:
    while running:

        # Calculate the average RGB values
        average_rgb_l = calculate_average_rgb(getRgbArray(region_l))
        #average_rgb_m = calculate_average_rgb(getRgbArray(region_m))
        average_rgb_r = calculate_average_rgb(getRgbArray(region_r))


        # Construct the payload with the average_rgb values
        payload = {
            "average_rgb_l": average_rgb_l.tolist(),
            #"average_rgb_m": average_rgb_m.tolist(),
            "average_rgb_r": average_rgb_r.tolist(),
        }

        # Fire the event with the payload
        fire_event("ambi", payload)

# Release the keyboard listener
keyboard.unhook_all()
