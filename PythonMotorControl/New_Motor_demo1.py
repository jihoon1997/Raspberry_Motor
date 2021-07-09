import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO를 설정
import time #time 라이브러리 설정

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #GPIO PIN 설정

GPIO.setup(18, GPIO.OUT) #PWM GPIO PIN: 18 OUTPUT 설정
GPIO.setup(23, GPIO.OUT) #ENABLE GPIO PIN: 23 OUTPUT 설정
GPIO.setup(24, GPIO.OUT) #DIRECTION GPIO PIN: 24 OUTPUT 설정
GPIO.setup(27, GPIO.OUT) #BRAKE GPIO PIN: 27 OUTPUT 설정

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #STOP SWITCH PIN: 17 INPUT 설정
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #STOP SWITCH2 PIN: 25 INPUT 설정

#오픈 컬렉터이므로 HIGH, LOW가 반대
GPIO.output(23,GPIO.LOW) #ENABLE GPIO PIN: 23 True 출력
GPIO.output(24,GPIO.LOW) #DIRECTION PIN: 24 True 출력 LOW:CW HIGH:CCW
GPIO.output(27,GPIO.LOW) #BRAKE GPIO PIN: 27 True 출력

#무부하 5800rpm, 정격 4000rpm 기어비 1/104
myPwm=GPIO.PWM(18, 100) #GPIO PIN 18 Frequency 100Hz
myPwm.start(0) #반드시 실행 PWM Start(정지)
MaskFlag=0 #Mask Detection Flag 0:No 1:Yes CW방향

while True:
    MaskFlag=int(input('Select Motor Direction 1.CW 2.CCW: ')) #int를 사용하여 입력 값을 정수로 변환

    if MaskFlag==1: #Mask Detection이 일어났을 때
        GPIO.output(24,GPIO.LOW) #DIRECTION PIN: 24 True 출력 LOW:CW HIGH:CCW
        start_time=time.time() #MaskFlag 1 발생 시 현재 시간(초) 얻어오기
        max_time=start_time+2.3 #max_time(동작시간)을 2.6초로 설정
        myPwm.ChangeDutyCycle(50) #Duty비 50%로 동작

        while True:
            input_state=GPIO.input(17) #input_state 변수: GPIO PIN 17번(스위치) 입력

            if time.time()>max_time:
                myPwm.ChangeDutyCycle(0) #Duty비 0%로 동작
                MaskFlag=0 #Mask Flag 0으로 설정
                time.sleep(0.1) #time 함수 sleep 0.1s
                break

            if input_state==False:
                myPwm.ChangeDutyCycle(0) #Duty비 0%로 동작(정지)
                MaskFlag=0 #Mask Flag 0으로 설정
                time.sleep(0.1) #time 함수 sleep 0.1s
                break
        
    if MaskFlag==2: #Mask Detection으로 차단 이후, 차단봉을 원래 위치로 위치시킬 때
        GPIO.output(24,GPIO.HIGH) #DIRECTION PIN: 24 False 출력 LOW:CW HIGH:CCW
        start_time=time.time() #MaskFlag 2 발생 시 현재 시간(초) 얻어오기
        max_time2=start_time+2.3 #max_time(동작시간)을 2.6초로 설정
        myPwm.ChangeDutyCycle(50) #Duty비 50%로 동작


        while True:
            input_state=GPIO.input(25) #input_state 변수: GPIO PIN 25번(스위치) 입력

            if time.time()>=max_time2:
                myPwm.ChangeDutyCycle(0) #Duty비 0%로 동작
                MaskFlag=0 #Mask Flag 0으로 설정
                time.sleep(0.1) #time 함수 sleep 0.1s
                break

            if input_state==False:  #STOP SWITCH_2가 눌렸을 때
                myPwm.ChangeDutyCycle(0) #Duty비 0%로 동작
                MaskFlag=0 #Mask Flag 1로 설정
                time.sleep(0.1) #time 함수 sleep 0.1s
                break
    

time.sleep(0.1) #time 함수 sleep 0.1s
GPIO.cleanup() #동작 후 반드시 GPIO 설정 초기화(cleanup)