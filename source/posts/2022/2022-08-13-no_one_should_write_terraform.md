No one should write Terraform
=============================

```{post} 2022-08-13
:tags: programming, terraform, devops
:category: Programming
```

Reflecting upon [zwischenzugs](https://zwischenzugs.com/) insightful and thought provoking article “[Who should write the Terraform?](https://zwischenzugs.com/2022/08/08/who-should-write-the-terraform/)”, the TL;DR conclusion I’ve come to is “No One”.

---

That’s a pretty simple statement for me to make from the outset, but stick with me and we can go on a journey. Having spent nearly two decades in roles ranging from a Technician fixing student laptops, Sys Admin working with a team managing the operations of a 24/7 Enterprise, being the sole developer building a hosted VoIP solution at a startup; To now working with dozens of software engineers and empowering them to work more efficiently. All of that and I’m a blue haired guy with opinions!


```{thumbnail} /assets/posts/2022-08-13-no_one_should_write_terraform/devops-engineer.webp
:title: Colleague: “What’s the difference between a Software Engineer and a DevOps Engineer”
:width: 300
:class: figure center
:show_caption: True
```

## The Problem
Over the years I’ve used many configuration automation tools. From my days working with Zenworks Configuration Management repackaging windows applications for corporate deployments, writing ansible maintaining Linux boxes, CloudFormation for deploying large swathes of AWS resources, or Terraform to tie resources together in a platform independent way. Regardless of which tool I’ve picked up, I’ve always come up against a fairly similar set of challenges.

```{thumbnail} /assets/posts/2022-08-13-no_one_should_write_terraform/box-of-devops.webp
:title: Look, He bought a box of DevOps!
:width: 500
:class: figure center
:show_caption: True
```

Now that comic[^cloud-guru] is very tongue in cheek and undersells what can be achieved when embracing DevOps as not just tooling, but as a fundamental way of working with technology. However it neatly sums up the common problem with all of the aforementioned tools, they are purely declarative. Each one of them does offer a domain specific way to introduce ways to be programmatic, but someone whose day-to-day is working on an application, is not going to have the bandwidth to learn a new tool just to create a bucket. Let alone understand the implications of those IAM binding copy/pasted from Stack Overflow resulting in a configuration making a bunch of private data publicly available.

So what’s the answer here? Do we abandon all these tools and go back to a world of Devs doing Dev things and Sys Admins being grumpy gatekeepers?

---

So I must confess, as someone with ADHD I often take things literally. For me, and I don’t mean this as a way of gate keeping or to look down upon someone whose a wizard in their tool of choice; because all those things take considerable skill to do well. But in my brain that was source controlled configuration and I always saw it as a stepping stone to true the end goal of using “Code” via a functional or OO language. Now this is not because I’m some opinionated developer. Rather, I grew up and spent the early part of my career hating programming. As time went on I realised not knowing how to program was holding me back as an Engineer, so I spent hundreds of hours teaching myself to do just that.

Getting back on track, in a former role we were leaning quite hard on CloudFormation. Even though we were only a team of two, we still faced challenges that I have encountered in bigger teams.

### Large Declarative Files
Ensuring a couple of thousand lines of YAML/JSON is correctly formatted, with the correct pieces in the right places is hard. That is before you want to start writing large sets of commands as your startup script!

Duplication of Effort
We were spending considerable time doing the same work over and over, which also meant as we got busy, changes were being left off a services due to being nested deep in a YAML files.

### Slow Feedback Loops
Changes meant applying updates, updates could be quite consuming. Especially if you made a typo or mistake, meaning you had to wait for some internal timeout. Too many times I just packed up for the day, because some change screwed up the stack and would be stuck for hours.

### Context Switching
It was very challenging to spend all day buried in some obscure Asterisk dial-plan issue, to then switch over to figuring out a tooling problem. Now that problem might impact someone with ADHD more so, it is still something everybody faces.

### Configuration vs Code Repositories
Due to the large amount of unrelated changes and commits that often come with purely declarative configuration, modules, environment files, permission control, and so on. There is a tendency to separate Configuration from Code. This leads to needing to go to multiple places to understand how your project is deployed, and can lead to configuration items being missed when code changes. Or if your team is really inefficient, developers working around the configuration problem and wedging it in code or a database table.

## The Solution
One day my boss at job[-1] came to me, having gone down a rabbit hole with Troposphere. For those not in the know, this is a library for generating valid CloudFormation via Python. This was it, finally I could do what the industry was talking about all over the place, I could start writing Infrastructure as Code!

In the following weeks I hyper-focused on solving the challenges that had really been frustrating me. I added AutoScaling, Load Balancers, logging sidecars by default, and way more. The core platform went from having some disparate tools for logging, to automatically getting it as I’d added it to the one of the other services that had a far greater need for centralised logging.

We slowly but surely spent less time managing an gargantuan collection of YAML files and instead found ways to optimise our workflows, increase our security, tighten up our IAM controls, and get back to focusing on the primary parts of jobs as being the only 2 developers in a fast growing startup.

---

When it was time to move on from that role, I happened to be pinged by an internal recruiter for a DevOps role that would involve bringing their Developers and the Platform on a journey towards more efficient processes, allowing to support the growth of E-Commerces version of the ‘Eternal September’ in March of 2020.

Now as part of that, I was switching from Amazon Web Services to Google Cloud. Troposphere being very much CloudFormation specific and noting that even AWS were starting to invest outside non-vendor specific tools, Terraform seamed like the obvious choice.

However when I went searching around for even something like Troposphere for GDM that was actively maintained, nothing. And then it hit me, I’d spent the better part of a decade thinking “Infrastructure as Code” was just that, using something like Python to automate infrastructure changes. I was in quite an existential crisis, as having experienced the burdens of purely declarative IaC, I didn’t know what to do!

---

At some point I stumbled across the right set of keywords, I found out that the industry had coined the term ‘CDK’ or Cloud Development Kit for the process of using Functional or OO programming languages that developers are already familiar with. So after talking it over with colleagues, vendors, and friends, I got a variety of opinions. Ranging from not really understanding the point, to outright suggesting it was too early to look at the CDK for Terraform, but most importantly support from my boss at the time, to come up with an MVP concept to get us going.

## Summary
It’s been a little over 12 months since I made that first commit, but since then we’ve gone from one type of “Stack” to several dozen. It’s performed > 5000 automated deployments, and has gone from something I envisioned wrapping up our MicroServices, to supporting all sorts of uses cases required from the developers. A moment that really stood out recently was a developer in their second or third week wanted experiment with a new service, and I didn’t even know they were building the configuration until they had a question! I answered and got back to the thing I was working on. I checked back later and their service was built, deployed, with a load balancer, auto-scaling, auto-healing, completely driven via GitHub Actions and no direct Involvement from Ops. The comment I got from them “Yeah, I was a bit confused for about a day, and then it all made sense”, which as someone who was less than a month at the company being able have a brand new service deployed into our test environment. It was likely quite refreshing for them and really rewarding for me.

In a future article I will delve into the specifics, but three things come to mind when I’ve talked about it with people who I have introduced the concept to

- **Fully Unit Tested IaC** — We can change any part of the code that generates our resulting configuration and be confident that what we give to Terraform to apply is correct.
- **State Files** — As we don’t need to try and reduce the amount of Stacks we manage, breaking them up into discrete stacks is extremely easy. Any state problems don’t create any wide scale impacts to operations.
- **Provider Versions and Availability** — The tools ensure the provider is available with the correct version, migrating them is just part of the tools responsibility. As we can thoroughly test these pathways, applying them wider is as simple as releasing a new version of our internal CDK wrapper.

## The Real TL;DR
In the whole time I’ve been working with Terraform I’ve written < 100 lines of HCL. No one should write Terraform, not even me.

[^cloud-guru]: Look, He bought a box of DevOps! - [A Cloud Guru](https://medium.com/@acloudguru)
