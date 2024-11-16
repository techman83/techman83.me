The Hugs Strike Back!
=====================

```{post} 2018-01-29
:tags: programming, arduino, linuxconfau, lca2018
:category: Hardware
```

Another year, another amazing [Linux Conf AU](http://lca2018.org)! Based on feedback from LCA2017, I was definitely going to iterate on the hug detector. In that time the [ESP32](http://esp32.net/) platform has begun to mature and because I like challenges, decided to use a board I received days prior to leaving for the conference and really only flashed with blink.

Other project parameters I'd set myself include:

 * Beyond component testing, nothing developed before the conference
 * Conference badge as an integral part of the design
 * Operational by main conference opening (Wednesday)

With that in mind, I set about beginning my work Monday evening. As I presented a [talk](./2018-01-22-come_on_do_you_want_your_mods_to_live_forever.md) earlier in the day and quite a broken sleep the night before, I was feeling a little weary. I spent several hours fighting with [I²C](https://en.wikipedia.org/wiki/I%C2%B2C) on the [Wemos Lolin32_Lite](https://wiki.wemos.cc/products:lolin32:lolin32_lite), which didn't seem to have pins mapped for the purpose and discussed GPIO Muxing which I was unfamiliar with. After deciding I was way too tired for that I figured I'd sleep and see if I could find one of the Hardware guys to chat about it in the morning.

I chatted to @jonoxer, who pointed me in the direction of @geekscape and then I bumped into @wolfeidau who I'd spoken to at the open hardware miniconf. He understood exactly what I was trying to do and was more than happy to impart his knowledge and learnings about working with I²C, in particular on the ESP32 platform. Turns out that any pin that isn't an input only pin, can be re-assigned using the Wire library. He also pointed me in the direction of an [I²C scanner](https://github.com/CCHS-Melbourne/iotuz-esp32-hardware/blob/master/Software/Snippets/i2cScanTest/i2cScanTest.ino) used in the previous years hardware project as an excellent starting place.

Feeling motivated after dinner, I headed back to the  accommodation and begun work. With a deadline of 2130 before I'd fall back to the ESP8266 based [D1 Mini](https://wiki.wemos.cc/products:d1:d1_mini), which I was far more familiar with; I got started. Now getting the pins remapped was pretty easy as it turns out:

```c++
#include <Wire.h>

void setup()
{
    Wire.begin(16, 17) // SDA, SCL
    // Do things
}
```

However whilst I could get it to work via the I²C scanner, I couldn't get it to work via the library for the [vl6180x lidar distance sensor](https://learn.adafruit.com/adafruit-vl6180x-time-of-flight-micro-lidar-distance-sensor-breakout) that was a core part of how I would be detecting hugs this year. After a lot of flaffing around, I figured it's a conference [and hacking the library is always an option](https://github.com/techman83/vl6180x-arduino/commit/42f625008d277f2d2f184dc32ec94dede9f2005a).

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/tweet01.png
:title: @Techman83
:width: 500
:class: figure center
```

That success spurred me on to tidying up the code to work with the range finder. I also got pretty sidetracked trying to get the [FreePixel](https://www.freetronics.com.au/products/freepixel-addressable-rgb-led-module) modules working and struggled with different libraries not actually producing the results I expected. As it was getting late I decided to use the built in LED as the visual indicator of a successful hug.

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/badge.jpg
:title: Badge
:width: 600
:class: figure center
```

The only thing that was left to do was hook up the JST Connector (pictured below) and test the battery.

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/jst2mm1.jpg
:title: JST Connector
:width: 400
:class: figure center
```

Unfortunately whilst I distinctly remember checking the polarity of the connector...

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/tweet02.png
:title: @developerjack
:width: 500
:class: figure center
```

Fortunately I didn't destroy it, but the charge circuitry is limited to about 100mA now. As opposed to the 500mA it is actually capable of. Seeing as it was 1am Wednesday morning, I had a functioning hug detector, and nearly destroyed it.. I decided to call it done and go to bed.

I headed off to the conference in the morning and after remembering to start the backend infrastructure (a python script running in screen..)

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/tweet03.png
:title: @Techman83
:width: 500
:class: figure center
```

Over the course of a couple of days it got a thorough testing and generated a lot of conversations. Which in reality was part of my motivation to build it. Oddly enough, having wires hanging off your badge is a wonderful conversation starter!

All was not well by Friday morning, the hug detector worked a little too well and I ended up getting filtered from twitter searches.

So overall I'm really happy with how well everything worked, the wonderful interactions it encouraged during the conference and all the wonderful people who made it extra fun. I think for the next iteration I'd like to:

 * Create a dedicated hug bot account, to ensure I don't bust my own account and also make it easier for people to filter out the hugs
 * Randomise the tweet content a bit more so that I don't trip up the filters
 * Incorporate better hug feedback, be it lights or an OLED display of some sort
 * Some better handling of I²C issues, I got around it this year mostly by regular power cycling which isn't ideal.

And as a final note, after the conference I went to [Brain Candy Live](http://www.braincandylive.com/), hosted by @donttrythis and @tweetsauce. My ticket included a 'Meet and Greet', however in my very exhausted and excited state forgot to look at the camera when getting a photo with them!

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/meetgreet.jpg
:title: Meeting Michael + Adam
:width: 600
:class: figure center
```
All was not lost though, as I did get a hug out of both Michael and Adam! Which was the best way to finish an entirely spectacular week!

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/tweet04.png
:title: @Techman83
:width: 500
:class: figure center
```

```{thumbnail} /assets/posts/2018-01-29-hug_detector_v2/tweet05.png
:title: @Techman83
:width: 500
:class: figure center
```
