---
title: Raspberry Pi 2 or 3
image: https://assets.ubuntu.com/v1/635f5dbf-raspberry_pi_logo_rgb_.svg?fmt=png&w=90
description: Ubuntu Core allows you to install apps on your board in just a few clicks.
---
# Raspberry Pi 2 or 3

We will walk you through the steps of flashing Ubuntu Core on a Raspberry Pi 2 or 3. At the end of this process, you will have a board ready for production or testing snaps.

{% include "includes/markdown/get_started_prerequisites.md" %}

## Hardware and software requirements

  * A Raspberry Pi 2 or 3
  * A microSD card
  * A monitor with an HDMI interface
  * An HDMI cable
  * A USB keyboard
  * An Ubuntu Core image

### Ubuntu Core image

 * [Ubuntu Core 16 image for Raspberry Pi 2](http://cdimage.ubuntu.com/ubuntu-core/16/stable/current/ubuntu-core-16-pi2.img.xz)
 * **Rapsberry Pi 3**
   * [Ubuntu Core 16 image for Raspberry Pi 3 (stable)](http://cdimage.ubuntu.com/ubuntu-core/16/stable/current/ubuntu-core-16-pi3.img.xz): the older kernel shipped with this stable image can trigger Wi-Fi issues during first boot, network cable recommended.
   * [Ubuntu Core 16 image for Raspberry Pi 3 (edge)](http://cdimage.ubuntu.com/ubuntu-core/16/edge/current/ubuntu-core-16-pi3.img.xz): this image provides reliable Wi-Fi at first boot, but is a daily build and not deemed stable.

## Installation instructions

 1. Copy the Ubuntu Core image on the SD card by following the [installation media instructions&nbsp;&rsaquo;](/core/get-started/installation-medias)
 * Attach the monitor and keyboard to the board. You can alternatively use a serial cable.
 * Insert the SD card and plug the power adaptor into the board

{% include "includes/markdown/get_started_first_boot.md" %}
