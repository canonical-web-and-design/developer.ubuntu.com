----
title: Run a kiosk snap on Ubuntu Core
description: How to create a kiosk snap running on top of Mir
----

# Running a kiosk on Ubuntu Core

This example is ideal for someone seeking to build a kiosk-style device with Ubuntu Core. It showcases a set of Qt applications as examples apps you could run on a kiosk.

To install Ubuntu Core see the [Get Started](../get-started) section.

## Quick Demo

Once you have Ubuntu Core running on your desired device, SSH into it and install the mir-kiosk and mir-kiosk-apps snaps in this particular order:

``` bash
sudo snap install mir-kiosk
sudo snap install mir-kiosk-apps --beta
```

Once this is done, the photoviewer application should start.

There are other examples included. To change applications you need to use the `snap set` command. For instance, to bring up the RSSNews app:

``` bash
snap set mir-kiosk-apps app=rssnews
```

To see the list of available apps, just enter the `snap set` command with an empty value, like this:

``` bash
snap set mir-kiosk-apps app=" "
```

Once you set an app, it will start on the display connected to your device:

![rssnews app](https://assets.ubuntu.com/v1/1449b3d1-Screenshot+from+2017-08-16+15-45-42.png)

## Step by step example

### Introduction

The mir-kiosk-apps snap is an example of a Wayland client, which you can use as a template to create your own client applications.

Ubuntu Core provides a solution for GL/GLES drivers to be hosted by the core and accessed by snaps. With this solution in place, you can build an app using GLES on one platform and run on another. For instance, build on Intel and run on Nvidia, or vice versa. Please let the snap team know if you discover any issues around this.

The mir-kiosk snap is only targeted at Ubuntu Core, not other snapd supported OSes. It is intended for kiosk-like products and applications.

This document targets Ubuntu Core devices and assumes your host machine is running an up to date version of Ubuntu 18.04 LTS, using the latest versions of snapcraft and snapd.

### Prerequisites

You will need an Ubuntu SSO account to create the first user on the Ubuntu Core installation during first boot.

1. Start by creating an [Ubuntu SSO account](https://login.ubuntu.com)
2. Import an SSH Key into your Ubuntu SSO account [on this page](https://login.ubuntu.com/ssh-keys). Instructions to generate an SSH Key on your computer can be found [here](https://help.ubuntu.com/community/SSH/OpenSSH/Keys)

### 1. Download the Ubuntu Core image and set up your VM environment

While you can install the mir snaps on a bare metal install of Ubuntu Core following these instructions, this example focuses on using a virtual machine to help people have a quick experience without needing a separate device.

Download the latest stable Ubuntu Core image for amd64 and uncompress it with the following commands:

```bash
sudo snap install --beta ubuntu-core-vm --devmode
sudo ubuntu-core-vm init
sudo ubuntu-core-vm
```

You should see Ubuntu Core booting in new window. It’ll ask you the usual questions to activate the Core image - once completed you can log in:

```bash
ssh -p 5555 $USERNAME@localhost
```

### 2. Install the mir-kiosk snap

Now you’re inside the VM, you can install Mir-kiosk with the following commands via SSH into your device or VM.

``` bash
ssh$ snap install mir-kiosk
```

mir-kiosk should launch, resulting in a black screen with a mouse cursor.

### 3. Get the mir-kiosk-apps snap running

This section assumes the Mir server is up and running, and you’ve followed all of the setup steps from the previous section.

On your host, if you haven’t already, install the snapcraft tools.

``` bash
sudo apt install snapcraft
```

Now clone the mir-kiosk-apps snap branch.

``` bash
git clone https://github.com/MirServer/mir-kiosk-apps
cd mir-kiosk-apps
```

For the purposes of building your own client-application to run on mir-kiosk, I recommend reading through 2 files in this branch: `snapcraft.yaml` and `mir-kiosk-app-daemon`. The `snapcraft.yaml` can be inspected for guidelines on what stage packages are being used. The `mir-kiosk-app-daemon` file can be used to determine which environment variables need to be set and you may also modify the last lines to change the example application called.

Run snapcraft to build the snap - remember we are building this on a Bionic 18.04 host:

```bash
snapcraft
```

Copy your snap over to your Ubuntu Core device or VM:

``` bash
scp mir-kiosk-apps*.snap <username>@<IP address>:/home/<username>
```

Then SSH to the device or VM and install it:

```bash
ssh$ snap install mir-kiosk-apps*.snap --dangerous
```
Once this is done, the photoviewer application should start automatically. 

### Tips

* Check the logs `snap logs mir-kiosk-apps` if something isn’t launching or running as expected.

* To stop or start the app snap from your ssh session:
```bash
sudo snap stop mir-kiosk-apps
sudo snap start mir-kiosk-apps
```

* To stop or start the Mir snap:
```bash
sudo snap stop mir-kiosk
sudo snap start mir-kiosk
```

### Resources

#### The projects used for building mir-kiosk and mir-kiosk-apps
  * [https://github.com/MirServer/mir-kiosk](https://github.com/MirServer/mir-kiosk)
  * [https://github.com/MirServer/mir-kiosk-apps](https://github.com/MirServer/mir-kiosk-apps)

#### Tutorials for building kiosk snaps
  * [Make a secure Ubuntu kiosk](https://tutorials.ubuntu.com/tutorial/secure-ubuntu-kiosk)
  * [Run a Web Kiosk/Web Display on Ubuntu Core](https://tutorials.ubuntu.com/tutorial/ubuntu-web-kiosk)
  * [Make a Wayland-native Kiosk snap](https://tutorials.ubuntu.com/tutorial/wayland-kiosk)
  * [Make a X11-based Kiosk Snap](https://tutorials.ubuntu.com/tutorial/x11-kiosk)
  * [Make a HTML5/Electron-based Kiosk Snap](https://tutorials.ubuntu.com/tutorial/electron-kiosk)
