# MYS MakerFestival 2023

Workshop Anleitung

## Holz Vorbereitung

![bausatz](pictures/01%20prepare%20wood/20230914_130242.jpg)

![alle einzelteile vorbereitet](pictures/01%20prepare%20wood/20230914_131258.jpg)

Dann die Positionierung-Stifte vorbereiten.
die länge lässt sich mit dem Seitenschneider am besten an den Holz-Schichten abmessen und direkt schneiden.
![Positionierungsstifte](pictures/01%20prepare%20wood/20230914_131637.jpg)

nun die oberen Teile Zusammenleimen
![obere Teile leimen](pictures/01%20prepare%20wood/20230914_132415.jpg)

dann das gleiche spiel mit den unteren teilen
![untere Teile Leimen](pictures/01%20prepare%20wood/20230914_132658.jpg)

bei diesen Teilen werden nur Zwei Teile geklebt.
die unteren Teile bleiben Lose und werden dann später nur auf die Stifte aufgesteckt.
![einschub](pictures/01%20prepare%20wood/20230914_132841.jpg)

zwischenstand
![zwischenstand](pictures/01%20prepare%20wood/20230914_133349.jpg)

wenn die oberen und unteren teile fest sind kommt als letzter schritt die box:

![vorbereitung box](<pictures/01 prepare wood/20230914_133451.jpg>)

mit hilfe der gummies auch die box leimen
hier darauf achten das diese rechtwinkelig ist.
![box leimen](<pictures/01 prepare wood/20230914_133952.jpg>)

## Elektronik vorbereiten

<!-- LED-Streifen
![LED-Streifen](<pictures/03 test electronics/20230913_132513_HDR.jpg>)
Controller
![Controller](<pictures/03 test electronics/20230916_224711.jpg>)
adapter
![adapter](<pictures/03 test electronics/20230917_012738.jpg>) -->

alle bauteile zurecht legen
![electronic parts](<pictures/03 test electronics/20230922_181443.jpg>)

### Touch Buttons

![Enameled copper wire lengths](<pictures/02 solder electronics/20230915_122823_mod.png>)
bitte die lackierung mit feinem Schleifpapier (320) an beiden Enden entfernen:

-   Seite1 5mm
-   Seite2 40-50mm

vom Kupferband 3x 50mm Stücke abschneiden.
### Beschleunigungssensor

![sensor](<pictures/03 test electronics/20230923_001833.jpg>)
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

### Touch Buttons
die drei Buttons kommen in die Pins mit den Namen 
- `SDA` unterster Button
- `SCL` mittlerer Button
- `TX`  oberer Button

### alle bauteile zusammengesteckt
![alle bauteile zusammengesteckt](<pictures/03 test electronics/20230923_011729.jpg>) 

vorsichtig das sich keine metallteile berühren!

nun Vorsichtig die Powerbank anstecken..
Schalter einschalten
und....

![und einmal testen](<pictures/03 test electronics/20230923_011821.jpg>)
und alles geht :-)

Test: 
- erst sollte auf dem Controller die LED in verschiedenen Farben Leuchten.
- dann der Streifen einen grünen *ladebalken* anzeigen
- dann einmal vorsichtig den Sensor in der Y-Achse schütteln
- darauf hin sollte der Streifen flackern
- dann den Taster D0 auf dem Controller drücken
- dies schaltet in den Lampen modus um
- nun leuchtet eine LED ganz am ende des Streifens
- nun den längsten Draht / Button *oben* mehrfach berühren
- darauf hin sollten auf dem Streifen immer mehr LEDs an gehen / es wird heller
- beim mittleren Button sollten diese wieder ausgehen / dunkler werden
- beim untersten Button sollte die Helligkeit wieder auf minimum (1 LED) springen

damit sind alle Funktionen  getestet.
→ Power-Schalter wieder ausschalten und Powerbank abziehen

→ Bauteile wieder auseinander stecken !!
## zusammen bauen Teil1

ein Stück Schrumpfschlauch auf Länge schneiden und bereit legen
### LED-streifen
als erstes den LED-Streifen von unten durch das Loch im Oberen holz schieben bis alle LEDs herausschauen und dieser gut auf dem Holz aufliegt.

### Sensor
die Sensor platine von Unten auf dem oberen Ende des Stabes positionieren - eventuell mit etwas kleber dort fixieren.
das Kabel am Stab entlang durch das Loch nach oben führen (siehe auch nächstes Bild)

### Touch-Buttons
Nun die Kupfer-Klebe-Folie auf den Draht-Enden auf die Rückseite des Stabes auf das Sensor-Kabel Kleben.
Am besten dabei die Kupfer-Dräthe tendenziell unter dem Sensor-Kabel *verlegen*.

Es hilft hier von Oben während dessen schon den Schrumpfschlauch Stück für Stück über den Stab zu schieben.

### Oberer Stab fertig Vorbereitet

Das ganze sollte nun so in etwa Ausschauen:
![build](<pictures/04 build/20230915_124936.jpg>) 

zum Schluss alle steck-elemente nach oben führen
![alle steck-elemente nach oben führen](<pictures/04 build/20230915_125104.jpg>) 

## zusammen bauen Teil2

nun werden wir den USB-Stecker und Power-Schalter im Mittleren Holz-Stück befestigen.
##

## zusammen bauen Teil3
nun wird alles vereint

als erstes den controller vorsichtig hindurch fädeln
![controller einbau](<pictures/04 build/20230915_125136.jpg>) 

controller fertig durchgefädelt
![controller fertig durchgefädelt](<pictures/04 build/20230915_125200.jpg>)

nun die steckverbindungen wieder achtsam zusammenfügen.
![fertig](<pictures/04 build/20230915_125415.jpg>)

und dann den controller vorsichtig in den stab drücken
(am besten auf der USB-Buchse und gleichzeitig auf dem Sensor-Anschluss)

<!-- BILD einfügen -->

nun noch von Unten zwei Muttern in die löcher einfügen 

Wenn hier noch Zeit übrig ist kann gern aus dem Kuststoff oder Schrumpfschlauch eine Abdeckung ausgeschnitten werden. (siehe [*layer-4 cover* Schnitt-Vorlage](../hw/case/export/case_layer-4_mod_small_cover.svg))
diese wird dann auch mit den Schrauben fixiert.

von Oben die Schrauben durchstecken und mit einem 1,5mm Imbus fest ziehen.
Somit ist das Mittlere Holz-Teil fixiert.


