from nad import NadMixer
import os
import anvil.server

mixer = NadMixer()

@anvil.server.callable("amp.reset")
def reset():
  mixer.on_start()

@anvil.server.callable("amp.get_volume")
def get_volume():
  return mixer.get_volume()

@anvil.server.callable("amp.set_volume")
def set_volume(vol):
  mixer._power_device_on()
  return mixer.set_volume(vol)


@anvil.server.callable("amp.set_power_on")
def set_power_on(on):
  if on:
    mixer._power_device_on()
  else:
    mixer._power_device_off()
  return mixer._ask_device('Main.Power') == "On"

@anvil.server.callable("amp.get_power_on")
def get_power_on():
  return mixer._ask_device('Main.Power') == "On"

@anvil.server.callable("amp.set_source")
def set_source(src):
  if mixer._check_and_set('Main.Source', src):
    return src
  else:
    return mixer._ask_device('Main.Source')

@anvil.server.callable("amp.get_source")
def get_source():
  return mixer._ask_device('Main.Source')


anvil.server.connect(os.getenv("UPLINK_KEY"))

mixer.on_start()

anvil.server.wait_forever()
