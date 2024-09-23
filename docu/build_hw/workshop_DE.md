# MYS MakerFestival Workshop

<style>
    html, body {
        background: hsl(270,100%,10%);
        color: hsl(40, 100%, 50%);
        font-size: 1.2em;
    }
    img {
        max-width: 90vw;
        max-height: 60vh;
    }
</style>

Workshop Anleitung

## Holz Vorbereitung

![bausatz](<./01 prepare wood/20230914_130242.jpg>)

![alle einzelteile vorbereitet](<./01 prepare wood/20230914_131258.jpg>)

### Positionierungsstifte

Dann die Positionierung-Stifte vorbereiten.
die länge lässt sich mit dem Seitenschneider am besten an den Holz-Schichten abmessen und direkt schneiden.
![Positionierungsstifte](<./01 prepare wood/20230914_131637.jpg>)

### oben

nun die oberen Teile Zusammenleimen

> WICHTIG:
> Layer 1 & 2 werden miteinander verleimt.
> und Layer 3 & 4 werden miteinader verleimt.
> Allerdings möchten die Positionierungsstifte durch alle 4 Durchgehen..

![prepare wood - top layer glueing](<01 prepare wood/20240821_120350 case glue.jpg>)
![prepare wood - top layer glueing](<01 prepare wood/20240821_120355 case glue detail.jpg>)
![prepare wood - top layer glueing](<01 prepare wood/20240821_120938 case glue clamping.jpg>)

### unten

dann das gleiche spiel mit den unteren teilen
(drei layer)

![untere Teile Leimen](<./01 prepare wood/20230914_132658.jpg>)

### USB-Slide-In

hier werden wieder die jeweiligen zwei Layer mit einander verleimt -
die unteren beiden Layer und die Oberen beiden Layer.
diese beiden _Pakete_ werden dann später nur auf die Stifte aufgesteckt.

![einschub](<./01 prepare wood/20230914_132841.jpg>)

#### obere layer

![usb-einschub](<01 prepare wood/20240919_200016 case - usb slide in - bottom.jpg>)
![usb-einschub](<01 prepare wood/20240919_200023 case - usb slide in - top.jpg>)

#### untere layer

![usb-einschub](<01 prepare wood/20240919_200112 case - usb slide in - overview.jpg>)
![usb-einschub](<01 prepare wood/20240919_200351 case - usb slide in - parts glued.jpg>)

### zwischenstand

![zwischenstand](<./01 prepare wood/20230914_133349.jpg>)

### box

wenn die oberen und unteren teile fest sind kommt als letzter schritt die box:

![vorbereitung box](<./01 prepare wood/20230914_133451.jpg>)

mit hilfe der gummies auch die box leimen
hier darauf achten das diese rechtwinkelig ist.
![box leimen](<./01 prepare wood/20230914_133952.jpg>)

### Cover

> Falls Vorhanden

als letztes noch die _cover-layer_ miteinander verleimen..
dabei sehr sehr sorgfältig arbeiten so das die Holz-Stößel sich frei bewegen können...
![prepare wood - ](<01 prepare wood/20240821_131404 cover details buttons.jpg>)
![prepare wood - ](<01 prepare wood/20240821_131430 cover details buttons.jpg>)

## Elektronik vorbereiten

<!-- LED-Streifen
![LED-Streifen](<pictures/03 test electronics/20230913_132513_HDR.jpg>)
Controller
![Controller](<pictures/03 test electronics/20230916_224711.jpg>)
adapter
![adapter](<pictures/03 test electronics/20230917_012738.jpg>) -->

alle bauteile zurecht legen
![electronic parts](<./03 test electronics/20230922_181443.jpg>)

In den Fotos sind noch \*Touch-Buttons zu sehen.
Diese habe ich wegen unzuverlässigkeit raus genommen.

### Beschleunigungssensor

![sensor](<./03 test electronics/20230923_001833.jpg>)

im bild oben rechts ist die Power-LED sichtbar.
Unten auf der Platine ist `VIN` aufgedruckt.
auf dieser Seite möchte das Kabel eingesteckt werden.
schon mal etwas vorsichtig umbiegen wie im bild hilft später für die Positionierung.

## Elektronik testen

### LED-Streifen

nun den led-streifen an den controller anschließen
dabei auf die beschriftungen auf der Controller-Platine achten:

-   rotes Kabel auf +5V
-   schwarzes Kabel auf GND
-   Blaue sollte bei SCK (clock) landen
-   Grün bei MOSI (Master Out Slave In)

### Beschleunigungssensor

das freie Ende nun in den Controller stecken

### Buttons

falls vorhanden:
die drei Buttons kommen in die Pins mit den Namen

-   `SDA` unterster Button
-   `SCL` mittlerer Button
-   `TX` oberer Button

### alle bauteile zusammengesteckt

![alle bauteile zusammengesteckt](<./03 test electronics/20230923_011729.jpg>)

> vorsichtig das sich keine metallteile berühren!

nun Vorsichtig die Powerbank anstecken..
Schalter einschalten
und....

![und einmal testen](<./03 test electronics/20230923_011821.jpg>)
und alles geht :-)

### Test

-   erst sollte auf dem Controller die LED in verschiedenen Farben Leuchten.
-   dann der Streifen einen grünen _ladebalken_ anzeigen
-   dann einmal vorsichtig den Sensor in der Y-Achse schütteln
-   darauf hin sollte der Streifen flackern
-   dann den Taster D0 auf dem Controller drücken
-   dies schaltet in den Lampen modus um
-   nun leuchtet eine LED ganz am ende des Streifens
-   nun den längsten Draht / Button _oben_ mehrfach berühren
-   darauf hin sollten auf dem Streifen immer mehr LEDs an gehen / es wird heller
-   beim mittleren Button sollten diese wieder ausgehen / dunkler werden
-   beim untersten Button sollte die Helligkeit wieder auf minimum (1 LED) springen

damit sind alle Funktionen getestet.
→ Power-Schalter wieder ausschalten und Powerbank abziehen

→ Bauteile wieder auseinander stecken !!

## zusammen bauen Teil1

ein Stück Schrumpfschlauch auf Länge schneiden und bereit legen

### LED-streifen

als erstes den LED-Streifen so positionieren das alle LEDs herausschauen und dieser gut auf dem Holz aufliegt.

### Buttons

die Buttons in die Aussparung im Gehäuse legen und dann die obersten beiden Layer zusammen stecken.

### Sensor

die Sensor Platine von Unten auf dem oberen Ende des Stabes positionieren -
eventuell mit etwas Kleber dort fixieren.
das Kabel am Stab entlang durch das Loch nach oben führen (siehe auch nächstes Bild)

### Oberer Stab fertig Vorbereitet

Das ganze sollte nun so in etwa Ausschauen:
![build](<./04 build/20230915_124936.jpg>)

zum Schluss alle steck-elemente nach oben führen
![alle steck-elemente nach oben führen](<./04 build/20230915_125104.jpg>)

## zusammen bauen Teil2

nun werden wir den USB-Stecker und Power-Schalter im Mittleren Holz-Stück befestigen.
![usb slide-in mounting ](<04 build/20240919_200541 case - usb slide in - electronic in - top.jpg>)
![usb slide-in mounting ](<04 build/20240919_200558 case - usb slide in - electronic in - bottom.jpg>)
![usb slide-in mounting ](<04 build/20240919_200619 case - usb slide in - electronic in - side.jpg>)
![usb slide-in mounting ](<04 build/20240919_200709 case - usb slide in - electronic in - mounted - top.jpg>)
![usb slide-in mounting ](<04 build/20240919_200727 case - usb slide in - electronic in - mounted - bottom.jpg>)

## zusammen bauen Teil3

nun wird alles vereint

als erstes den controller vorsichtig hindurch fädeln
![controller einbau](<./04 build/20230915_125136.jpg>)

controller fertig durchgefädelt
![controller fertig durchgefädelt](<./04 build/20230915_125200.jpg>)

nun die steckverbindungen wieder achtsam zusammenfügen.
![fertig](<./04 build/20230915_125415.jpg>)

und dann den controller vorsichtig in den stab drücken
(am besten auf der USB-Buchse und gleichzeitig auf dem Sensor-Anschluss)

<!-- BILD einfügen -->

## zusammen bauen Teil4
nun noch von Unten zwei Muttern in die löcher einfügen

Wenn hier noch Zeit übrig ist kann gern aus dem Kuststoff oder Schrumpfschlauch eine Abdeckung ausgeschnitten werden. (siehe [_layer-4 cover_ Schnitt-Vorlage](./../../hw/case/export/case_layer-4_mod_small_cover.svg))
diese wird dann auch mit den Schrauben fixiert.

von Oben die Schrauben durchstecken und mit einem 1,5mm Imbus fest ziehen.
Somit ist das Mittlere Holz-Teil fixiert.

Fertig ist dein Zauberstab :-)
    
## Programmieren

<!-- TODO -->
....
schau mal in die documente:
- [verwendung](/docu/usage/de.md)
- [eigene bilder aufspielen](/docu/prepare_images/de.md)
- [software aktuallisieren](/docu/update_firmware/de.md)

