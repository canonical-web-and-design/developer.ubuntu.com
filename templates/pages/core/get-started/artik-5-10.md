---
title: Samsung Artik 5 or 10
image: https://assets.ubuntu.com/v1/c5dfb2cb-samsung-artik.png?w=150
description: Ubuntu Core runs smoothly on both small and large footprint boards.
tags: samsung, artik, iot, core, server, armhf
distributions:
  - Ubuntu Core 16
  - Ubuntu Server 16.04 LTS
---

# Samsung Artik 5 or 10

## Ubuntu Core

We will walk you through the steps of flashing Ubuntu Core on a Samsung Artik 5 or 10. At the end of this process, you will have a board ready for production or testing snaps.

{% include "includes/markdown/get_started_prerequisites.md" %}

### Ubuntu Core image

 * [Ubuntu Core 16 image for Samsung Artik 5](http://people.canonical.com/~platform/snappy/artik/uc-series16-final-image/artik5.img.xz)
 * [Ubuntu Core 16 image for Samsung Artik 10](http://people.canonical.com/~platform/snappy/artik/uc-series16-final-image/artik10.img.xz)

### Installation instructions

 1. Copy the Ubuntu Core image on the SD card by following the [installation media instructions&nbsp;&rsaquo;](/core/get-started/installation-medias)
 * Prepare your Artik to boot from the SD card, by setting the "SW2" switches to 1:on and 2:on
 * Insert the SD card
 * Connect the 5V power supply to the board, then use the power button on the board to switch it on

{% include "includes/markdown/get_started_first_boot.md" %}

---

## Ubuntu Server

As an alternative to Ubuntu Core, you can also install Ubuntu Server 16.04 LTS, where you can use your favourite development tools to create and run snaps.

### Ubuntu image

* [ARTIK 5 - Ubuntu Server 16.04 LTS image](http://people.canonical.com/~platform/snappy/artik/archive/artik5-ubuntu-server.img.tar.xz)
* [ARTIK 10 - Ubuntu Server 16.04 LTS image](http://people.canonical.com/~platform/snappy/artik/archive/artik10-ubuntu-server.img.tar.xz)

Download and copy the image for your board on an SD card by following the [installation media instructions&nbsp;&rsaquo;](/core/get-started/installation-medias).

### Installation instructions

Before installing Ubuntu, you need to set your Artik to boot from the SD card, to do so, set the "SW2" switches to `1:on` and `2:on`.

Booting the board from the SD Card will start the Ubuntu installer:

1. Insert the SD card in your Samsung ARTIK
* Connect the 5V power supply to the board, then use the power button on the board to switch on your Samsung ARTIK
* The system will automatically execute the first stage of installation
* Follow the instructions and enter appropriate options for language, WiFi, location (timezone), and keyboard layout
* Pick a hostname, user account and password
* Wait for the configuration to finish. If you connected to a WiFi network at step 4, it will take several minutes to download and apply additional updates. You can now reboot the system
* Ubuntu is installed. Use your account and password to log in
