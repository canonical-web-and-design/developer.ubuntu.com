---
title: Compute Module 3
image: https://assets.ubuntu.com/v1/2d9f8097-Compute-Module-small-500x2802.jpg
description: Ubuntu Core works on minimal setups, embed and go!
---

# Compute Module 3

We will walk you through the steps of flashing Ubuntu Core on a Compute Module 3. At the end of this process, you will have a board ready for production or testing snaps.

{% include "includes/markdown/get_started_prerequisites.md" %}

## Hardware and software requirements

  * A Compute Module 3
  * A Compute Module IO board
  * Two micro USB to USB cables (one for power, one to setup the CM from the host)
  * An HDMI cable and a display
  * A USB keyboard
  * A USB to RJ45 adaptor or a WiFi dongle
  * A USB hub to attach the keyboard and the RJ45 adaptor/WiFi dongle (note that the keyboard and display can be replaced with a serial cable connected directly to pins of the IO board)
  * An Ubuntu Core image

### Ubuntu Core image

[Ubuntu Core 16 image for Compute Module 3](http://cdimage.ubuntu.com/ubuntu-core/16/edge/current/ubuntu-core-16-armhf+cm3.img.xz)

## Installation instructions

### 1. On the host system: Ubuntu Desktop 16.04 or above

 1. In a terminal, download the USBboot tool you will use to setup the board, and install its build dependencies:

        git clone --depth=1 https://github.com/raspberrypi/usbboot.git
        sudo apt install libusb-1.0-0-dev

 * Then `cd` into the usbboot directory, build with `make` and start the resulting binary as root:

        cd usbboot
        make
        sudo ./rpiboot

 * Once started, it will wait for the Compute Module to be attached to the machine.

### 2. On the Compute Module IO board

 1. Position the Compute Module on the IO board
 * Attach the USB hub, RJ45 adaptor, keyboard and monitor (HDMI) to the board
 * Ensure the `J4` switch (`USB SLAVE BOOT ENABLE`) on the IO board is in the `EN` position
 * With the two micro USB to USB cables, plug the host machine into the IO Board USB slave port (`J15`) and power on the IO board.

### 3. Back to the host system

 1. The USBboot tool should have recognized the attached Compute Module and mounted the EMMC partition as a new device
 * Identify the device by opening the "Disks" application:
    * Locate the EMMC partition of the Compute Module in the left pane
    * Note down its "Device" address on the right pane.
    * If it's mounted, unmount it by clicking the square icon below the partition diagram or the eject icon in a file manager
 * Download the [Ubuntu Core image](#ubuntu-core-image). When this is done you should have an `ubuntu-core-16-armhf+cm3.img.xz` file in your `~/Downloads` directory
 * Flash Ubuntu Core on the EMMC partition with:

        xzcat ~/Downloads/<image file .xz> | sudo dd of=<device address> bs=32M; sync

     This process will take some time. After completion, you can reboot your Compute Module IO board and follow the first boot process with the display and keboard attached to it.


{% include "includes/markdown/get_started_first_boot.md" %}
