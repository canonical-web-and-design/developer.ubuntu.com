---
title: Orange Pi Zero
image: https://assets.ubuntu.com/v1/55cfce66-orange-pi-logo.png
description: Ubuntu Core also runs on the AllWinner H2 SoC used on Orange Pi boards.
tags: orange, pi, core, iot, embedded, armhf
distributions:
  - Ubuntu Core 16
---
# Orange Pi Zero

## Ubuntu Core

We will walk you through the steps of flashing Ubuntu Core on an Orange Pi Zero. At the end of this process, you will have a board ready for production or testing snaps.

{% include "includes/markdown/get_started_prerequisites.md" %}

### Hardware and software requirements

  * An Orange Pi Zero
  * A microSD card
  * A USB to TTL Serial Cable
  * An Ethernet cable (for first setup)
  * A 5V power supply rated at 2 amps and a cable with a micro USB plug
  * `screen` installed on your host computer (`sudo apt install screen`)

#### Ubuntu Core image

 * [Ubuntu Core 16 for Orange Pi Zero](http://www.orangepi.org/downloadresources/orangepizero/2017-08-18/orangepizero_97899291e57c7a56ec9073f.html)

### Installation instructions

 1. Copy the Ubuntu Core image on the SD card by following the [installation media instructions&nbsp;&rsaquo;](/core/get-started/installation-medias)
 * Insert the SD card into the board.
 * Connect the Ethernet cable to the board and to the network.
 * Connect the TTL end of the TTL to USB cable, to the three pins next to the Ethernet port. On [this diagram](http://www.orangepi.org/orangepizero/images/orangepizero_info.jpg), they are identified by the label "Debug serial port". The pin layout is, from the outside to the inside:
    * `GND` (black wire)
    * `RX` (white wire)
    * `TX` (green wire).
 * Connect the USB end of the cable into your host computer, open a terminal and run `sudo screen /dev/ttyUSB0 115200` to open a listening connection to the board.
 * Power on the board. The terminal on your host computer should display the boot sequence. If not, please ensure the TTL to USB cable is correctly connected.

{% include "includes/markdown/get_started_first_boot.md" %}
