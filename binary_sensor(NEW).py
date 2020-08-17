"""Component for interacting with the Yale Smart Alarm System API Binary Sensors"""
import logging

import voluptuous as vol
from yalesmartalarmclient.client import (
    AuthenticationError,
    YaleSmartAlarmClient,
)


from homeassistant.const import (
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
)

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from datetime import timedelta

CONF_AREA_ID = "area_id"

DEFAULT_NAME = "Yale Smart Alarm"

DEFAULT_AREA_ID = "1"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

YALE_DOOR_CONTACT_STATE_CLOSED = "closed"
YALE_DOOR_CONTACT_STATE_OPEN = "open"
YALE_DOOR_CONTACT_STATE_TAMPER = "tamper"
YALE_DOOR_CONTACT_STATE_UNKNOWN = "unknown"
YALE_DOOR_CONTACT_STATE_EMPTY = ""

_ENDPOINT_DEVICES_STATUS = "/api/panel/device_status/"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_AREA_ID, default=DEFAULT_AREA_ID): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the alarm platform."""
    name = config[CONF_NAME]
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    area_id = config[CONF_AREA_ID]

    try:
        client = YaleSmartAlarmClient(username, password, area_id)
    except AuthenticationError:
        _LOGGER.error
        ("Authentication failed. Check credentials")
        return
    
    object_status = client._get_authenticated(_ENDPOINT_DEVICES_STATUS);

    for object in object_status['data']:
        add_entities([YaleBinarySensor2(hass, client, object['name'],object['type'].replace('device_type.',''),object)], True)
        
class YaleBinarySensor2(Entity):
    """Implementation of a Yale binary sensor."""
    
    def __init__(self, hass, client, device_name, device_type, yale_object):
        """Initialize the sensor."""
        self.device_name = device_name
        self.client = client
        self.yale_object = yale_object
        self.device_type = device_type
        self._is_on = False
    
    @property
    def name(self):
        """return the name"""
        return self.device_name
        
    @property
    def is_on(self):
        return self._is_on
    
    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        attribs = {}
        attribs['area'] = self.yale_object['area']
        attribs['no'] = self.yale_object['no']
        attribs['type'] = self.device_type
        attribs['status1'] = self.yale_object['status1']
        attribs['bypass'] = self.yale_object['bypass']
        attribs['rssi'] = self.yale_object['rssi']
        attribs['type_no'] = self.yale_object['type_no']
        return attribs

    @property
    def state(self):
        """Return the state of the sensor."""
        state = self.yale_object["status1"]
        
        if "device_status.dc_close" in state:
            self._is_on = False
            return YALE_DOOR_CONTACT_STATE_CLOSED
        elif "device_status.dc_open" in state:
            self._is_on = True
            return YALE_DOOR_CONTACT_STATE_OPEN
        elif "device_status.tamper_open" in state:
            self._is_on = True
            return YALE_DOOR_CONTACT_STATE_TAMPER
        elif not state:
            self._is_on = False
            return YALE_DOOR_CONTACT_STATE_EMPTY
        else:
            self._is_on = False
            _LOGGER.error("Unknown State:"+str(self.yale_object["status1"]))
            return self.yale_object["status1"]
   
        
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update sensor data."""
        temp_object = self.client._get_authenticated(_ENDPOINT_DEVICES_STATUS)
        for object in temp_object['data']:
            if(object['name'] == self.device_name):
                self.yale_object = object
                break
     
    
