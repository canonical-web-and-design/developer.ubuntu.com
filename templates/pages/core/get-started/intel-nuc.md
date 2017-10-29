---
title: Intel NUC
image: https://assets.ubuntu.com/v1/a69b2863-intel+nuc.svg?fmt=png&w=150
description: Ubuntu Core can be easily installed on other architectures like Intel® 64 bits.
tags: nuc, intel, core, server, iot, 64
distributions:
  - Ubuntu Core 16
  - Ubuntu Server 16.04 LTS
---
# Intel NUC

## Ubuntu Core

We will walk you through the steps of flashing Ubuntu Core on an Intel NUC. At the end of this process, you will have a board ready for production or testing snaps.

{% include "includes/markdown/get_started_prerequisites.md" %}

### Hardware and software requirements

 * An Intel® NUC
    * The NUC needs to have its BIOS updated to the latest version. For this, you can follow online instructions [on the Intel website](http://www.intel.com/content/www/us/en/support/boards-and-kits/000005850.html)
 * 2 USB 2.0 or 3.0 flash drives (2GB min.)
 * A USB keyboard, mouse and hub to accomodate all the USB pieces
 * A monitor with VGA or HDMI interface
 * A VGA or HDMI cable
 * A network connection with Internet access
 * An [Ubuntu Desktop 16.04.2 LTS image](http://releases.ubuntu.com/16.04.2/ubuntu-16.04.2-desktop-amd64.iso)
 * An Ubuntu Core image

#### Ubuntu Core image

[Ubuntu Core 16 image for Intel NUC](http://releases.ubuntu.com/ubuntu-core/16/ubuntu-core-16-amd64.img.xz)

 * MD5SUM:  f335673a2a386fc839cc68376bc8d6dd

### Installation instructions

#### Prepare installation medias

 1. Download and copy the Ubuntu Desktop 16.04.1 LTS image on the first USB flash drive by following the Live USB Ubuntu Desktop instuctions for [Ubuntu](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-ubuntu) | [Windows](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-windows) | [Mac OS X](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-mac-osx)
 * Download the Ubuntu Core image for Intel NUC and **copy the file** on the second USB flash drive

#### Boot from the Live USB flash drive

 * Connect the USB hub, keyboard, mouse and the monitor to the NUC
 * Insert the Live USB Ubuntu Desktop flash drive in the NUC
 * Start the NUC and push F10 to enter the boot menu
 * Select the USB flash drive as a boot option
 * Select "Try Ubuntu without installing”

#### Flash Ubuntu Core

 * Once the system is ready, insert the second USB flash drive containing the Ubuntu Core image file
 * Open a terminal and type the following command to check for directories mounted on the internal storage:

        mount | grep mmcblk

    If there is any directory mounted on the internal eMMC storage, unmount it. For instance, if you see an occurence of `/dev/mmcblk0p3 on /media/ubuntu/writable type ext4 (rw,relatime,data=ordered)`, run `sudo umount /media/ubuntu/writable`.

 * Run the following command, where `<disk label>` is the label of the second USB flash drive:

        xzcat /media/ubuntu/<disk label>/ubuntu-core-16-amd64.img.xz | sudo dd of=/dev/mmcblk0 bs=32M status=progress; sync

 * Reboot the system and remove the flash drives when prompted, it will then reboot from the internal memory where Ubuntu Core has been flashed

{% include "includes/markdown/get_started_first_boot.md" %}

---

## Ubuntu Server

As an alternative to Ubuntu Core, you can install Ubuntu Server 16.04 LTS, where you can use your favourite development tools to create and run snaps.

### Ubuntu image

* [Intel NUC - Ubuntu Desktop 16.04 LTS image](http://people.canonical.com/~platform/snappy/nuc/ubuntu-server-16.04.1-20160817-0.iso)

Download and copy the image on an USB flash drive by following the [installation media instructions &rsaquo;](/core/get-started/installation-medias).

### Installation instructions

Booting the board from the USB flash drive will start the Ubuntu installer.

1. Insert the USB flash drive in the NUC
* Start the NUC and push F10 to enter the boot menu.
* Select the USB flash drive as a boot option
* The system will automatically execute the first stage of installation, including eMMC storage partitioning and image installation. After installation is complete, a prompt dialog will be shown and you will need to restart the system
* Boot the system on the eMMC storage and finish the install configuration
* Follow the instructions and enter appropriate options for language, WiFi, location (timezone), and keyboard layout
* Pick a hostname, user account and password
* Wait for the configuration to finish. If you connected to a WiFi network at step 4, it will take several minutes to download and apply additional updates. You can now reboot the system
* Ubuntu is installed. Use your account and password to log in
