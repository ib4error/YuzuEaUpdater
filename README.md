[![Github All Releases](https://img.shields.io/github/downloads/ib4error/YuzuEAUpdater/total.svg)]()

# YuzuEaUpdater
This lightweight, python based, application provides user friendly access to Yuzu Early Releases from the _**pineappleEA/pineapple-src**_ repository. 

## IMPORTANT
This updater assumes you have a _yuzu directory_ with a _yuzu-windows-msvc_ directory in you **%LocalAppData%**
+ %LocalAppData%\yuzu **[ REQUIRED DIR ]**
+ %LocalAppData\yuzu\yuzu-windows-msvc **[ Updater Target Folder ]**

## What It Can Do
+ Check for EA updates listed in the last 48 hours
+ Installs latest EA releases
+ Ability to restore any previous EA version

### How to Use

+ Simply download the release and place it anywhere you'd like.
  + This .exe is fully compiled with everything you need.
  + I recommend having an Emulation directory on your machine where you can categorize all the various things needed with emulation.
  +  Place the _YuzuEAUpdater_ folder in your Emulation folder.
+ Right click exe and **Run as Administrator**
  + Since the _YuzuEAUpdater_ is moving files around in your %LocalAppData% I highly recommend.

### How does it work? FYI
The YuzuEAUpdater is lightweight program that utilizes python and various librarys, modules, and packages to perform basic actions such as download, unzip, copy dir, past dir, rm dir, and regex search strings to maneuver github api, api calls.

