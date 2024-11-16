Jira Automation + Copying Fields
================================

```{post} 2014-08-04
:tags: programming, groovy, jira, automation, scriptrunner
:category: Programming
:author: techman83
```

We heavily utilise Jira at my place of work and one of our non IT based departments use it in their business processes. It was chosen to replace a custom developed, unreliable .NET application and apart from minor bending to suit the processes Jira is an excellent replacement. It's also far more reliable, far easier to keep up-to-date and runs on Linux!

In the latest update I had a chance to really push the new version of the [Jira Automation Plugin](https://marketplace.atlassian.com/plugins/com.atlassian.plugin.automation.jira-automation-plugin), which is a free and open source plugin. Written by Atlassian to support their internal processes, It's a little nugget of awesome that has really extended what we can do without writing bulk custom code.

The team that maintains the Jira Automation plugin implemented a feature request I raised for [Copying fields](https://bitbucket.org/atlassianlabs/automation/issue/10/copy-field-contents-to-another), which they implented and included in their next release. However being a simple field copy, the data needs to be exactly how the destination expects.

Insert the [Script Runner](https://marketplace.atlassian.com/plugins/com.onresolve.jira.groovy.groovyrunner) plugin. Which offers a massive amount of things you can extend without writing a custom Jira Plugin. Whilst I've written one before I'm completely allergic to the concept, as it requires Java ramp up that I'm not really interested in.

When I first used the Script Runner plugin, external scripts were really the only option for doing things. Often when I need to hack something together a post action script is my default go to, but in the case of the combination of the Automation Plugin gave results that didn't work in practice and required a lot more effort to do the job.

The easiest way to give the Automation plugin data that the destination can accept is to use a transitionary custom field. I was initially using a post action script to populate it, however it populates it after the Trigger that fires the automation and gets blatted in the process. Which is less than ideal.

*Setting a field to contain the raw username*

```java
// Accessing Customfield data
import com.atlassian.jira.ComponentManager
import com.atlassian.jira.issue.CustomFieldManager

// Updating Custom field data
import com.atlassian.jira.issue.ModifiedValue
import com.atlassian.jira.issue.util.DefaultIssueChangeHolder
import com.atlassian.jira.issue.util.IssueChangeHolder
import com.atlassian.jira.issue.fields.CustomField

// Define Field IDs
def assignee = "customfield_11402"
def assigneeTransition = "customfield_11705"

// Load Custom Fields from Jira
ComponentManager componentManager = ComponentManager.getInstance()
CustomFieldManager customFieldManager = componentManager.getCustomFieldManager()
CustomField assigneeSrc = customFieldManager.getCustomFieldObject(assignee)
CustomField assigneeTransitionCF = customFieldManager.getCustomFieldObject(assigneeTransition)

// Load Values
def assigneeVal = issue.getCustomFieldValue(assigneeSrc).getUsername()

// Write data
IssueChangeHolder changeHolder = new DefaultIssueChangeHolder();
assigneeTransitionCF.updateValue(null, issue, new ModifiedValue(issue.getCustomFieldValue(assigneeTransitionCF), assigneeVal), changeHolder)
```

Now the Script Runner plugin can produce [scripted fields](https://jamieechlin.atlassian.net/wiki/display/GRV/Scripted+Fields). Which can return information when queried (cached by default, but caching can be disabled). Which is a perfect companion to the Automation Plugin.

*Returning a raw username compatible with the Assignee Field*

```java
import com.atlassian.jira.ComponentManager
import com.atlassian.jira.issue.CustomFieldManager
import com.atlassian.jira.issue.fields.CustomField

if ( issue.getCustomFieldValue(ComponentManager.getInstance().getCustomFieldManager().getCustomFieldObject("customfield_10400")) == null ) {
  return
} else {
  // Get username from 'Custom Field 10400'
  return issue.getCustomFieldValue(ComponentManager.getInstance().getCustomFieldManager().getCustomFieldObject("customfield_10400")).getUsername()
}
```

 - Update 2014-08-08 - It's probably a good idea to check that 10400 contains a user object before you fill your logs with Null Pointer Exceptions during indexing!

*Automatically generate a Date compatible with the Due Date field*

```java
import java.sql.Timestamp
import java.util.Date
import java.text.SimpleDateFormat
import java.text.DateFormat

//Returns current date + 4 weeks - formatted '26/Jul/14'
return new SimpleDateFormat("d/MMM/yy").format(new Timestamp(new java.util.Date().getTime()).plus(28))
```

Though the script runner is based on Groovy, you can import (at least to my limited knowledge) any Java class available within the Jira framework. The Jira Automation + Script Runner plugins complement each other perfectly and really give you a huge amount of flexibility without writing a custom Plugin. As long as the data for the destination is valid the Automation plugin will happily set the field and it's trivial to provide that data via a Scripted field.

Happy Days!
