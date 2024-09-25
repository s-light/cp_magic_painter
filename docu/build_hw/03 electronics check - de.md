# Elektronik vorbereiten

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

## Beschleunigungssensor

![sensor](<./03 test electronics/20230923_001833.jpg>)

im bild oben rechts ist die Power-LED sichtbar.
Unten auf der Platine ist `VIN` aufgedruckt.
auf dieser Seite möchte das Kabel eingesteckt werden.
schon mal etwas vorsichtig umbiegen wie im bild hilft später für die Positionierung.

# Elektronik testen

## LED-Streifen

nun den led-streifen an den controller anschließen
dabei auf die beschriftungen auf der Controller-Platine achten:

-   rotes Kabel auf +5V
-   schwarzes Kabel auf GND
-   Blaue sollte bei SCK (clock) landen
-   Grün bei MOSI (Master Out Slave In)

## Beschleunigungssensor

das freie Ende nun in den Controller stecken

## Buttons

falls vorhanden:
die drei Buttons kommen in die Pins mit den Namen

-   `SDA` unterster Button
-   `SCL` mittlerer Button
-   `TX` oberer Button

## alle bauteile zusammengesteckt

![alle bauteile zusammengesteckt](<./03 test electronics/20230923_011729.jpg>)

> vorsichtig das sich keine metallteile berühren!

nun Vorsichtig die Powerbank anstecken..
Schalter einschalten
und....

![und einmal testen](<./03 test electronics/20230923_011821.jpg>)
und alles geht :-)

## Test

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