### First boot

  1. The system will boot then become ready to configure
  2. The device will display the prompt “Press enter to configure”
  3. Press enter then select “Start” to begin configuring your network and an administrator account. Follow the instructions on the screen, you will be asked to configure your network and enter your Ubuntu SSO credentials
  4. At the end of the process, you will see **your credentials to access your Ubuntu Core machine**:

        This device is registered to <Ubuntu SSO email address>.
        Remote access was enabled via authentication with the SSO user <Ubuntu SSO user name>
        Public SSH keys were added to the device for remote access.

#### User login

Once setup is done, you can login with SSH into Ubuntu Core, from a machine on
the same network, using the following command:

    ssh <Ubuntu SSO user name>@<device IP address>

The user name is your Ubuntu SSO user name, it has been reminded to you at the end of the account configuration step.

##### First boot tips

  * During setup,` console-conf` will download the SSH key registered with your Store account and configure it so you can log into the device via `ssh <Ubuntu SSO account name>@<device IP address>` without a password.
  * There is no default `ubuntu` user on these images, but you can run `sudo passwd <account name>` to set a password in case you need a local console login.

### Install and develop snaps

Your board is ready to have snaps installed &mdash; [get started with the `snap` command](http://snapcraft.io/docs/core/usage)

You can install a classic Ubuntu environment on top of Ubuntu Core to have a fully-fledged development environment and [develop snaps on target &rsaquo;](/core/get-started/developer-setup)
