import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO를 설정
import time #time 라이브러리 설정

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #GPIO PIN 설정


GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #STOP SWITCH PIN: 17 INPUT 설정
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #STOP SWITCH2 PIN: 25 INPUT 설정

count = 0;

while True:
    input_state=GPIO.input(26) #input_state 변수: GPIO PIN 17번(스위치) 입력
    input_state_1=GPIO.input(25) #input_state 변수: GPIO PIN 17번(스위치) 입력
     
    if input_state==False:  #STOP SWITCH_2가 눌렸을 때
        if count == 0:
            print('FALSE')
            count = 1 
    elif input_state==True:
        if count == 1:
            print('human detect')
            count = 0
    
            
              
   
               

