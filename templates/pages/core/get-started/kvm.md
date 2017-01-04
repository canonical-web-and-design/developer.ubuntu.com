---
title: KVM
image: https://assets.ubuntu.com/v1/aa0e2566-kvm-logo.png?w=120
description: Develop on target or on your Linux desktop, run Ubuntu Core in a virtual environment.
---
# KVM

We will walk you through the steps of installing Ubuntu Core on your Linux desktop in a virtual machine.

{% include "includes/markdown/get_started_prerequisites.md" %}

## Installation instructions

### 1. Install KVM

Install the qemu-kvm package with the following command:

    sudo apt install qemu-kvm

Then, run the kvm-ok command to check KVM status and your hardware:

    kvm-ok
    INFO: /dev/kvm exists
    KVM acceleration can be used

This is the best outcome — it means that Ubuntu Core will run fast on your system, taking advantage of hardware acceleration in your CPU.

### 2. Download Ubuntu Core

Download the [Ubuntu Core image for amd64](http://releases.ubuntu.com/ubuntu-core/16/ubuntu-core-16-amd64.img.xz) and uncompress it with the following commands:

    wget http://releases.ubuntu.com/ubuntu-core/16/ubuntu-core-16-amd64.img.xz
    unxz ubuntu-core-16-amd64.img.xz

You have an image ready to boot.

### 3. Launch KVM

You can now launch a virtual machine with KVM, using the following command:

    kvm -smp 2 -m 1500 -netdev user,id=mynet0,hostfwd=tcp::8022-:22,hostfwd=tcp::8090-:80 -device virtio-net-pci,netdev=mynet0 -drive file=ubuntu-core-16-amd64.img,format=raw

Note that this command also sets up port redirections:

* `localhost:8022` is redirecting to port `22` of the virtual machine for accessing it through SSH
* `localhost:8090` is redirecting to its port `80`

You should see a window, with your Ubuntu Core virtual machine booting inside it.

### 4. First boot

  1. The system will boot then become ready to configure
  2. The device will display the prompt “Press enter to configure”
  3. Press enter then select “Start” to begin configuring your network and an administrator account. Follow the instructions on the screen, you will be asked to configure your network and enter your Ubuntu SSO credentials
  4. At the end of the process, you will see **your credentials to access your Ubuntu Core machine**:

        This device is registered to <Ubuntu SSO email address>.
        Remote access was enabled via authentication with the SSO user <Ubuntu SSO user name>
        Public SSH keys were added to the device for remote access.

#### User login

Once setup is done, you can login with SSH into Ubuntu Core, using the following command:

    ssh -p 8022 <Ubuntu SSO user name>@localhost

The user name is your Ubuntu SSO user name, it has been reminded to you at the
end of the account configuration step.

##### First boot tips

  * During setup,` console-conf` will download the SSH key registered with your store account and configure it so you can log into the device via `ssh -p 8022 <Ubuntu SSO account name>@localhost` without a password.
  * There is no default `ubuntu` user on these images, but you can run `sudo passwd <account name>` to set a password in case you need a local console login.

### 5. Install snaps

Your virtual machine is ready to have snaps installed.

[Get started with the snap command](http://snapcraft.io/docs/core/usage)
