----
Title: Intel Joule
Description:
----

![](http://i.imgur.com/NoshHIW.png)

## Ubuntu Core on an Intel Joule

We will walk you through the steps of flashing Ubuntu Core on an Intel Joule.

{% include "includes/markdown/get_started_prerequisites.md" %}

## Hardware and software requirements

* an Intel® Joule
  * The board needs to have its BIOS updated to version #131, which is available
[here](https://downloadmirror.intel.com/26206/eng/Joule-Firmware-2016-09-23-131_Public.zip).
* 2 USB 2.0 or 3.0 flash drives (2GB min.)
* a monitor with an HDMI interface
* a Mini HDMI to HDMI cable
* a USB keyboard and a mouse
* a USB Hub for all the above USB pieces (4)
* an 802.11 a/b/g/n WiFi network with Internet access
* an [Ubuntu Desktop 16.04.1 LTS image](http://releases.ubuntu.com/16.04.1/ubuntu-16.04.1-desktop-amd64.iso)
* an Ubuntu Core image

### Ubuntu Core image

[Ubuntu Core 16 beta image for Intel Joule](http://people.canonical.com/~platform/snappy/tuchuck/tuchuck-20161014085519.img.xz)

## Installation instructions

1. You will need [an Ubuntu SSO account and an SSH key linked to it](#prerequisites), to create the first user on the device
* Download and copy the Ubuntu Desktop 16.04.1 LTS image on the first USB flash drive by following the [...](...)
* Download the Ubuntu Core image and copy the file on the second USB drive
* Connect your USB hub, keyboard, mouse, monitor to the Joule
* Insert the first USB flash drive, containing Ubuntu Desktop 16.04.1 LTS
* Power-up the Joule board, boot-up the device from USB and select “Try Ubuntu without installing” in the first boot menu
* Once the system is ready, insert the second USB flash drive
* Open a terminal and run the following command, where `<disk label>` is the name of the second USB flash drive:

        xzcat /media/ubuntu/<disk label>/tuchuck*.img.xz | sudo dd of=/dev/mmcblk0 bs=32M status=progress; sync

* Remove the USB flash drive and reboot the system

{% include "includes/markdown/get_started_first_boot.md" %}
