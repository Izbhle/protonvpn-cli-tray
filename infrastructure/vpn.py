import subprocess


def activateVpn(options):
    subprocess.run(
        ["protonvpn-cli", "c"] + options, stdout=subprocess.PIPE
    ).stdout.decode("utf-8")


def deactivateVpn():
    subprocess.run(["protonvpn-cli", "d"], stdout=subprocess.PIPE).stdout.decode(
        "utf-8"
    )


def getVpnStatus():
    nets = subprocess.Popen(("nmcli", "c", "show", "--active"), stdout=subprocess.PIPE)
    vpns = subprocess.run(
        ("grep", "-i", "vpn"), stdin=nets.stdout, stdout=subprocess.PIPE
    )
    nets.wait()
    if vpns.stdout == None:
        return "disconnected"
    vpnList = vpns.stdout.decode("utf-8").splitlines()
    hasKillSwitch = False
    hasLeakProtection = False
    hasProtonVPN = False
    for vpn in vpnList:
        if vpn.startswith("pvpn-killswitch"):
            hasKillSwitch = True
        if vpn.startswith("pvpn-ipv6leak-protection"):
            hasLeakProtection = True
        if vpn.startswith("Proton VPN"):
            hasProtonVPN = True
    if hasProtonVPN:
        return "connected"
    if hasKillSwitch or hasLeakProtection:
        return "no-network"
    return "disconnected"
