# Homeassitant  Event Ambilight
Python script to send RGB value events to your HA instance

# Ambilight Script
This script allows you to create an ambilight effect using Tuya bulbs and obtain RGB values from your current desktop colors. The script captures the screen, calculates the average RGB values of specified regions, and sends the RGB values to your HA instance via events.

## Prerequisites
Before running the script, make sure you have the following:

Python 3.x installed on your system.

Required Python packages: numpy, mss, keyboard, and requests. You can install them by running the following command:

```
pip install numpy mss keyboard requests
```

## Usage
1. Clone the repository or download the script to your local machine.

2. Open a terminal or command prompt and navigate to the directory where the script is located.

3. Run the script using the following command:

```
python ambilight.py --event-api-url <event_api_url> --ha-token <ha_token> --offset <offset_value>
```

- `event_api_url`: The Event API URL for your HA instance.

Example:
```
--event-api-url http://192.168.1.20:8123/api/events/
```

- `ha_token`: Your HA token for authentication.
- `offset_value`: The offset value for region placement. Adjust this value to customize the ambilight effect.

4. Press the `^` key to stop the script and exit.


## HA config:

create a HA automation and forward the values of the event to your bulps:
Example for the left bulp:

```
alias: Ambilight left
description: ""
trigger:
  - platform: event
    event_type: ambi
condition: []
action:
  - service: light.turn_on
    entity_id: light.pybilight_left
    data_template:
      rgb_color:
        - "{{ trigger.event.data.average_rgb_l[2] }}"
        - "{{ trigger.event.data.average_rgb_l[1] }}"
        - "{{ trigger.event.data.average_rgb_l[0] }}"
mode: single
```


## Acknowledgements

This script utilizes the following Python packages:

- `numpy`: Used for numerical operations and calculations.
- `mss`: Used for screen capturing and retrieving RGB values.
- `keyboard`: Used for detecting key presses to control the script.
- `requests`: Used for making HTTP requests to the Tuya Event API.


## Disclaimer

Please note that this script may have limitations and may not provide the same level of accuracy and performance as dedicated ambilight hardware. Use it at your own risk and discretion.
Make sure to comply with the terms and conditions of the Tuya API and any applicable regulations when using this script.
