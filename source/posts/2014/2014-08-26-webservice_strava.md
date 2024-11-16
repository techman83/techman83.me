Title: WebService::Strava - A Strava API Perl Client
====================================================

```{post} 2014-08-26
:tags: programming, perl, cycling, strava
:category: Programming
:author: techman83
```

Being a Cyclist and a Geek, I like to track things. Being a Sys Admin and a Programmer I also like this to happen in the most efficient manner possible. Insert [Strava](http://strava.com), which is basically a social networking platform for cyclists/runners/swimmers (I believe they're adding more as well). Strava has an App for recording things or you can use any app or device that can output in one of the supported formats (GPX, FIT and TCX).

Strava also has an [api](http://strava.github.io) and I was looking to implement something for [Exobrain](https://metacpan.org/pod/Exobrain) and noted that whilst a Perl Client existed for Strava it was based on V2 API which no longer exists. So after pinging the Maintainer I was given co-maint on [WebService::Strava](https://metacpan.org/pod/WebService::Strava) and today I was able to release my first module on cpan!

Probably the easiest way to install it is via cpanm + local::lib. On an Ubuntu distro you can grab these with apt:

```bash
sudo apt-get install cpanminus liblocal-lib-perl
```

Then you can configure local::lib

```bash
$ perl -Mlocal::lib >> ~/.bashrc
$ eval $(perl -Mlocal::lib)
```

then install WebService::Strava

```bash
cpanm WebService::Strava
```

Once installed you will need to configure your authentication. After setting up your application in your [profile](https://www.strava.com/settings/api) just run

```bash
strava --setup
```

It will ask for your client id, client secret and authenticate with the strava api. You will have to copy the 'code' from the url bar as Strava doesn't yet implement 'urn:ietf:wg:oauth:2.0:oob' standard for scripts.

After which you can in a few lines access most of the API

```perl
#!/usr/env/perl
use strict;
use feature qw(say);
use WebService::Strava;

my $strava = WebService::Strava->new();

my $athlete = $strava->athlete();

say $athlete->firstname;
```

Which outputs

```bash
leon@bofh-sider:/tmp$ perl strava.pl
Leon
```

Full documentation is available on [cpan](https://metacpan.org/pod/WebService::Strava) and you can contribute, ask for features on [github](https://github.com/techman83/WebService-Strava3)
