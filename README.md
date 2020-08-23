# YaleBinarySensor
Yale Smart Alarms Binary Door Sensors for Homeassistant

Add to config/custom_components/yalebinarysensor

Need to add the following to your configuration.yaml

~~~text
binary_sensor:
  - platform: yalebinary
    username: <YALE USERNAME>
    password: <YALE PASSWORD>
    additional_sensors: True
~~~
  
it will add binary sensors for all your yale system components, if you only want door/window contacts set additional_sensors : False

Adds sensors to your system e.g. pulls in additional information e.g. battery state and temper information

e.g. binary_sensor.back_door

All credit to the homeassistant devs and the following without which it would not be possible
https://github.com/domwillcode/yale-smart-alarm-client
