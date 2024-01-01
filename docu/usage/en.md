## Usage

The Software has 2 Modes:
- Lamp
- POV (Persistence Of Vision) 

you can switch between these two with the small button on the controller `D0`

TODO: this is outdated! currently only the german version is up to date. sorry!

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
        "color_range": {
            "min": CHSV(0.08),
            "max": CHSV(0.12),
        },
```
define the base color hue as following:  
![hue color](color_hue.svg)  
(the shown example is a warm orange-yellow range..)
save the file and 
make sure you use the *safe remove* option of your system before resetting the board or unplugging!

### Mode: POV

~~the three touch buttons are used to change settings:~~
- ~~top: higher~~
- ~~center: lower~~
- ~~bottom: settings mode (brightness, color)~~

touch buttons currently deactivated as they have falls positiv during shaking..
