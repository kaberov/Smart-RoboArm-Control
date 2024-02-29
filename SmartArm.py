import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}


# Main control class for the DoBot Magician.
class SmartArm:
    def __init__(self, home_x=0, home_y=0, home_z=0):
        # self.suction = False
        self.picking = False
        self.api = dType.load()
        self.homeX = home_x
        self.homeY = home_y
        self.homeZ = home_z
        self.connected = False
        self.connect()

    def __del__(self):
        self.disconnect()

    # Attempts to connect to the dobot
    def connect(self):
        if self.connected:
            print("You're already connected")
        else:
            state = dType.ConnectDobot(self.api, "", 115200)[0]
            if state == dType.DobotConnect.DobotConnect_NoError:
                print("Connect status:", CON_STR[state])
                dType.SetQueuedCmdClear(self.api)

                # dType.SetHOMEParams(self.api, self.homeX, self.homeY, self.homeZ, 0, isQueued=1)
                dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued=0)
                dType.SetPTPCommonParams(self.api, 50, 25, 1)
                dType.SetPTPJumpParams(self.api, 75, 150, 1)

                # dType.SetHOMECmd(self.api, temp=0, isQueued=1)
                self.move_home()

                self.connected = True
            else:
                print("Unable to connect")
                print("Connect status:", CON_STR[state])
        return self.connected

    # Returns to home location and then disconnects
    def disconnect(self):
        self.move_home()
        dType.DisconnectDobot(self.api)

    # Returns to home location
    def move_home(self):
        last_index = dType.SetPTPCmd(self.api, dType.PTPMode.PTPJUMPXYZMode, self.homeX, self.homeY, self.homeZ, 0)[0]
        self.command_delay(last_index)

    # Delays commands
    def command_delay(self, last_index):
        dType.SetQueuedCmdStartExec(self.api)
        while last_index > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(200)
        dType.SetQueuedCmdStopExec(self.api)

    # main jump and grup function
    def ptp_jump(self, x1, y1, z1, x2, y2, z2):
        last_index = dType.SetEndEffectorGripper(self.api, True, False, isQueued=1)[0]
        last_index = dType.SetPTPCmd(self.api, dType.PTPMode.PTPJUMPXYZMode, x1, y1, z1, 0, isQueued=1)[0]
        last_index = dType.SetEndEffectorGripper(self.api, True, True, isQueued=1)[0]
        last_index = dType.SetWAITCmd(self.api, 1, 1)
        last_index = dType.SetPTPCmd(self.api, dType.PTPMode.PTPJUMPXYZMode, x2, y2, z2, 0, isQueued=1)[0]
        last_index = dType.SetEndEffectorGripper(self.api, True, False, isQueued=1)[0]
        last_index = dType.SetWAITCmd(self.api, 1, 1)
        last_index = dType.SetPTPCmd(self.api, dType.PTPMode.PTPJUMPXYZMode, self.homeX,
                                     self.homeY, self.homeZ, 0, isQueued=1)[0]
        last_index = dType.SetEndEffectorGripper(self.api, False, False, isQueued=1)[0]

        self.command_delay(last_index)
