import RPi.GPIO as GPIO
import sys
from re import findall
from time import sleep
from subprocess import check_output


def get_temp():
    temp = check_output(["vcgencmd", "measure_temp"]).decode()
    temp = float(findall('\d+\.\d+', temp)[0])
    return(temp)


try:
    GPIO.setwarnings(False)
    tempOn = 50
    threshold = 10
    controlPin = 14
    pinState = False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(controlPin, GPIO.OUT, initial=0)
    while True:
        temp = get_temp()
        if temp > tempOn and not pinState or temp < tempOn - threshold and pinState:
            pinState = not pinState
            GPIO.output(controlPin, pinState)
        print(str(temp) + "  " + str(pinState))
        sleep(1)
except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except:
    print("Other Exception")
    print("--- Start Exception Data:")
    traceback.print_exc(limit=2, file=sys.stdout)
    print("--- End Exception Data:")
finally:
    print("CleanUp")
    GPIO.cleanup()
    print("End of program")
