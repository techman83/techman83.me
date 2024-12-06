Cloud Developer Kits gloss over their best feature!
===================================================

```{post} 2024-12-06
:tags: programming, terraform, devops, platformengineering
:category: Programming
```

Between the little over two years since I wrote 'No one should write Terraform', rewriting large parts of our Internal Developer Platform, and starting on '[Cally](https://cally.callyco.io/)'; there was something myself and most of the commenters missed. Cloud Development Kits often ignore what I would consider one of the strongest selling points. Decoupling yourself and your engineers from your infrastructure!

---

This perspective is certainly biased towards my use case, which is centred around providing an Internal Developer Platform for our internal engineering team, a tool which has been responsible for well over 150,000 deployments since then; and has contributed to the design philosophies around the aforementioned '[Cally](https://cally.callyco.io/)'.
The comments and feedback to my last article most frequently were "Have you thought about using X?", or "have you seen this new tool Y?". Doing my due diligence, and opening the intro page to find what is code block showing you how you can create an AWS service using your favourite language..

```{thumbnail} /assets/posts/2024-12-06-cdks_best_feature/sst.png
:title: SST.dev
:width: 600
:class: figure center
:show_caption: True
```

Now there are some tools[^sst] that bring the promise of being able to generate infrastructure with your code, and that certainly sounds interesting. If you have a small team / startup, fully responsible for your infrastructure, with team members who are all infrastructure experts as well as software engineers, great! That might be the right tool for the job, but I suspect that in a lot of cases the opinion buried in my last article still applies

> Someone whose day-to-day is working on an application, is not going to have the bandwidth to learn a new tool just to create a bucket. Let alone understand the implications of those IAM binding copy/pasted from Stack Overflow resulting in a configuration making a bunch of private data publicly available.
>
> - [No one should write Terraform](../2022/2022-08-13-no_one_should_write_terraform.md)

Ultimately all the tools look quite robust, and appear to have converged around either primarily using, or offering the ability to use Terraform/OpenTofu providers. Which realistically is quite sensible, especially if you want to [order pizza](https://ndmckinley.github.io/terraform-provider-dominos/) after a long day, or maybe use one of many [thousand](https://www.hashicorp.com/blog/hashicorp-terraform-ecosystem-passes-3-000-providers-with-over-250-partners) equally useful providers available. But in my experience, once you have a pattern your Internal Developer Platform is not your bottle neck; it's understanding how to package one or several of the 100s of services available to you, in a secure, robust, and sensible manner for your team to consume.

---

## Contracts and Configuration
The most important aspect of our tooling has been the robust and rich multi layered configuration interface. This provides a consistent, simplified contract for all services managed by our tooling.
This is an example from Cally:

```yaml
defaults:
  providers:
    google:
      default_labels:
        git-repo: my-repo
development:
  defaults:
    providers:
      google:
        project: my-development-project
  services:
    test-service:
      stack_type: CallyStack
      stack_vars:
        example: variable
```

**The Config YAML File:**

- Serves as a contract between engineers and our code
- It is verified using JSONschema, which also generates our documentation.
- Enforces a strict configuration interface, enabling simpler and less defensive code.

**CDK for Terraform**

- Establishes a contract between our configuration and Terraform.
- Guarantees consistent output for a given input.

**Terraform**

- Acts as a contract between Terraform and the infrastructure.
- Is a robust state management tool when paired with well-written providers.
- OpenTofu can be used as an [alternative](https://github.com/opentofu/opentofu/issues/601) to Terraform if preferred.

The benefits of this approach are that a configuration problem is a configuration problem, a code problem is a code problem, and a terraform problem is a terraform problem. You aren't chasing your tail trying to figure out if you've done something wrong, the config is incorrect, or if the provider has a [bug/limitation.](https://github.com/GoogleCloudPlatform/magic-modules/pull/7160).

```{thumbnail} /assets/posts/2024-12-06-cdks_best_feature/spiderman-point.jpg
:title: Who's at fault??
:width: 600
:class: figure center
:show_caption: True
```

When it comes to a tool, pick whichever suits your team and build around it. Whilst I've chosen the CDK for Terraform, I spend very little time thinking about it. Most of it has been abstracted away, so that we can focus on how we can provide useful guard-railed access to the infrastructure, because sometimes the raw terraform can be quite dangerous.
Here's an example from Google's IAM docs:

> Be careful! You can accidentally lock yourself out of your project using this resource. Deleting a google_project_iam_policy removes access from anyone without organization-level access to the project. Proceed with caution. It's not recommended to use google_project_iam_policy with your provider project to avoid locking yourself out, and it should generally only be used with projects fully managed by Terraform. If you do use this resource, it is recommended to import the policy before applying the change.

I can assure you, missing that statement can make for an exciting morning. Shoutout to Google's audit logs though!

---

## Maintenance Burden
One thing often glossed over is the maintenance burden of your IaC. The big cloud vendors are releasing often weekly, with big breaking changes every year or so. And that's without even considering the scenario of being stuck on an [older version](https://developer.hashicorp.com/terraform/language/v1.1.x/upgrade-guides/0-13) of the tooling.

Mid 2021, at version 0.5.0 was when I started experimenting with the CDK for Terraform, and we had a decent amount of production deployments by 0.7.0. Though the provider layout changed in version 0.8.0, we were able to keep using the previous layout until mid last year and 0.17.0 dropped support for the legacy layout. By this stage we had 1000s of resources managed, 50+ different pre-built 'Stack' types, and this felt like a daunting task to address. However the only real breaking change that mattered was how Terraform IDs were handled, as they were much less restrictive than they used to be! But with the test coverage we had, it was easy enough to write a filter to ensure any generated Terraform identifiers remained consistent. The rest of the time was spent improving interactions with the underlying CDK for Terraform code, as the original goal of generating IaC for VM based Microservices and the related infrastructure for a single vendor had long since been exceeded.

The above refactor was preceded by a complete overhaul of the configuration parser. The bespoke multi layered parser had served us well, but there were edge cases that seemed trivial, and weren't. Largely due to the organic development of an internal experiment, which had become a fundamental tool driving 1000s of deployments a week.

The changes to the tooling were completed, rolled out, and largely unnoticed by the consumers of the tooling. We'd kept our promise with those consuming it and with Terraform, even though we'd essentially gutted and re-written the internals.

---

I largely covered in the [prior article](../2022/2022-08-13-no_one_should_write_terraform.md) the benefits of using an imperative language like Python over a declarative one like HCL, so here are some of the tools that ensure we can rapidly iterate our Internal Developer Platform and keep our focus on delivering useful and easy to consume infrastructure.

- [ruff](https://docs.astral.sh/ruff/) has been an absolute game changer in terms of linting and code quality. It's extremely fast, and flexible in terms of what rule sets you want to configure.
- [black](https://github.com/psf/black) allows us to set the standards, and keeps us honest. No more unnecessary discussions about layout or format.
- [mypy](https://mypy-lang.org/) because sometimes being a little strict can be a good thing!
- [coverage](https://coverage.readthedocs.io/) whilst 100% coverage isn't the be all and end all, often unexpected lines not covered reveals bugs that would have gone unnoticed!

Though Terraform tools do exist, they're very domain specific. Being able to lean on decades of existing tools, and broadly understood programming concepts to provide strong guarantees that your Internal Developer Platform is robust and reliable, whilst being able to iterate rapidly.

---

## TL;DR
Ultimately the decision is yours, pick a tool that suits your use case and language proficiency. Be it sticking with raw HCL or using a CDK like Pulumi, SST, the CDK for Terraform, or one of the many others I'm sure to learn about in the comments.

[Cally](https://cally.callyco.io/) is a project I've been working on in my spare time, it aims to provide a foundational layer for your Internal Developer Platform, with the goals of addressing what I've discussed in this article.

**Key Features**
- Simple but rich and [documented configuration](https://cally.callyco.io/configuration) layer
- Documentation with [examples](https://cally.callyco.io/concepts) to make getting started easier
- Built in [test harness](https://cally.callyco.io/api#testing) to provide a starting point for ensuring your IaC has robust test coverage
- The [license](https://github.com/CallyCo-io/Cally/blob/main/LICENSE) is deliberately permissive as the goals are to lower the barrier to entry for building an Internal Developer Platform

It's still in the early stages, but if you're interested, check it out! I'd love to find all the bugs that I've missed 😀

[^sst]: [SST.dev](https://sst.dev)
