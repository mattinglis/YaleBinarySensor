# YaleBinarySensor
Yale Smart Alarms Binary Door Sensors for Homeassistant

Add to config/custom_components/yalebinarysensor

Need to add the following to your configuration.yaml

~~~text
binary_sensor:
  - platform: yalebinary
    username: <YALE USERNAME>
    password: <YALE PASSWORD>
~~~
  
it will add binary sensors for all your door/window contacts

e.g. binary_sensor.back_door
