# cp_magic_painter

Malen mit Licht - POV (Persistance Of Vision) Zauberstab

![Zauberstab (CAD)](hw/case/case_assembly_screenshots/overview.png)

## Build
have a look at the [build documentation](docu/workshop_DE.md)

## Usage

The Software has 2 Modes:
- Lamp
- POV (Persistence Of Vision) 

you can switch between these two with the small button on the controller `D0`

### Mode: Lamp 
the three touch buttons are used to change settings:
- top: brighntess higher
- center: brighntess lower
- bottom: brighntess minimum
<!-- - top: higher
- center: lower 
- bottom: settings mode [brightness | color] (currently fixed to brighntess) -->

currently to change the color connect to a computer and open the [`config.py`](config.py) file found on the `CIRCUITPY` *usb-stick* device.
there you find a line 
```python
        "base_color": CHSV(0.7),  # only specifiing Hue. purple
```
define the base color hue as following:
![hue color](docu/color_hue.svg)
save the file and 
make sure you use the *safe remove* option of your system before resetting the board or unplugging!

### Mode: POV

~~the three touch buttons are used to change settings:~~
- ~~top: higher~~
- ~~center: lower~~
- ~~bottom: settings mode (brightness | color)~~

touch buttons currently deactivated as they have falls positiv during shaking..



## HW

-   APA102 ('Dotstar') LED-Pixel-Strip 144Pixel/m - **36 LEDs**
-   [Adafruit QT Py ESP32-S3](https://www.adafruit.com/product/5426) as controller
-   [Adafruit LIS3DH Triple-Axis Accelerometer](https://www.adafruit.com/product/2809)
-   USB PowerBank [PNY PowerPack T2600 (P-B-2600-1-K01-RL)](https://www.pny.com/File%20Library/Support/PNY%20Products/Resource%20Center/PowerPacks/PowerPack_T-Series_web.pdf) i got some old stock - nice form factor: 101,9 mm x 24 mm x 22,3 mm
  sadly its getting hard to get these Lithium-ion cylindrical cell packs..
-   some [lasercut wood](hw/case/export/case_parts_mod.svg) for the case..

for more details have a look at the [order_overview.pdf](hw/order__overview.pdf)

## project state

next steps
- get lasercut wood
- test assembly & fit
- tweak design
- extend & tweak firmware


## origin
this project / Workshop was first created for the [`Make Your School MakerFestival 2023`](https://www.makeyourschool.de/maker-festival/)

it is based on these two excellent Adafruit tutorials:
- [circuitpython painter](https://learn.adafruit.com/circuitpython-painter)
- [clue light paintstick](https://learn.adafruit.com/clue-light-paintstick)