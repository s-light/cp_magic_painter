# cp_magic_painter - Malen mit Licht
POV (Persistance Of Vision) Zauberstab

![Zauberstab (CAD)](hw/case/case_assembly_screenshots/overview.png)
![Zauberstab Photo](docu/magic_painter%20final.jpg)

https://github.com/s-light/cp_magic_painter/assets/1340319/28aa995e-11ee-43ee-a761-ba1665ddfda5


## documentation
have a look at [the documentation](https://s-light.github.io/cp_magic_painter/docu/)

Wichtige Dokumentations-Seiten:
- [Firmware Aktualisieren](https://s-light.github.io/cp_magic_painter/docu/update_firmware/de.html)
- [Bilder Vorbereiten](https://s-light.github.io/cp_magic_painter/docu/prepare_images/de.html)
- [Bedienung](https://s-light.github.io/cp_magic_painter/docu/usage/de.html)


## origin
this project / Workshop was first created for the [`Make Your School MakerFestival 2023`](https://www.makeyourschool.de/maker-festival/)

it is based on these two excellent Adafruit tutorials:
- [circuitpython painter](https://learn.adafruit.com/circuitpython-painter)
- [clue light paintstick](https://learn.adafruit.com/clue-light-paintstick)


## needed circuitpython libraries

- nonblocking_serialinput
- adafruit_lis3dh
- adafruit_pioasm
- adafruit_debouncer
- adafruit_pixelbuf
- adafruit_neopxl8
- adafruit_dotstar
- adafruit_ticks
- neopixel
- adafruit_msa3xx
- adafruit_bus_device
- ansi_escape_code
- adafruit_fancyled
- adafruit_imageload
- adafruit_register


## HW
have a look in [hw/](./hw/)

- uC: [Adafruit QT Py S3](https://learn.adafruit.com/adafruit-qt-py-esp32-s3/)
- sensor: [Adafruit LIS3DH Triple-Axis Accelerometer Breakout](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/overview)
- LEDs: APA102 / Dotstar ([z.B. this one](https://www.adafruit.com/product/2241) - we need 36Pixel (25cm))