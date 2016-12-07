---
Title: Samsung Artik 5 or 10
Description: These steps will walk you through flashing Ubuntu Core on a Samsung Artik 5 or 10.
---

# Samsung Artik 5 or 10
![](http://i.imgur.com/tZ619Fm.png)

We will walk you through the steps of flashing Ubuntu Core on a Samsung Artik 5 or 10. At the end of this process, you will have a board ready for production or testing snaps.

As an alternative, you can also install Ubuntu Classic to have a fully-fledged development environment and [develop snaps on target](/core/get-started/developer-setup).

{% include "includes/markdown/get_started_prerequisites.md" %}

## Ubuntu Core image

 * [Ubuntu Core 16 image for Samsung Artik 5](http://people.canonical.com/~platform/snappy/artik/uc-series16-beta-image/artik5.img.tar.xz)
 * [Ubuntu Core 16 image for Samsung Artik 10](http://people.canonical.com/~platform/snappy/artik/uc-series16-beta-image/artik10.img.tar.xz)

## Installation instructions

 1. Copy the Ubuntu Core image on the SD Card by following the [installation media instructions](/core/get-started/installation-medias)
 * Prepare your Artik to boot from the SD card, by setting the "SW2" switches to 1:on and 2:on
 * Insert the SD card
 * Connect the 5V power supply to the board, then use the power button on the board to switch it on

{% include "includes/markdown/get_started_first_boot.md" %}
