# micropython-weather-ttgo
MicroPython Tempest Weather display for LiLyGO_T-Display Code Repository

1. Build Micropython for LiLyGo_T-Display and load to device (git clone <b>https://github.com/Xinyuan-LilyGO/lilygo-micropython</b>).
2. ampy -p COMx put main.py
3. ampy -p COMx put weather-ttgo
4. Copy config_sample.py as config.py in configs directory.
5. Edit config.py add in WiFi SSID and Password and Tempest device token and station_id. 

Reset device (main.py will start weather/main.py if your boot.py calls main).

Enjoy. 
