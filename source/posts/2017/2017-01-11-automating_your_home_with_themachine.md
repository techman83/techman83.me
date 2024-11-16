Automating your home with 'themachine'
======================================

```{post} 2017-01-11
:tags: homeautomation, machinelearning, programming, python
:category: Hardware
:author: techman83
```

There will be more posts to come, but for some time I have been playing around with home automation. One of the things I really wanted to do was utilise some form of machine learning to make decisions about when I wanted the Shed's Airconditioning or the wall fan turned on. I could have utilised rules in my [OpenHAB](http://www.openhab.org/) based home automation system, however I'd already gotten reasonably creative with those and wanted a challenge.

I've been learning about machine learning for a while, in particular however it was this post on [Stackoverflow](http://stackoverflow.com/questions/30991592/support-vector-machine-in-python-using-libsvm-example-of-features) and sentdex's [Machine Learning with Python](https://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v) playlist that really helped me find a solution that appeared to fit what I was trying to do.

Using a couple of [DHT22](http://www.freetronics.com.au/products/humidity-and-temperature-sensor-module) sensor modules attached to [Wemos D1 Mini](https://www.wemos.cc/product/d1-mini.html), I was readily collecting Temperature data into OpenHAB.

```{thumbnail} /assets/posts/2017-01-11-automating_themachine/dht11_wemos_d1.jpg
:title: Wemos D1 + DHT22 shown with USB Key for Scale
:width: 600
:class: figure center
```

I settled on a Support Vector Machine algorithm as it seemed to best fit my dataset of "inTemperatur,inHumidity,outTemperature,outHumidity" and my decisions required being On or Off. The following video does an excellent job of explaining SVM.

https://www.youtube.com/watch?v=mA5nwGoRAOo

I ended up writing a Python script that listens for change and learn events on the [MQTT](https://en.wikipedia.org/wiki/MQTT) message bus which ties my home automation system together. OpenHAB fires change events when I'm present in the shed and fires learn events when I manually turn on AC or Fan on. If 'themachine' predicts a positive result greater than 95% certaintity it will fire back to a channel that OpenHAB has a switch sitting on to receive the event.

Example log of an event:

```
2017-01-11 20:53:52,721 INFO     I'm 97.92% sure you wanted the shedFan on. shed,26.70,58.10,21.00,81.30
```

You can find out more information about how to implement something similar on [GitHub](https://github.com/techman83/habsvm-themachine), it's MIT licensed so feel free to use the code how you'd like.

I have to admit, the first time it came on by itself was a little weird. I was standing on a stepladder doing some terminating in my rack (yes of course I have a full height network rack in my shed), thinking that it had gotten a little warm *AC Turns on* ... "woah". Skynet however is a long way off, well at least in my little home automation setup.
