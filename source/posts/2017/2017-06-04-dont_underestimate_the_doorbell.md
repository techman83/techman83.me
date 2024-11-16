Don't underestimate the... Doorbell
===================================

```{post} 2017-06-04
:tags: programming, arduino, esp8266, hardware
:category: Hardware
```

A while ago I needed a doorbell, so I [hacked](https://github.com/techman83/hackydoorbell) one together using a Raspberry Pi I had laying around. It was a temporary fix while I got around to building an Arduino based replacement. A month or so ago the SD card croaked, so it was time.

I have a bunch of [Wemos D1 Mini's](https://wiki.wemos.cc/products:d1:d1_mini) which would be the basis of my project and I also wanted it to play an actual sound file, so I'd ordered an [I2S](https://en.wikipedia.org/wiki/I%C2%B2S) based [Class-D Mono Amplifier](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview) from Adafruit.


```{thumbnail} /assets/posts/2017-06-04-dont_underestimate_the_doorbell/doorbell.jpg
:title: Breadboard
:width: 600
:class: figure center
```

I'd stumbled across a [project](https://github.com/bbx10/SFX-I2S-web-trigger) using the same amplifier and they'd used a permissive license, so I didn't actually end up needing to write much of my own code. I however spent a number of hours trying to figure out why the sound was extremely distorted, only to note that I'd hooked up `LRC` to `TX` instead of `D4`.

## Pin Connections

<table class="table">
    <thead>
        <tr>
            <th>Adafruit I2S DAC</th>
            <th>ESP8266</th>
            <th>D1 Mini</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>LRC</td>
            <td>GPIO2/TX1 LRCK</td>
            <td>D4</td>
            <td>Left/Right audio</td>
        </tr>
        <tr>
            <td>BCLK</td>
            <td>GPIO15 BCLK</td>
            <td>D8</td>
            <td>I2S Clock</td>
        </tr>
        <tr>
            <td>DIN</td>
            <td>GPIO03/RX0 DATA</td>
            <td>RX</td>
            <td>I2S Data</td>
        </tr>
        <tr>
            <td>GAIN</td>
            <td>n/c</td>
            <td>n/c</td>
            <td>9 dB gain</td>
        </tr>
        <tr>
            <td>SD</td>
            <td>n/c</td>
            <td>n/c</td>
            <td>Stereo average</td>
        </tr>
        <tr>
            <td>GND</td>
            <td>GND</td>
            <td>GND</td>
            <td>Ground</td>
        </tr>
        <tr>
            <td>Vin</td>
            <td>BAT</td>
            <td>5V</td>
            <td>3.3/5V power</td>
        </tr>
    </tbody>
</table>

I've broken the Non Blocking WAV player into a separate library [ESP8266-wavplay](https://github.com/techman83/esp8266-wavplay) along with one for the Wav SPIFFS reader [ESP8266-wavspiffs](https://github.com/techman83/esp8266-wavspiffs), which makes for a tiny amount of code to produce a functional doorbell.

```c++
#include "ESP8266Wavplay.h"

void setup()
{
  Serial.begin(115200);
  Serial.println("Booting");
  // Set D3 as Switch pin
  pinMode(D3, INPUT_PULLUP);

  // Setup WavPlay
  wavSetup();
  showDir();
}

void loop() {
  int state = digitalRead(D3);

  if ( state == 0 && !wavPlaying()) {
    wavStartPlaying("/doorbell.wav");
  }

  // WavPlay is non blocking, we need to call it to make
  // sure it keeps playing until file end.
  wavLoop();
}
```

You can find the project [here](https://github.com/techman83/esp8266-doorbell) and is already laid out as a [PlatformIO](http://platformio.org/) project. If you've yet to come across PlatformIO and you do a lot with Arduino, it takes a lot of the pain out of things like managing dependencies, custom libraries, platform independent code etc.

Happy Hacking and  may the force be with you.

```{youtube} SCnJ7anb-r0
:width: 100%
```
