from launcher.rlweb import RLWeb

class RLauncher(RLWeb):
    def __init__(self):
        super(RLauncher, self).__init__()
    def atstart(self):
        # �g�[�N���擾
        token = self.parseToken()
        if token == None:
            return 1
        else:
            return 0
        return 0
    def initialize(self):
        print("RLauncher.initialize")
        return 0
    def run(self):
        print("RLauncher.run")
        return 0
    def finalize(self):
        print("RLauncher.finalize")
        return 0
    def atend(self):
        return 0
