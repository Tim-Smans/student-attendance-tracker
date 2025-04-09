
from .client import get
from ..utils.device_utils import get_device_identifier


def get_active_session():
  
  """
  Fetches the active session for the device where this function is ran.

  Returns:
    dict: The active session object if one exists, otherwise None.
  """
  current_device = get_current_device()

  if current_device is None:
    return None
  
  active_session = get("roomdevices/" + current_device["id"] + "/active_session")
  print(active_session.json())
  return active_session.json()

def  is_active_session():

  """
  Checks if there is an active session on the device where this function is ran.

  Returns:
    bool: True if there is an active session, False otherwise.
  """
  current_device = get_current_device()

  if current_device is None:
    return None
  
  active_session = get("roomdevices/" + current_device["id"] + "/active_session")
  return active_session.status_code == 200



def get_current_device():
  """
  Fetches the current device object based on the device's identifier.

  Returns:
    dict: The device object if the device exists, otherwise None.
  """
  this_device = get("roomdevices/device_identifier/" + get_device_identifier())
  print(this_device.json())
  return this_device.json()


