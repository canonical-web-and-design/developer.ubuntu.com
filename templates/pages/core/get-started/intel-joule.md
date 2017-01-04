---
title: Intel Joule
image: https://assets.ubuntu.com/v1/1f53b707-INTEL_JOULE-LOGO.png?w=200
description: Ubuntu Core lets you interact and control complex hardware and modules.
---
# Intel Joule

We will walk you through the steps of flashing Ubuntu Core on an Intel Joule. At the end of this process, you will have a board ready for production or testing snaps.

(As an alternative, you can also [install Ubuntu Desktop 16.04 LTS](#alternative-install:-ubuntu-desktop-16.04-lts)).

{% include "includes/markdown/get_started_prerequisites.md" %}

## Hardware and software requirements

* An Intel® Joule
    * The board needs to have its BIOS updated to version #131, which is available
[here](https://downloadmirror.intel.com/26206/eng/Joule-Firmware-2016-09-23-131_Public.zip).
* 2 USB 2.0 or 3.0 flash drives (2GB min.)
* A monitor with an HDMI interface
* A Mini HDMI to HDMI cable
* A USB keyboard and a mouse
* A USB Hub for all the above USB pieces (4)
* An 802.11 a/b/g/n WiFi network with Internet access
* An [Ubuntu Desktop 16.04.1 LTS image](http://releases.ubuntu.com/16.04.1/ubuntu-16.04.1-desktop-amd64.iso)
* An Ubuntu Core image

### Ubuntu Core image

[Ubuntu Core 16 beta image for Intel Joule](http://people.canonical.com/~platform/snappy/tuchuck/tuchuck-20161014085519.img.xz)

## Installation instructions

1. Download and copy the Ubuntu Desktop 16.04.1 LTS image on the first USB flash drive by following the Live USB Ubuntu Desktop instuctions for [Ubuntu](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-ubuntu) | [Windows](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-windows) | [Mac OS X](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-mac-osx)
* Download the Ubuntu Core image for Intel Joule and **copy the file** on the second USB drive
* Connect your USB hub, keyboard, mouse, monitor to the Joule
* Insert the first USB flash drive, containing Ubuntu Desktop 16.04.1 LTS
* Power-up the Joule board, boot-up the device from USB and select “Try Ubuntu without installing” in the first boot menu
* Once the system is ready, insert the second USB flash drive
* Open a terminal and run the following command, where `<disk label>` is the name of the second USB flash drive:

        xzcat /media/ubuntu/<disk label>/tuchuck*.img.xz | sudo dd of=/dev/mmcblk0 bs=32M status=progress; sync

* Remove all USB flash drives and reboot the system, it will reboot from the internal memory now containing Ubuntu Core

{% include "includes/markdown/get_started_first_boot.md" %}

## Alternative install: Ubuntu Desktop 16.04 LTS

As an alternative to Ubuntu Core, you can also install Ubuntu Desktop 16.04 LTS, where you can use your favourite development tools to create and run snaps.

### Ubuntu image

* [Intel Joule - Ubuntu Desktop 16.04 LTS image](http://people.canonical.com/~platform/snappy/tuchuck/tuchuck-20161014085519.img.xz)

Download and copy the image on an USB flash drive by following the [installation media instructions](/core/get-started/installation-medias).

### Installation instructions

Booting the board from the USB flash drive will start the Ubuntu installer.

1. Boot the system from the USB flash drive
* The system will automatically execute the first stage of installation, including eMMC storage partitioning and image installation. After installation is complete, a prompt dialog will be shown and you will need to restart the system
* Boot the system on the eMMC storage and finish the install configuration
* Follow the instructions and enter appropriate options for language, WiFi, location (timezone), and keyboard layout
* Pick a hostname, user account and password
* Wait for the configuration to finish. If you connected to a WiFi network at step 4, it will take several minutes to download and apply additional updates. You can now reboot the system
* Ubuntu is installed. Use your account and password to log in
