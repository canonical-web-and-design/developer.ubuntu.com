---
title: Developer setup
description: These steps will walk you through installing a developer environment on an Ubuntu Core device.
---

# Developer setup

1. [Developing on target](#developing-on-target)
    * [Installing and using developer tools](#installing-and-using-developer-tools)
2. [Testing your snaps locally](#testing-your-snaps-locally)
    * [snap install](#snap-install)
    * [snap try](#snap-try)
3. [Installing additional snaps](#installing-additional-snaps)
    * [pulseaudio](#pulseaudio)
    * [tpm](#tpm)
    * [bluez](#bluez)
4. [Platform specific](#platform-specific)
    * [RealSense snaps](#realsense-snaps-(intel-joule)) (Intel Joule)

## Developing on target

You can use any Ubuntu 16.04 LTS workstation to develop a snap using [snapcraft](http://snapcraft.io/docs/build-snaps/), then build for another architecture [using Launchpad or a chroot setup](http://snapcraft.io/docs/build-snaps/build-for-another-arch), but developing on the target device itself is convenient when testing device specific features and lets you iterate faster.

### Installing and using developer tools

Ubuntu Core provides a read-only file system; that doesn't let you install deb packages. Installing the "classic" snap creates a classic Ubuntu environment for you to use on the device.

1. SSH to your device using your Ubuntu SSO user name
2. Install the latest version of the "classic" snap from the [`edge` channel](http://snapcraft.io/docs/reference/channels), with the `--devmode` flag to give it unconfined access to the device.

        snap install classic --edge --devmode

3. Unpack the classic environment and access it using:

        sudo classic

4. You are now presented with the bash shell of a classic Ubuntu 16.04 LTS environment, ready to install your required snap development tools (`snapcraft`, `build-essential`) and other developer tools you might need (`git`, `nodejs`, `bzr`, etc.).

        sudo apt update
        sudo apt install snapcraft build-essential git

5. Next, you can learn how to create snaps on [snapcraft.io](http://snapcraft.io/docs/build-snaps/)

## Testing your snaps locally

You have two ways to test your built snaps in your production environment, either installing a built snap file with `snap install` or using the `snap try` command in your project folder.

### snap install

The `snap install` command lets you install the snap on your system as a user would do from the store.

 1. Exit the classic environment with `Ctrl+D`
 * Install your built snap, with the `--dangerous` flag to bypass store signature checks:

        snap install <snap file> --dangerous

### snap try

The `snap try` command will mount a directory with the content of a snap, as an installed snap on your system. This directory will stay writable, so you can make changes to your snap source code while it's running.

It requires you to have ran `snapcraft` on your project folder at least once, so a `prime` directory with the content of your snap has been generated.

1. Exit the classic environment with `Ctrl+D`
* Run `snap try` in your project folder

The `snap enable` and `disable` commands will let you stop and restart your snap after you changed its code, if for example, it is providing a service that runs when the snap is installed.

## Installing additional snaps

When developing on your device, it can be useful to add the following snaps to enable specific features.

### pulseaudio

Available on armhf, i386, amd64, arm64.

PulseAudio is a sound server for POSIX and Win32 systems. To record or playback audio files, you need to install the pulseaudio snap.

#### Installing pulseaudio

    sudo snap install pulseaudio

#### Using pulseaudio

Note that when executing the following commands, a warning message can be printed ("Failed to create secure directory..."), it can be ignored.

* List all audio modules and devices:

        sudo pulseaudio.pactl list

* List output ports (sinks):

        sudo pulseaudio.pactl list sinks

* List input ports (sources):

        sudo pulseaudio.pactl list sources

* List audio cards:

        sudo pulseaudio.pactl list cards

* Set output and input profile
    * Analog output and analog input:

            sudo pulseaudio.pactl set-card-profile 0 output:analog-stereo+input:analog-stereo

    * Analog output and analog input:

            sudo pulseaudio.pactl set-card-profile 0 output:hdmi-stereo+input:analog-stereo

    Note: the argument `0` is sequence and `output:analog-stereo+input:analog-stereo` and `output:hdmi-stereo+input:analog-stereo` are profiles. They are listed in card information, check the ‘List audio cards’ command above.

* Mute or unmute

    * Mute an output port:

            sudo pulseaudio.pactl set-sink-mute 2 1

        `2` is the sequence of output port which is listed by ‘List output ports (sinks)’. `1` means mute.

    * Unmute an output port:

            sudo pulseaudio.pactl set-sink-mute 2 0

        `0` means unmute.

* Set volume of an output port:

        sudo pulseaudio.pactl set-sink-volume 2 60%

* Record a file in wav format

        sudo pulseaudio.parec --raw /tmp/record.wav

    Use `Ctrl+ C` to stop recording.

* Playback a file in wav format

        sudo pulseaudio.paplay --raw /tmp/record.wav

### tpm

Available on amd64, i386.

The tpm snap provides a daemon and utilities to deal with TPM chips. Before use tpm snap, remember to enable TPM in the BIOS menu.

#### Installing tpm

    sudo snap install tpm

#### Using tpm

* Show version information:

        tpm.version

* Self test:

        tpm.selftest -l debug

* Get NVRAM info:

        tpm.nvinfo

* Take ownership:

        tpm.takeownership

* Clear and disable tpm:

        tpm.clear

    You will need to reboot for this operation to complete.

### bluez

Available on arm64, i386, amd64, armhf.

BlueZ provides support for the core Bluetooth layers and protocols. You can use bluez to control bluetooth controllers and devices.

#### Installing bluez

    sudo snap install bluez

#### Using bluez

* Enable the controller:

    Start `bluez.bluetoothctl` and execute `power on`.

        $ sudo bluez.bluetoothctl
        [NEW] Controller <MAC ADDRESS> [default]
        [bluetooth]# power on
        [CHG] Controller <MAC ADDRESS>
        Changing power on succeeded
        [CHG] Controller <MAC ADDRESS> Powered: yes

* Scan devices:

    Start `bluez.bluetoothctl` and execute `scan on` to start scanning for devices, use `scan off` to stop.

        $ sudo bluez.bluetoothctl
        [NEW] Controller <MAC ADDRESS> [default]
        [bluetooth]# scan on
        [CHG] Controller <MAC ADDRESS> Discovering: yes
        [NEW] Device <MAC ADDRESS> device-name-0
        [NEW] Device <MAC ADDRESS> device-name-1
        [NEW] Device <MAC ADDRESS> device-name-2
        [bluetooth]# scan off
        [CHG] Controller <MAC ADDRESS> Discovering: no

## Platform specific

Some platforms, such as the Intel Joule, can benefit from extra libraries to make the most of Ubuntu Core.

### RealSense snaps (Intel Joule)

You can install RealSense user space libraries with:

    sudo snap install --devmode --edge librealsense-chenhan

Canonical also provide a `librealsense` [snapcraft part](http://snapcraft.io/docs/build-snaps/parts) to accelerate development of RealSense applications.

A GitHub project to develop unit tests for the Intel RealSense already utilizes this `librealsense` part. Follow these steps and look at the source code to get an example on how to start using `librealsense` in a snap.

#### Build the project

Clone the source and build the snap with snapcraft:

    git clone https://github.com/swem/librealsense-unit-test-snap.git
    cd librealsense-unit-test-snap/
    snapcraft

#### Install it locally

After building the snap, install it with:

    sudo snap install --dangerous --devmode librealsense-unit-test-snap*.snap

#### Use it

Running the following command will launch the snap and run unit tests for an Intel RealSense Camera ZR300:

    sudo librealsense-unit-test-snap.ZR300-live-test

[See the project on GitHub](https://github.com/swem/librealsense-unit-test-snap)
