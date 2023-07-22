# Proton VPN CLI Tray

Copyright (c) 2023 Fritz Stach

This repository is meant to provide a linux system integration for the Proton VPN CLI.

For licensing information see [COPYING](COPYING.md).

## Description
This is meant as a placeholder for the official Proton VPN Linux GUI that does not use excessive resources.
Basic settings (using P2P, Tor, Secure Core Servers or TCP vs UDP connections) can be configured in the tray (right click) menu.
Clicking the Tray icon toggles the VPN.

Proton VPN CLI commands and nm commands are exectued as shell commands, no Python API is necessary.

Current VPN status is fetched, by attaching a listener to `nmcli monitor`.
As a result the Tray does not use any CPU load while in Idle, and requires only 2.2MB of RAM.



### Dependencies:
| **Distro**                              | **Command**                                                                                                     |
|:----------------------------------------|:----------------------------------------------------------------------------------------------------------------|
|Fedora/CentOS/RHEL                       | `python3-qt5 protonvpn-cli` |
|Ubuntu/Linux Mint/Debian and derivatives | `python3-pyqt5 protonvpn-cli` |
|Arch Linux/Manjaro                       | `python3-pyqt5 protonvpn-cli` |

## Installation

Install the dependencies (can also use pip3 to install pyqt)

Download the repository, make `protonvpn-cli-tray.py` executable and add it to autostart.

Any other way to launch the tray is fine as well.