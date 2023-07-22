import json
import os


class Settings(dict):
    def __init__(self, configFilePath):
        self.configFilePath = os.path.expanduser(configFilePath)
        if os.path.isfile(self.configFilePath):
            configFile = open(self.configFilePath, "r")
            settings = json.load(configFile)
            configFile.close()
        else:
            settings = {
                "protocol": "tcp",  # tcp | upd
                "serverConnectionType": "-f",  # fastest | secureCore | peerToPeer | Tor
            }
        super().__init__(settings)

    def update(self, vals):
        super().update(vals)
        configFile = open(self.configFilePath, "w")
        json.dump(self, configFile)
        configFile.close()
