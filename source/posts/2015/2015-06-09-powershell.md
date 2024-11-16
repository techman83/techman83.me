Powershell + Windows Update
===========================

```{post} 2015-06-09
:tags: programming, powershell, windows, update, win10
:category: Programming
:author: techman83
```

Windows administration is part of my job that I don't enjoy as much as linux, but it is still necessary. Though Windows is becoming less and less required, a lot of software still relies on it.

Microsoft to their credit are making an effort to shift people onto their new OS before it becomes another Windows XP situation (Released in 2001, 4 OS' released in that time and it is still being used in a lot of places). However they seemed to have failed restricting the updates to Consumer machines only.

Having the update deploy to coporate machines (I've seen reports of it happening on Domain joined and Volume licensed machines) is all rather annoying and removing them only means they have a chance to come back next time the user updates. In an ideal world you'd use WSUS, but with a geographically disperse workforce often working in remote locations this isn't practical.

Enter [PSWindowsUpdate](https://gallery.technet.microsoft.com/scriptcenter/2d191bcd-3308-4edd-9de2-88dff796b0bc/). Now it didn't work on powershell 2.0 without a slight modification

PSWindowsUpdate.psm1 - It's top comment on one of the threads, If I remember where I'll make the attribution.

```powershell
if ($PSVersionTable.PSVersion.tostring() -ge 4)
{
    Get-ChildItem -Path $PSScriptRoot | Unblock-File
}
Get-ChildItem -Path $PSScriptRoot\*.ps1 | Foreach-Object{ . $_.FullName }
```

I also removed the confirmation around the uninstall (I think it's just missing the argument to ignore it, but It was quicker for me just to remove it):

Get-WUUninstall.ps1 with confirmation removed from "Process', also added '/quiet /norestart'

```powershell
Process
{
      If($KBArticleID)
      {
          $KBArticleID = $KBArticleID -replace "KB", ""

          wusa /uninstall /kb:$KBArticleID /quiet /norestart
      } #End If $KBArticleID
      Else
      {
          wmic qfe list
      } #End Else $KBArticleID
} #End Process
```

This is what I came up with and it appears to work well enough. It could use some extra checking and polishing, but we will have auto deploy and also as a utility app. If someone mentions it, they can be instructed to re-run it and it will try again. Also that's about as much time I wish to spend doing anything in powershell!

```powershell
Import-Module PSWindowsUpdate

$ServiceID = Get-WUServiceManager| Select ServiceID

# KB3035583 - GWX - Get Windows 10 AdWare
# KB2952664 - Compatibility Update for Upgrading Win 7 to Win 10
# KB3021917 - Phones Home to tell MS how your computer will perform with Win 10

$kbIDs = "KB3035583","KB2952664","KB3021917"

$installed = Get-WUList -ServiceID $ServiceID -IsInstalled -KBArticleID $kbIDs | Select KB

if ($installed) {
    write-host "We have some crud to remove"
    Write-Host $installed

    foreach ($update in $installed) {
        Write-Host "Removing " $update.KB
        Get-WUUninstall -KBArticleID $update.KB
        Start-Sleep -s 10
    }
} else {
    write-host "We're Crap free"
}

Start-Sleep -s 10

$tohide = Get-WUList -ServiceID $ServiceID -KBArticleID $kbIDs -IsNotHidden

if ( $tohide ) {
    Write-Host "Hide ALL the CRAP!!!"
    Write-Host ($tohide | Format-Table | Out-String)
    foreach ($hide in $tohide) {
        Write-Host "Hiding " $hide.KB
        Write-Host ($hide | Format-Table | Out-String)
        $hide.IsHidden = $true
        Start-Sleep -s 10
    }
}
```

Things to note:

 * Get-WUList seems to take forever.
 * Get-WUList seems won't show what's current until after a reboot (some updates require a reboot and seem to not change their installed state until done).
 * You can iterate of an object or an array, but if your object is an array and you don't loop over it you'll be left scratching your head.
