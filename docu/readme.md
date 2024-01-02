# cp_magic_painter - Malen mit Licht 
POV (Persistance Of Vision) Zauberstab

![Zauberstab (CAD)](hw/case/case_assembly_screenshots/overview.png)
![Zauberstab Photo](./magic_painter%20final.jpg)
<video src="mode%20POVPainter.mp4" controls title="Mode: POVPainter - showing two different images"></video>

currently some documentation is only written in german.
an english version will follow hopefully some day...




## Build / Zusammenbauen
- [build documentation / Bau-Workshop Anleitung (DE)](workshop_DE.md)

## Prepare / Vorbereitungen

- [prepare images / Bilder Vorbereiten (DE)](prepare_images/de.md)
- [update firmware / Software Aktualisiseren (DE)](update_firmware/de.md)

## Usage / Benutzung

- [Benutzung (DE)](usage/de.md)
- [usage (EN)](usage/en.md)



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
- firmware
  - fix touch buttons
  - add gesture recognition
- docu
  - how to update firmware
  - how to change configuration
