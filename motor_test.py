import wiringpi as GPIO
import sys
import time
 
class Servo:
    def __init__(self, pin):
        self.PIN = pin
        GPIO.wiringPiSetupGpio()    # 上図 pin(BOARD) の番号でピン指定するモード
        GPIO.pinMode(self.PIN, 2)  # 出力ピンとして指定
        GPIO.pwmSetMode(0)          # 0Vに指定
        GPIO.pwmSetRange(1024)      # レンジを0～1024に指定
        GPIO.pwmSetClock(375)

    def round(self, angle):
        if(-90 <= angle and angle <= 90):
            move_deg = int((9.5*angle/180 + 2.5)*(1024/100))
            GPIO.pwmWrite(self.PIN, angle)

servo = Servo(2)
servo.round(30)
servo.round(0)
