---
title: DragonBoard 410c
description: These steps will walk you through flashing Ubuntu Core on a DragonBoard 410c.
---

# DragonBoard 410c

We will walk you through the steps of flashing Ubuntu Core on a DragonBoard 410c. At the end of this process, you will have a board ready for production or testing snaps.

{% include "includes/markdown/get_started_prerequisites.md" %}

## Hardware and software requirements

  * A DragonBoard 410c
  * A microSD card
  * A monitor with an HDMI interface
  * An HDMI cable
  * A USB keyboard
  * An USB to RJ45 adaptor or a WiFi connection
  * An Ubuntu Core image

### Ubuntu Core image

[Ubuntu Core 16 image for DragonBoard 410c](http://cdimage.ubuntu.com/ubuntu-core/16/stable/ubuntu-core-16-dragonboard-410c.img.xz)

## Installation instructions

 1. Copy the Ubuntu Core image on the SD card by following the [installation media instructions](/core/get-started/installation-medias)
 * Make sure the DragonBoard is unplugged from power
 * Set the S6 switch to `0-1-0-0`, where 1 is the "SD boot" option
 * Attach the monitor and keyboard to the board
 * Insert the SD card and plug the power adaptor into the board

{% include "includes/markdown/get_started_first_boot.md" %}
