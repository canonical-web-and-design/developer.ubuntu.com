----
title: Examples
description: Reusable code snippets to speed up your Ubuntu Core development and deployment journey, from using interfaces to building a gadget snap.
----

# Examples

Here you can find example code and example implementations of the key Ubuntu Core components. This will help you build your own implementations and better understand how these key components are built. Read the code or branch it to get started with your own projects.

## Run a kiosk with Ubuntu Core
The Mir display server can be used to create a lightweight user interface on a board running Ubuntu Core.

[See the kiosk example &rsaquo;](/core/examples/snaps-on-mir)

##Hooks
A hook is an executable file that is called under a certain pre-configured condition. For example, a hook can ensure a database update occurs when a snap gets upgraded.

[See examples for hooks &rsaquo;](/core/examples/hooks)

##Interfaces
Interfaces allow snaps to communicate or share resources according to a protocol defined by the interface. For example, the serial port interface is offered by the Ubuntu Core snap to let other snaps access the serial port of your board or computer.

[See examples for interfaces ›](/core/examples/interfaces)

##Gadget snaps
A gadget snap is responsible for defining and manipulating the system properties specific to one or more devices. Here are a few examples of gadget snaps for various devices and development boards.

[See examples for gadgets ›](/core/examples/gadget-snaps)

##Assertions
Assertions are digitally signed documents that express a fact or policy by a particular authority about a particular object in the snap universe. For example a user assertion can be used by a system administrator to create users on a specific device.

[See examples for assertions ›](/core/examples/assertions)
