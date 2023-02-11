import network
import gc
import json
import utime as time
from machine import Pin, SPI, RTC
import st7789
import weather.do_connect as do_connect
from   weather.urllib import urequest as request
import weather.configs.tft_config as tft_config
import weather.configs.config as settings
import weather.fonts.vga1_8x16 as font1
import weather.fonts.vga1_16x16 as font

tft = tft_config.config(0)

def center_text(text, x=0, y=0):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() // 2 - length // 2 * font.WIDTH + x,
        tft.height() // 2 - font.HEIGHT + y,
        st7789.WHITE,
        st7789.BLACK)

def main():
    tft.init()
    tft.rotation(1)
    tft.fill(st7789.BLACK)
    print("In weather.main.py")
    wlan = do_connect.connect()
    if wlan:
       if wlan.isconnected() == False:
          print("not connected") 
          tft.png('weather/images.image_no_internet.png', 0, 0, st7789.SLOW)
          center_text("Not connected to WiFi")
          return
    else:
       tft.png('weather/images/image_no_internet.png', 0, 0, st7789.SLOW)
       center_text("Not connected to WiFi")
       return

    tft.fill(st7789.BLACK)
    tft.png('weather/images/weather-64.png', 0, 0, st7789.SLOW)
    #tft.text(font,jbody['station_name'],80,0)

    station_id = settings.tempest['station-id']
    token = settings.tempest['token']
    url = "http://swd.weatherflow.com/swd/rest/observations/station/"+station_id+"?token="+token

    while True:
        r = request.urlopen(url)
        body = r.read()
        r.close()
        jbody = json.loads(body)

        center_text(jbody['public_name'], x=30, y=-50)    
        loc = time.localtime()
        dte = "{:02n}".format(loc[1])+"/"+"{:02n}".format(loc[2])+"/"+"{:02n}".format(loc[0])
        tft.text(font,dte,80,26)
        tme = "{:02n}".format(loc[3])+":"+"{:02n}".format(loc[4])  #+":"+"{:02n}".format(loc[5])
        tft.text(font,tme,114,46)                                   # was 84,64
    
        tft.text(font,"Temp:",0,70)
        obs = jbody['obs']

        tmp = obs[0]['air_temperature']
        far = int(tmp * 1.8 + 32)
        far = str(far)+jbody['station_units']['units_temp']
        tft.text(font,far,150,70)

        hum = str(obs[0]['relative_humidity'])
        tft.text(font,"Humidity:",0,86)
        tft.text(font,hum,150,86)
    
        wav = str(obs[0]['wind_avg'])
        tft.text(font,"Wind Avg:",0,100)
        tft.text(font,wav,150,100)    
        gc.collect()
        time.sleep(300)							# sleep for 5 minutes
    
if __name__ == "__main__":
   main()
