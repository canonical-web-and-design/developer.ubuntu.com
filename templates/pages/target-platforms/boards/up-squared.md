---
title: UP Squared IoT Grove Development Kit
image: https://assets.ubuntu.com/v1/1f53b707-INTEL_JOULE-LOGO.png?w=200
description: The UP Squared IoT Grove Development Kit by Intel
tags: intel, server, lts, desktop, iot
distributions:
  - Ubuntu Server 16.04 LTS
---

# UP Squared IoT Grove Development Kit

## Ubuntu Server

We will walk you through the steps of installing Ubuntu Server on the [UP Squared IoT Grove Development Kit](https://insights.ubuntu.com/2017/11/20/introducing-the-up²-grove-iot-development-kit-with-ubuntu/). At the end of this process, you will have a fully fledged development or production environment.

### Ubuntu image

Intel provides a modified Ubuntu Server 16.04.3 LTS image shipped with a custom 4.10 kernel and the Intel IoT Developer Kit.

* [Ubuntu Server 16.04 LTS image](https://downloads.up-community.org/download/up-squared-iot-grove-development-kit-ubuntu-16-04-server-image/)

Download and copy the image to a USB flash drive by following the installation media instructions for: [Ubuntu](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-ubuntu), [Windows](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-windows) or [macOS](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-macos).

### Installation instructions

Booting the board from the USB flash drive will start the Ubuntu installer.

1. Insert the USB flash drive in the Up Squared board
2. Power on the board
3. The installer will start automatically. Follow the prompts to install Ubuntu Server on the on-board eMMC disk. You can refer to [this tutorial](https://tutorials.ubuntu.com/tutorial/tutorial-install-ubuntu-server#4) for complete Ubuntu Server installation guidance.

### Next steps

Your board is ready to develop and run snaps, secured application packages tailored for IoT, this tutorial will show you [how to create your first snap](https://tutorials.ubuntu.com/tutorial/create-your-first-snap).
