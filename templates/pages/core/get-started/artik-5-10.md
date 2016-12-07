----
Title: Samsung Artik 5 or 10
Description:
----

![](http://i.imgur.com/tZ619Fm.png)

## Ubuntu Core on a Samsung Artik 5 or 10

We will walk you through the steps of flashing Ubuntu Core on a Samsung Artik 5 or 10.

At the end of this document you will have a board ready for production or testing snaps.

You can also install Ubuntu Classic on this board to have a development environment and develop snaps on target.

{% include "includes/markdown/get_started_prerequisites.md" %}

### Ubuntu Core image

 * [Ubuntu Core 16 image for Samsung Artik 5](http://people.canonical.com/~platform/snappy/artik/uc-series16-beta-image/artik5.img.tar.xz)
 * [Ubuntu Core 16 image for Samsung Artik 10](http://people.canonical.com/~platform/snappy/artik/uc-series16-beta-image/artik10.img.tar.xz)

## Installation instructions

 1. Copy the Ubuntu Core image on the SD Card by following the [installation media instructions](/core/get-started/installation-medias)
 * Make sure the DragonBoard is unplugged from power
 * Set the S6 switch to `0-1-0-0`, where 1 is the "SD boot" option
 * Attach the monitor and keyboard to the board
 * Insert the SD Card and plug the power adaptor into the board

{% include "includes/markdown/get_started_first_boot.md" %}
