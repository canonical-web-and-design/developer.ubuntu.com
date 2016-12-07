---
Title: Intel Nuc
Description: These steps will walk you through flashing Ubuntu Core on an Intel NUC.
---

![](http://i.imgur.com/wB6bD81.png)

## Ubuntu Core on an Intel Nuc

We will walk you through the steps of flashing Ubuntu Core on an Intel NUC. At the end of this process, you will have a board ready for production or testing snaps.

As an alternative, you can also install Ubuntu Classic to have a fully-fledged development environment and [develop snaps on target](/core/get-started/developer-setup).

{% include "includes/markdown/get_started_prerequisites.md" %}

## Hardware and software requirements

 * an Intel® NUC
    * The NUC needs to have its BIOS updated to the latest version. For this, you can follow online instructions [on the Intel website](http://www.intel.com/content/www/us/en/support/boards-and-kits/000005850.html)
 * 2 USB 2.0 or 3.0 flash drive (respectively 2GB and 8GB min.)
 * a monitor with an HDMI interface
 * a USB keyboard and a mouse
 * a network connection with Internet access
 * an [Ubuntu Desktop 16.04.1 LTS image](http://releases.ubuntu.com/16.04.1/ubuntu-16.04.1-desktop-amd64.iso)
 * An Ubuntu Core Image

### Ubuntu Core image

[Ubuntu Core 16 image for Intel NUC](http://people.canonical.com/~platform/snappy/havasu/uc-series16-beta-image/havasu-20161021070243.img.xz)

## Installation instructions

### Prepare installation medias

 1. Download and copy the Ubuntu Desktop 16.04.1 LTS image on the first USB flash drive by following the Live USB Ubuntu Desktop instuctions for [Ubuntu](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-ubuntu) | [Windows](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-windows) | [Mac OS X](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-mac-osx)
 * Download the Ubuntu Core image for Intel NUC and **copy the file** on the second USB flash drive

### Prepare the NUC (if using internal ROM as disk)

This step is only necessary in case you want to install Ubuntu Core on the emmc Built-In Storage. If you wired an SSD drive to your NUC, this section can be skipped.

 1. Start your NUC by pressing the On button while pressing F2 during the boot up, this will open the BIOS settings
 * On the initial screen, open the "Advanced" tab, then open the "Devices and Peripherals" tab
 * On the "Devices and Peripherals" menu, under the "On board devices" submenu, make sure that the emmc checkbox ("4GB emmc Built-in Storage") is checked. If you didn't find this option, this means that you need to update your NUC BIOS to latest version. For this, you can follow [online instructions on the Intel website](http://www.intel.com/content/www/us/en/support/boards-and-kits/000005850.html).
 * In the "Boot" menu, "Secure boot" submenu, make sure that the "secure boot" option is not checked.

### Boot from the Live USB flash drive

 * Insert the Live USB Ubuntu Desktop flash drive in the NUC
 * Start the NUC and push F10 to enter the boot menu.
 * Select the USB flash drive as a boot option
 * Select "Try Ubuntu without installing”

### Flash Ubuntu Core

 * Once the system is ready, insert the second USB flash drive containging the Ubuntu Core image file
 * Open a terminal and run the following command, where `<disk label>` is the name of the second USB flash drive:
    * Using the NUC emmc storage:

            xzcat /media/ubuntu/<disk label>/havasu*.img.xz | sudo dd of=/dev/mmcblk0 bs=32M status=progress; sync

    * Using an SSD drive:

            xzcat /media/ubuntu/<disk label>/havasu*.img.xz | sudo dd of=/dev/sda bs=32M status=progress; sync

 * Remove all USB flash drives and reboot the system, it will reboot from the internal memory or SSD drive now containing Ubuntu Core

{% include "includes/markdown/get_started_first_boot.md" %}
