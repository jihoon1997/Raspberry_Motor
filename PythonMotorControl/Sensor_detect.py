import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO를 설정
import time #time 라이브러리 설정

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #GPIO PIN 설정

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #STOP SWITCH2 PIN: 26 INPUT 설정

while True:
    input_state=GPIO.input(26) #input_state 변수: GPIO PIN 26번(스위치) 입력

    # Sensor는 Detect시 Low No Detect시 High를 출력
    if input_state==True: #Sensor Detection이 일어나지 않았을 때
        print ('No Detect')
    elif input_state==False: #Sensor Detection이 일어났을 때
        print ('Human Detect')

time.sleep(0.1) #time 함수 sleep 0.1s
GPIO.cleanup() #동작 후 반드시 GPIO 설정 초기화(cleanup)