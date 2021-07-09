import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO를 설정
import time #time 라이브러리 설정

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #GPIO PIN 설정

GPIO.setup(18, GPIO.OUT) #PWM GPIO PIN: 18 OUTPUT 설정
GPIO.setup(23, GPIO.OUT) #ENABLE GPIO PIN: 23 OUTPUT 설정
GPIO.setup(24, GPIO.OUT) #DIRECTION GPIO PIN: 24 OUTPUT 설정
GPIO.setup(27, GPIO.OUT) #BRAKE GPIO PIN: 27 OUTPUT 설정

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Return Flag SWITCH PIN: 4 INPUT 설정
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #STOP SWITCH_2 PIN: 17 INPUT 설정
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Mask Detection Flag SWITCH PIN: 22 INPUT 설정
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #STOP SWITCH PIN: 25 INPUT 설정

#오픈 컬렉터이므로 HIGH, LOW가 반대
GPIO.output(23,GPIO.LOW) #ENABLE GPIO PIN: 23 True 출력
GPIO.output(24,GPIO.LOW) #DIRECTION PIN: 24 True 출력 LOW:CW HIGH:CCW
GPIO.output(27,GPIO.LOW) #BRAKE GPIO PIN: 27 True 출력

#무부하 5800rpm=96.67Hz, 정격 4000rpm=66.66Hz 오차범위 10%
myPwm=GPIO.PWM(18, 100) #GPIO PIN 18 Frequency 100Hz
myPwm.start(0) #반드시 실행 PWM Start(정지)
MaskFlag=0

while True:
    MaskFlag=int(input('Select Motor Direction 1.CW 2.CCW: ')) #int를 사용하여 입력 값을 정수로 변환

    if MaskFlag==1: #Mask Detection이 일어났을 때
        GPIO.output(24,GPIO.LOW) #DIRECTION PIN: 24 True 출력 LOW:CW HIGH:CCW
        
        for i in range(0,220,1): #무부하시 12V일 때, 1400~1500사이 24V일 때, 900~1000사이
                myPwm.ChangeDutyCycle(50)
                time.sleep(0.01)
        
        myPwm.ChangeDutyCycle(0) #Duty비 0%로 동작(정지)
        MaskFlag=0 #Mask Flag 1으로 설정
        time.sleep(0.1) #time 함수 sleep 0.1s

        
    if MaskFlag==2: #Mask Detection으로 차단 이후, 차단봉을 원래 위치로 위치시킬 때
        GPIO.output(24,GPIO.HIGH) #DIRECTION PIN: 24 False 출력 LOW:CW HIGH:CCW

        for i in range(0,220,1): #무부하시 12V일 때, 1400~1500사이 24V일 때, 900~1000사이
                myPwm.ChangeDutyCycle(50)
                time.sleep(0.01)
        
        myPwm.ChangeDutyCycle(0) #Duty비 0%로 동작
        MaskFlag=0 #Return Flag 1로 설정
        time.sleep(0.1) #time 함수 sleep 0.1s

time.sleep(0.1) #time 함수 sleep 0.1s

GPIO.cleanup() #동작 후 반드시 GPIO 설정 초기화(cleanup)