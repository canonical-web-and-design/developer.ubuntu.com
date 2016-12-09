---
Title: Developer setup
Description: These steps will walk you through installing a developer environment on an Ubuntu Core device.
---

# Developer setup

Installing a classic Ubuntu environment is required to develop and build snaps directly on your Ubuntu Core device.

## Developing on target

You can use any Ubuntu 16.04 LTS workstation to develop a snap using [snapcraft](http://snapcraft.io/docs/build-snaps/), then build for another architecture [using Launchpad or a chroot setup](http://snapcraft.io/docs/build-snaps/build-for-another-arch), but developing on the target device itself is convenient when testing device specific features and lets you iterate faster.

### Installing and using developer tools

Ubuntu Core provides a read-only file system, that doesn't let you install deb packages. Installing the "classic" snap creates a classic Ubuntu environment for you to use on the device.

1. SSH to your device using your Ubuntu SSO user name
2. Install the latest version of the "classic" snap from the [`edge` channel](http://snapcraft.io/docs/reference/channels), with the `--devmode` flag to give it unconfined access to the device.

        snap install classic --edge --devmode

3. You can now unpack the classic environment and access it using:

        sudo classic

4. You are now presented with the bash shell of a classic Ubuntu 16.04 LTS environment, ready to install your required snap development tools (`snapcraft`, `build-essential`) and other developer tools you might need (`git`, `nodejs`, `bzr`, etc.).

        sudo apt update
        sudo apt install snapcraft build-essential git

5. Learn how to create snaps on [snapcraft.io](http://snapcraft.io/docs/build-snaps/)

### Testing your snaps locally

You have two ways to test your built snaps in your production environment, either installing a built snap file with `snap install` or using the `snap try` command in your project folder.

#### snap install

The `snap install` command lets you install the snap on your system as a user would do from the store.

 1. Exit the classic environment with `Ctrl+D`
 * Install your built snap, with the `--dangerous` flag to bypass store signature checks:

          snap install <snap file> --dangerous

#### snap try

The `snap try` command will mount a directory with the content of a snap, as an installed snap on your system. This directory will stay writable, so you can make changes to your snap source code while it's running.

It requires you to have ran `snapcraft` on your project folder at least once, so a `prime` directory with the content of your snap has been generated.

1. Exit the classic environment with `Ctrl+D`
* Run `snap try` in your project folder

The `snap enable` and `disable` commands will let you stop and restart your snap after you changed its code, if for example, it is providing a service that runs when the snap is installed.
