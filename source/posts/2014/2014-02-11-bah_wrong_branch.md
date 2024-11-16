Git: Bah, wrong branch!
=======================

```{post} 2014-02-11
:tags: programming, git
:category: Programming
:author: techman83
```

I love git, it's a really great tool. However no matter how used I get to my workflows I eventually end up commiting something into the wrong branch!

And although I tend to use a custom bash shell called [git-sh](https://github.com/rtomayko/git-sh) with a full colour prompt, with all the relevant information:

```bash
master u=!dev-home>
```

I somehow still manage to commit in the wrong place. So after doing it again today I figured I'd use some git functionality to resolve it.

Ahh time to write some code.

```bash
master u=!dev-home> tee somescript.pl
!#/usr/bin/perl
!#/usr/bin/perl


print "I'm a script...\n"
print "I'm a script...\n"

master u=!dev-home> add somescript.pl
master u=!dev-home *> commit somescript.pl -m 'somescript added'
[master 8f922af] somescript added
 1 file changed, 3 insertions(+)
  create mode 100644 somescript.p
```

Bah, I commited to the wrong branch.. Again! I know, how 'bout I cherry pick that commit into the branch I wanted.

```bash
master u+1!dev-home> checkout dev
Switched to branch 'dev'

dev!dev-home> cherry-pick 8f922af
[dev aeb40b7] somescript added
 1 file changed, 3 insertions(+)
  create mode 100644 somescript.p
```

Now it's in the right place!

```bash
dev!dev-home> show
commit aeb40b782a53c73e6cc2b4b4f87074b026d7e6c2
Author: Leon Wright <leon.wright@imdexlimited.com>
Date:   Tue Feb 11 15:11:01 2014 +0800

    somescript added

    diff --git a/somescript.pl b/somescript.pl
    new file mode 100644
    index 0000000..6145323
    --- /dev/null
    +++ b/somescript.pl
    @@ -0,0 +1,3 @@
    +!#/usr/bin/perl
    +
    +print "I'm a script...\n"
```

Hmm, but master has the commit that I don't want in it. Good thing I hadn't pushed that to my remote repository

```bash
master u+1!dev-home> git reset --hard origin/master
HEAD is now at 3761131 test xml stuffs
```

Normality restored!
