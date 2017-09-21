---
title: Intel Joule
image: https://assets.ubuntu.com/v1/1f53b707-INTEL_JOULE-LOGO.png?w=200
description: Ubuntu Core lets you interact and control complex hardware and modules.
tags: armhf, intel, joule, core, desktop, iot
distributions:
  - Ubuntu Core 16
  - Ubuntu Desktop 16.04 LTS
---
# Intel Joule

## Ubuntu Core

We will walk you through the steps of flashing Ubuntu Core on an Intel Joule. At the end of this process, you will have a board ready for production or testing snaps.

{% include "includes/markdown/get_started_prerequisites.md" %}

### Hardware and software requirements

* An Intel® Joule
    * The board needs to have its BIOS updated to version #193, which is available
[here](https://downloadmirror.intel.com/26206/eng/joule-firmware-2017-02-19-193-public.zip). BIOS update instructions can be found [here](https://software.intel.com/en-us/flashing-the-bios-on-joule)
* 2 USB 2.0 or 3.0 flash drives (2GB min.)
* A monitor with an HDMI interface
* A Mini HDMI to HDMI cable
* A USB keyboard and a mouse
* A USB Hub for all the above USB pieces (4)
* An 802.11 a/b/g/n WiFi network with Internet access
* An [Ubuntu Desktop 16.04.2 LTS image](http://releases.ubuntu.com/16.04.2/ubuntu-16.04.2-desktop-amd64.iso)
* An Ubuntu Core image

#### Ubuntu Core image

[Ubuntu Core 16 image for Intel Joule](http://cdimage.ubuntu.com/ubuntu-core/16/stable/20170323/ubuntu-core-16-joule.img.xz)

* MD5SUM: 03adc0bce55ed1d87c10f79bf5b7e2fa

### Installation instructions

1. Download and copy the Ubuntu Desktop 16.04.1 LTS image on the first USB flash drive by following the Live USB Ubuntu Desktop instuctions for [Ubuntu](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-ubuntu) | [Windows](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-windows) | [Mac OS X](https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-mac-osx)
* Download the Ubuntu Core image for Intel Joule and **copy the file** on the second USB drive
* Connect your USB hub, keyboard, mouse, monitor to the Joule
* Insert the first USB flash drive, containing Ubuntu Desktop 16.04.1 LTS
* Power-up the Joule board, boot-up the device from USB and select “Try Ubuntu without installing” in the first boot menu
* Once the system is ready, insert the second USB flash drive
* Open a terminal and run the following command, where `<disk label>` is the name of the second USB flash drive:

        xzcat /media/ubuntu/<disk label>/ubuntu-core-16-joule.img.xz | sudo dd of=/dev/mmcblk0 bs=32M status=progress; sync

* Remove all USB flash drives and reboot the system, it will reboot from the internal memory now containing Ubuntu Core

{% include "includes/markdown/get_started_first_boot.md" %}

---

## Ubuntu Desktop

As an alternative to Ubuntu Core, you can install Ubuntu Desktop 16.04 LTS, where you can use your favourite development tools to create and run snaps.

* The board needs to have its BIOS updated to version #193, which is available
[here](https://downloadmirror.intel.com/26206/eng/joule-firmware-2017-02-19-193-public.zip). BIOS update instructions can be found [here](https://software.intel.com/en-us/flashing-the-bios-on-joule)

### Ubuntu image

[Intel Joule - Ubuntu Desktop 16.04 LTS image](http://people.canonical.com/~platform/snappy/tuchuck/desktop-final/tuchuck-xenial-desktop-iso-20170317-0.iso)

* MD5SUM: 07e4895b2921117288ff611c6f5fea28

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

### Change the default audio output

In the current release, the analog audio port on mezzanine board is chosen as the default audio output. To use HDMI audio, you need to modify the Joule sound configuration file: `/etc/modprobe.d/joule-snd.conf`.

#### Edit configuration

1. Open an editor to modify the configuration file:

        $ sudo nano /etc/modprobe.d/joule-snd.conf

* To use HDMI audio, uncomment the line `#blacklist snd_sock_skl` and comment the line `softdep snd_hda_intel pre: snd_sock_skl`. You can revert these changes if you want to change your sound output back to defaults.
* Reboot the system to apply the new setting.
