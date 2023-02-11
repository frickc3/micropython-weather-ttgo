import network
import json
import time
import configs.config as settings

def connect():
   wlan_sta = network.WLAN(network.STA_IF)
   if wlan_sta.isconnected():
       return wlan_sta
   #wlan_sta.disconnect()
   wlan_sta.active(True)
   ssid = settings.wifi['ssid']
   spwd = settings.wifi['password']
   if wlan_sta.isconnected():
      return wlan_sta
   print('Trying to connect to %s...' % ssid)

   try:
      wlan_sta.connect(ssid, spwd)
   except OSError as error:
      print(error)
      return
        
   for retry in range(100):
      connected = wlan_sta.isconnected()
      if connected:
         break
      time.sleep(0.10)
      print('.', end='')
   if connected:
      print('\nConnected. Network config: ', wlan_sta.ifconfig())
        
   else:
      print('\nFailed. Not Connected to: ' + ssid)
      return None
   return wlan_sta   
