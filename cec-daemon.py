#!/usr/bin/python3
import pexpect, subprocess
import sys, traceback, time
from wakeonlan import send_magic_packet

def sendKey(key):
    subprocess.call(['xdotool', 'key', key])

def turnOnTv(p):
    p.sendline('on 0.0.0.0')
    p.sendline('on 0.0.0.0')
    p.sendline('on 0.0.0.0')
    print("turned tv on")

def printOutput(p):
    while True:
        output = p.stdout.readline()
        if p.poll() is not None and output == '':
            break
        if output:
            line = output
            print(line)

def turnOffTv(p):
    p.sendline('standby 0.0.0.0')
    p.sendline('standby 0.0.0.0')
    p.sendline('standby 0.0.0.0')
    print("turned tv off")

def awaitReady(p):
    p.expect("waiting for input")
    print("connection ready")

def hdmi(p, number):
    p.sendline("tx 1F:82:" + str(number) + "0:00")
    print("switched to hdmi " + str(number))

inputCodes = ["00", "01", "02", "03", "04", "47", "35", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]

def handleInput(p):
    print("awaiting input")
    while True:
        try:
            output = p.expect(["0f:36"] + [f'01:44:{i}' for i in inputCodes])
            if (output == 0):
                subprocess.call(['systemctl', 'suspend'])
            elif (output == 1):
                sendKey("space")
            elif (output == 2):
                sendKey("Up")
            elif (output == 3):
                sendKey("Down")
            elif (output == 4):
                sendKey("Left")
            elif (output == 5):
                sendKey("Right")
            elif (output == 6):
                sendKey("s")
            elif (output == 7):
                send_magic_packet('3c.7c.3f.d7.9c.8c')
                hdmi(p, 3)
            elif (output == 8):
                sendKey("0")
            elif (output == 9):
                sendKey("1")
            elif (output == 10):
                sendKey("2")
            elif (output == 11):
                sendKey("3")
            elif (output == 12):
                sendKey("4")
            elif (output == 13):
                sendKey("5")
            elif (output == 14):
                sendKey("6")
            elif (output == 15):
                sendKey("7")
            elif (output == 16):
                sendKey("8")
            elif (output == 17):
                sendKey("9")
        except pexpect.exceptions.TIMEOUT:
            pass

def main():
    process = pexpect.spawn('cec-client')
    try:
        awaitReady(process)
        turnOnTv(process)
        handleInput(process)
    except KeyboardInterrupt:
        turnOffTv(process)
    except Exception:
        traceback.print_exc(file=sys.stdout)
    process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    main()


