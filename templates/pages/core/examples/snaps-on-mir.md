----
title: Run a kiosk snap on Ubuntu Core
description: How to create a kiosk snap running on top of Mir
----

# Run a kiosk snap on Ubuntu Core

This example has been verified to run on amd64 devices, amd64 kvm-qemu based VM, armhf/RPi3 and arm64/dragonboard.

For getting Ubuntu Core installed and running please reference Getting Started for Ubuntu Core

**Note:** for RPi3, gpu support not quite in the stable channel Ubuntu Core image, will need to use the rpi3 daily edge image

## Quick Start to Experience

Download the latest ubuntu core image. Once you have your Ubuntu Core image running on your desired device/VM, ssh into your device/VM and install in this particular order. If you need more information or are new to snaps, please read through the more detailed subections of this webpage.

``` bash
snap install mir-libs --channel=edge
snap install mir-kiosk --channel=edge
snap install mir-kiosk-apps --channel=edge
```

You should then see the something similar to the image below on your device or VM.

If you are interested in trying out other client applications, you can use the snap set command. For instance:

``` bash
snap set mir-kiosk-apps app=rssnews
```

To see the list of what potential clients exist, just enter the snap set command like so:

``` bash
snap set mir-kiosk-apps app=" "
```

## Introduction

This tutorial is ideal for someone seeking to build a kiosk-style device on Ubuntu Core. This tutorial uses a variety of Qt examples: PhotoViewer as shown above, or Clock as shown below, as well as many other applications. You can determine applications supported by the mir-kiosk-apps snap by interrogating the snap set command.

The mir-kiosk-apps snap is strictly an example of a mir client apps, which developers can use as a template to follow/copy in order to create their own client application snap.

Ubuntu Core recently added a solution for gl/gles drivers to be hosted by the core and accessed by snaps. Previously, vendor specific implementations had to be bundled with any gl/gles enabled application. With this solution in place, it should be that you may build an app using gles on one platform and run on another. For instance on build on intel and run on nvidia, or vice versa. Please let the snappy team know if you discover any issues around this. There's is an open bug on this topic, but it is believed to currently work.

The mir-kiosk snap is only targeted for Ubuntu Core. It is intended for kiosk-like products and applications. For products requiring many separate UI applications supported, Ubuntu Personal with the full Unity8 shell is the more appropriate solution.

This document targets 16 Ubuntu Core and assumes your host machine is running at least 16.04 (up to date), with the stable-phone-overlay installed and using the latest snapcraft and snapd listed here. It might work with earlier versions, but I've only taken care to validate the latest mir on the latest snapcraft on the latest core.

### Prerequisites

You need to be on at least Ubuntu 16.04 LTS host to obtain the proper tools and the latest versions of stage packages. Note, you can install the mir-snaps on a bare metal install of Ubuntu Core on a actual device following these same instructions. However, this example uses a virtual machine to help people have a quick experience who might not have a seperate device, so please make sure Virtual Machine Manager is installed

``` bash
sudo apt install qemu-kvm virt-manager
```

### 1. Download the Ubuntu Core image and set up your VM environment

Now that Ubuntu Core 16 images are becoming available, I recommend using the latest images being published by the Snappy team. These can be found here. If you are new to Ubuntu Core or snaps, I highly recommend visiting snapcraft.io

Now launch your Virtual Machine Manager application (you have installed from steps above). Select the icon for “New Virtual Machine” (or menu to File->New Virtual Machine).


Before beginning, you may need to set the virtual machine the VMM application will use, go to File->Add Connection, select QEMU/KVM. Now to import the image you just created. In the dialog select the radio button for “Import Existing Disk Image”, browse to your `.img`  and select it. You can leave the other defaults. Once you select your way forward, it should launch another window with your Ubuntu Core image VM in it. Once the system settles it will provide you a prompt to walk through the Ubuntu Core console-config, this will occur on any device or VM where you've just freshly installed Ubuntu Core. Note the ip address will be provided for you to ssh into your device or VM.

### 2. Install the mir-libs & mir-kiosk Snaps

Note that the insallation order will matter, install both the mir-kiosk and mir-libs snaps with the following commands via ssh into your device or VM.

``` bash
ssh$ snap install mir-libs --channel=edge
ssh$ snap install mir-kiosk --channel=edge
```

The mir-kiosk should launch, resulting in a black screen with a mouse cursor.

### 3. Get the mir-kiosk-apps snap running

This section assumes the Mir server is up and running, and you’ve followed all of the setup steps from the previous section.

On your host, if you haven’t already, install the snapcraft tools.

``` bash
sudo apt install snapcraft
```

Now pull down the mir-kiosk-apps snap branch. For the purposes of building your own client-application to run on mir-kiosk, I recommend reading through 2 files in this branch: snapcraft.yaml and mir-kiosk-app-daemon. The snapcraft.yaml can be inspected for guidelines on what stage packages are being used. The mir-kiosk-app-daemon file can be used to determine which environment variables need to be set and you may also modify the last lines to change the example application called.

``` bash
git clone -b master https://git.launchpad.net/mir-kiosk-apps
cd mir-kiosk-apps
snapcraft
```
Copy your snap over to your Ubuntu Core device or VM:

``` bash
scp mir-kiosk-apps*.snap devicename@x.x.x.x:/home/devicename
```

Then SSH to the device or VM and install it:

``` bash
ssh$ snap install mir-kiosk-apps*.snap
```

Due to the mir-kiosk-apps being from another provider (you in this case), you will need to manually connect the mir-kiosk-apps snap to the mir-libs interface.

``` bash
ssh$ snap disable mir-kiosk-apps
ssh$ snap connect mir-kiosk-apps:mir-libs mir-libs:mir-libs
ssh$ snap enable mir-kiosk-apps
```

### Tips

* Check or tail `/var/log/syslog` if something isn’t launching or running as expected.

* If you run out of memory from loading too many snaps, you can also grow your image size.

        sudo qemu-img resize xenial_core_amd64.img +1G

* To stop or start the app snap:

        ssh$ sudo systemctl stop snap.mir-kiosk-apps.mir-kiosk-app-daemon.service

        ssh$ sudo systemctl start snap.mir-kiosk-apps.mir-kiosk-app-daemon.service


* To stop or start the Mir snap:

        ssh$ sudo systemctl stop snap.mir-kiosk.mir-kiosk.service

        ssh$ sudo systemctl start snap.mir-kiosk.mir-kiosk.service


* You can check interfaces are connecting with:

        ssh$ snap interfaces

* You may find that cursor/mouse input is better behaved if you forward the mouse to the VM. To do this, in the VMM menu, click on "Virtual Machine" then "Redirect USB device".

### Resources

The various projects used for building mir-libs, mir-kiosk, mir-kiosk-apps, mir-demos-snap are located here:

* [https://launchpad.net/mir-libs-snap](https://launchpad.net/mir-libs-snap)
* [https://launchpad.net/mir-kiosk](https://launchpad.net/mir-kiosk)
* [https://launchpad.net/mir-kiosk-apps](https://launchpad.net/mir-kiosk-apps)
* [https://launchpad.net/mir-demos-snap](https://launchpad.net/mir-demos-snap)
