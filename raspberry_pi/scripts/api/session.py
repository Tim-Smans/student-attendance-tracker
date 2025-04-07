
from api.client import get
from utils.device_utils import get_device_identifier


def get_active_session():
  current_device = get_current_device()

  if current_device is None:
    return None
  
  active_session = get("roomdevices/" + current_device["id"] + "/active_session")

  return active_session.json()



def get_current_device():
  this_device = get("roomdevices/device_identifier/" + get_device_identifier())
  return this_device


get_active_session()