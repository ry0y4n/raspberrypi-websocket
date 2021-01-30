# pip install websocket-client
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

import RPi.GPIO as GPIO
import time

import wiringpi as wp

# SPI channel (0 or 1)
SPI_CH = 0

# SPI speed (hz)
SPI_SPEED = 1000000

# GPIO number
LED_PIN = 25

# threshold
THRESHOLD = 200

# setup
wp.wiringPiSPISetup (SPI_CH, SPI_SPEED)
wp.wiringPiSetupGpio()
wp.pinMode(LED_PIN, wp.GPIO.OUTPUT)

GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
gp_out = 4
GPIO.setup(gp_out, GPIO.OUT)
# motor = GPIO.PWM(gp_out, 50)
# motor.start(0.0)

class Websocket_Client():

    def __init__(self, host_addr):

        # デバックログの表示/非表示設定
        websocket.enableTrace(True)

        self.flag = True

        # WebSocketAppクラスを生成
        # 関数登録のために、ラムダ式を使用
        self.ws = websocket.WebSocketApp(host_addr,
            on_message = lambda ws, msg: self.on_message(ws, msg),
            on_error   = lambda ws, msg: self.on_error(ws, msg),
            on_close   = lambda ws: self.on_close(ws))
        self.ws.on_open = lambda ws: self.on_open(ws)

    # メッセージ受信に呼ばれる関数
    def on_message(self, ws, message):
        print("receive : {}".format(message))
        GPIO.setmode(GPIO.BCM)

        gp_out = 4
        GPIO.setup(gp_out, GPIO.OUT)
        motor = GPIO.PWM(gp_out, 50)
        motor.start(0.0)

        if self.flag:
            motor.ChangeDutyCycle(4.0)
            self.flag = not self.flag
            print(self.flag)
        else:
            motor.ChangeDutyCycle(5.5)
            self.flag = not self.flag
            print(self.flag)
        time.sleep(0.5)
        GPIO.cleanup()

    # エラー時に呼ばれる関数
    def on_error(self, ws, error):
        print(error)

    # サーバーから切断時に呼ばれる関数
    def on_close(self, ws):
        print("### closed ###")

    # サーバーから接続時に呼ばれる関数
    def on_open(self, ws):
        thread.start_new_thread(self.run, ())

    # サーバーから接続時にスレッドで起動する関数
    def run(self, *args):
        while True:
            buffer = 0x6800
            buffer = buffer.to_bytes(2,byteorder='big')
            wp.wiringPiSPIDataRW(SPI_CH, buffer)
            value = (buffer[0]*256+buffer[1]) & 0x3ff
            if value > THRESHOLD:
                print(value)
                time.sleep(1.0)
                self.ws.send(str(value))
            time.sleep(1.0)
            # input_data = input("send data:")
            # self.ws.send(input_data)
    
        self.ws.close()
        print("thread terminating...")
    
    # websocketクライアント起動
    def run_forever(self):
        self.ws.run_forever()


# # SPI channel (0 or 1)
# SPI_CH = 0

# # SPI speed (hz)
# SPI_SPEED = 1000000

# # GPIO number
# LED_PIN = 25

# # threshold
# THRESHOLD = 200

# # setup
# wp.wiringPiSPISetup (SPI_CH, SPI_SPEED)
# wp.wiringPiSetupGpio()
# wp.pinMode(LED_PIN, wp.GPIO.OUTPUT)

# GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BCM)
# gp_out = 4
# GPIO.setup(gp_out, GPIO.OUT)
# motor = GPIO.PWM(gp_out, 50)
# motor.start(0.0)

HOST_ADDR = "wss://websocket-momosuke.an.r.appspot.com/chat"
ws_client = Websocket_Client(HOST_ADDR)
ws_client.run_forever()

