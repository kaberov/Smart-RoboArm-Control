import SmartArm as Dbt


# --Main Program--
def main():
    ctrl_bot = Dbt.SmartArm(0, -200, 150)  # Create DoBot Class Object with home position x,y,z
    ctrl_bot.ptp_jump(-120, -178, 50, 110, -185, 50)
    ctrl_bot.disconnect()


if __name__ == "__main__":
    main()
