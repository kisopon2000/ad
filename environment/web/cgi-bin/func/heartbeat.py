from launcher.rlauncher import RLauncher

class HeartbeatLauncher(RLauncher):
    def __init__(self):
        super(HeartbeatLauncher, self).__init__()
    def initialize(self):
        print("HeartbeatLauncher.initialize")
        return 0
    def run(self):
        print("HeartbeatLauncher.run")
        return 0
    def finalize(self):
        print("HeartbeatLauncher.finalize")
        return 0
