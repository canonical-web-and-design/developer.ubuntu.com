---
title: Create installation medias for Ubuntu Core
description: These steps will walk you through creating a bootable Ubuntu Core SD card or USB flash drive.
---

# Create installation medias for Ubuntu Core

These steps will walk you through creating a bootable Ubuntu Core SD Card or USB flash drive.

This will erase any existing content on the removable drive.

The process is the same on any operating system, you will: download an image file, insert your removable drive (SD card, USB flash drive, etc.), unmount it, replace the drive content with the image file content, eject the drive.

## On Ubuntu

 1. Download the Ubuntu Core image for your device in your `Downloads` folder

 * Insert your SD card or USB flash drive

 * Identify its address by opening the "Disks" application and look for the "Device" line. If the line is in the `/dev/mmcblk0p1` format, then your drive address is: `/dev/mmcblk0`. If it is in the `/dev/sdb1` format, then the address is `/dev/sdb`

 * Unmount it by right clicking its icon in the launcher bar, the eject icon in a file manager or the square icon in the "Disks" application

 * Open a terminal (`Ctrl+Alt+T`) to copy the image to your removable drive

    * If the Ubuntu Core image file you have downloaded ends with an `.xz` file extension, run:

            xzcat ~/Downloads/<image file .xz> | sudo dd of=<drive address> bs=32M

    * Else, run:

            sudo dd if=~/Downloads/<image file> of=<drive address> bs=32M

 * Then, run the `sync` command to finalize the process

 * You can now eject your removable drive. You are ready to [install Ubuntu Core on your device](/core/get-started).

## On Windows

 1. Download the Ubuntu Core image for your device in your `Downloads` folder

 * If the Ubuntu Core image file you have downloaded ends with an `.xz` file extension, you will need to extract it first. To do so, you might have to install an archive extractor software, like [7-zip](http://www.7-zip.org/).

 * Insert your SD card or USB flash drive

 * Download and install [Win32DiskImager](http://sourceforge.net/projects/win32diskimager/files/latest/download), then launch it

 * Find out where your removable drive is mounted by opening a File Explorer window to check which mount point the drive is listed under. Here is an example of an SD card listed under `E`:

    ![](http://i.imgur.com/QXLkLsa.png)

 * In order to flash your card with the Ubuntu image, **Win32DiskImager** will
need 2 elements:

    * an **Image File**: navigate to your `Downloads` folder and select the image you have just extracted

    * a **Device**: the location of your SD card. Select the drive on which your SD card is mounted

    ![](http://i.imgur.com/ebeQHKT.png)

 * When ready click on **Write** and wait for the process to complete.

 * You can now eject your removable drive. You are ready to [install Ubuntu Core on your device](/core/get-started).

## On Mac OS

 1. Download the Ubuntu Core image for your device in your `Downloads` folder

 * If the Ubuntu Core image file you have downloaded ends with an `.xz` file extension, you will need to extract it first. To do so, you might have to install an archive extractor software, like [The
 Unarchiver](https://itunes.apple.com/gb/app/the-unarchiver/id425424353?mt=12).

 * Insert your SD card or USB flash drive

 * Open a terminal window (Go to Application -> Utilities, you will find the
Terminal app there), then run the following command:

        diskutil list

 * In the results, identify your removable drive device address, it will probably look like an entry like the ones below:

        /dev/disk0
          #:                       TYPE NAME                    SIZE       IDENTIFIER
          0:      GUID_partition_scheme                        *500.3 GB   disk0
        /dev/disk2
          #:                       TYPE NAME                    SIZE       IDENTIFIER
          0:                  Apple_HFS Macintosh HD           *428.8 GB   disk1
                                        Logical Volume on disk0s2
                                        E2E7C215-99E4-486D-B3CC-DAB8DF9E9C67
                                        Unlocked Encrypted
        /dev/disk3
          #:                       TYPE NAME                    SIZE       IDENTIFIER
          0:     FDisk_partition_scheme                        *7.9 GB     disk3
          1:                 DOS_FAT_32 NO NAME                 7.9 GB     disk3s1

    Note that your removable drive must be `DOS_FAT_32` formatted. In this example, `/dev/disk3` is the drive address of an 8GB SD card.

 * Unmount your SD card with the following command:

        diskutil unmountDisk <drive address>

 * When successful, you should see a message similar to this one:

        Unmount of all volumes on <drive address> was successful

 * You can now copy the image to the SD card, using the following command:

        sudo dd if=~/Downloads/<image file> of=<drive address> bs=32MB

      When finalised you will see the following message:

        3719+1 records in
        3719+1 records out
        3899999744 bytes transferred in 642.512167 secs (6069924 bytes/sec)

 * You can now eject your removable drive. You are ready to [install Ubuntu Core on your device](/core/get-started).
