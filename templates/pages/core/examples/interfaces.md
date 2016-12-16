----
title: Interfaces
description: Interface examples
----

# Interface examples

Interfaces allow snaps to communicate or share resources according to a protocol defined by the interface. For example, the serial port interface is offered by the Ubuntu Core snap to let other snaps access the serial port of your board or computer.

[For more information about creating interfaces](http://docs.ubuntu.com/core/en/guides/build-device/interfaces)

[For more information about using interfaces in your snap](http://snapcraft.io/docs/reference/interfaces).


##Serial port interface
Offered by the Ubuntu Core snap to give your snap access to the serial port. Use this as a reference when you build your own interface.

[View the serial port interface code](https://github.com/snapcore/snapd/blob/98c8e937625ce3134cf17025d8f0eb3e1016259a/interfaces/builtin/serial_port.go)

##Bluez interface
Offered by the Bluez snap to give your snap access to Bluetooth.

[View the Bluez port interface code](http://bazaar.launchpad.net/~ssweeny/bluez/snappy-interface/files)

##Camera interface
A basic implementation offered by the Ubuntu Core snap to give your snap access to the camera.

[View the camera interface code](https://github.com/snapcore/snapd/blob/98c8e937625ce3134cf17025d8f0eb3e1016259a/interfaces/builtin/camera.go)
