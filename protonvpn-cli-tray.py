#!/usr/bin/env python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from infrastructure.lib.subprocess_watcher import SubprocessWatcher
from infrastructure.vpn import activateVpn, deactivateVpn, getVpnStatus
from infrastructure.settings import Settings

configFilePath = "~/.config/protonvpn/protonvpn_cli_tray_config.json"

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def updateSettingsAndActions(self, settingsKey, settingsValue, actionsAndValues):
        self.settings.update({settingsKey: settingsValue})
        for action, value in actionsAndValues:
            action.setChecked(settingsValue == value)

    def addActionsMultiSelect(self, actionsAndValues, settingsKey):
        for action, value in actionsAndValues:
            action.setCheckable(True)
            action.setChecked(self.settings[settingsKey] == value)
            action.triggered.connect(lambda state, x=value: self.updateSettingsAndActions(settingsKey, x, actionsAndValues))

    def __init__(self, parent=None):
        # Load possible tray icons
        self.icons = {
            'connected': QtGui.QIcon(r'./assets/icons/vpn-connected.svg'),
            'disconnected': QtGui.QIcon(r'./assets/icons/vpn-disconnected.svg'),
            'no-network': QtGui.QIcon(r'./assets/icons/vpn-no-network.svg'),
        }
        # Load settings file or start with defaults
        self.settings = Settings(configFilePath)
        QtWidgets.QSystemTrayIcon.__init__(self, self.icons[getVpnStatus()], parent)
        # Define context menu
        menu = QtWidgets.QMenu(parent)
        menu.addSection("Protocol")
        setProtocolTcp = menu.addAction("TCP")
        setProtocolUdp = menu.addAction("UDP")
        self.addActionsMultiSelect([[setProtocolUdp, 'udp'], [setProtocolTcp, 'tcp']], 'protocol')
        menu.addSeparator()
        menu.addSection("Server")
        setServerFastest = menu.addAction("Fastest")
        setServerP2P = menu.addAction("P2P")
        setServerTor = menu.addAction("Tor")
        setServerSecureCore = menu.addAction("Secure Core")
        self.addActionsMultiSelect([
            [setServerFastest, '-f'],
            [setServerP2P, '--p2p'],
            [setServerTor, '--tor'],
            [setServerSecureCore, '--sc']
        ], 'serverConnectionType')
        menu.addSeparator()
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        self.setToolTip("Proton VPN")
        exitAction.triggered.connect(self.exit)
        self.activated.connect(self.toggleAction)
        self.updateIconThread = SubprocessWatcher(('nmcli', 'monitor'), self.updateIcon)
        self.updateIconThread.start()

    def updateIcon(self):
        self.setIcon(self.icons[getVpnStatus()])

    def toggleAction(self):
        status = getVpnStatus()
        if status == 'connected':
            self.deactivateAction()
        else:
            self.activateAction()

    def activateAction(self):
        activateVpn([self.settings['serverConnectionType'], '-p', self.settings['protocol']])

    def deactivateAction(self):
        deactivateVpn()

    def exit(self):
        deactivateVpn()
        self.updateIconThread.exit()
        QtCore.QCoreApplication.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(w)

    trayIcon.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
