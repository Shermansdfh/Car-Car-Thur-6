/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

#define DEBUG  // debug flag

#include <SoftwareSerial.h>
// for RFID
#include <MFRC522.h>
#include <SPI.h>

/*===========================define pin & create module object================================*/
// BlueTooth
// BT connect to Serial1 (Hardware Serial)
// Mega               HC05
// Pin  (Function)    Pin
// 18    TX       ->  RX
// 19    RX       <-  TX
// TB6612, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
// TODO: 請將腳位寫入下方

// Bluetooth
#define rxPIN 19
#define txPIN 18 

// Motor
#define MotorL_I1 2     // 定義 A1 接腳（右）
#define MotorL_I2 3     // 定義 A2 接腳（右）
#define MotorL_PWML 11  // 定義 ENA (PWM調速) 接腳
#define MotorR_I3 5     // 定義 B1 接腳（左）
#define MotorR_I4 6     // 定義 B2 接腳（左）
#define MotorR_PWMR 12  // 定義 ENB (PWM調速) 接腳

// IR
#define IRpin_LL 40
#define IRpin_L 38
#define IRpin_M 36
#define IRpin_R 34
#define IRpin_RR 32

// RFID, 請按照自己車上的接線寫入腳位
#define RST_PIN 9                 // 讀卡機的重置腳位
#define SS_PIN 53                  // 晶片選擇腳位
MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件
/*===========================define pin & create module object===========================*/

/*============setup============*/
void setup() {
    // bluetooth initialization
    Serial1.begin(9600);
    
    // Serial window
    Serial.begin(9600);
    
    // RFID initial
    SPI.begin();
    mfrc522.PCD_Init();
    
    // TB6612 pin
    pinMode(MotorL_I1, OUTPUT);
    pinMode(MotorL_I2, OUTPUT);
    pinMode(MotorR_I3, OUTPUT);
    pinMode(MotorR_I4, OUTPUT);
    pinMode(MotorL_PWML, OUTPUT);
    pinMode(MotorR_PWMR, OUTPUT);

    // tracking pin
    pinMode(IRpin_LL, INPUT);
    pinMode(IRpin_L, INPUT);
    pinMode(IRpin_M, INPUT);
    pinMode(IRpin_R, INPUT);
    pinMode(IRpin_RR, INPUT);
#ifdef DEBUG
    Serial.println("Start!");
#endif
}
/*============setup============*/

/*=====Import header files=====*/
#include "RFID.h"
#include "bluetooth.h"
#include "node.h"
#include "track.h"
/*=====Import header files=====*/

/*===========================initialize variables===========================*/
int l2 = 0, l1 = 0, m0 = 0, r1 = 0, r2 = 0;  // 紅外線模組的讀值(0->white,1->black)
int _Tp = 150;                                // set your own value for motor power
double last_error = 0; 
bool state = false;     // set state to false to halt the car, set state to true to activate the car
BT_CMD _cmd = NOTHING;  // enum for bluetooth message, reference in bluetooth.h line 2
/*===========================initialize variables===========================*/

/*===========================declare function prototypes===========================*/
void Search();    // search graph
void SetState();  // switch the state
/*===========================declare function prototypes===========================*/

/*===========================define function===========================*/
void loop() {
    /*
    rfid(mfrc522.uid.size);
    if (digitalRead(40) && digitalRead(38) && digitalRead(36) && digitalRead(34) && digitalRead(32)) {
        MotorWriting(0, 0);
    }
    else {
        tracking(digitalRead(40), digitalRead(38), digitalRead(36), digitalRead(34), digitalRead(32));
    }
    */
  
    if (!state)
        MotorWriting(0, 0);
    else
        Search();
    SetState();
}

void SetState() {
    _cmd = ask_BT(); // Get command from bluetooth
    bool on_node = 0;   // 用來記錄到了node
    switch(_cmd) {
        case forward:       
            Serial.println("FORWARD");
            /*
            MotorWriting(_Tp, _Tp); 
            delay(500);
            MotorWriting(0, 0);
            */
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
                if (on_node==0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }
            delay(100);
            MotorWriting(0,0);
            break;
        case backward:
            Serial.println("BACKWARD");
            uTurn();
            /*
            MotorWriting(_Tp, _Tp); 
            delay(500);
            MotorWriting(0, 0);
            */
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
                if (on_node==0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }
            delay(100);
            MotorWriting(0,0);
            break;
        case rightTurn:
            Serial.println("RIGHT");
            quarterCircleRight();
             /*
            MotorWriting(_Tp, _Tp); 
            delay(500);
            MotorWriting(0, 0);
            */
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
                if (on_node==0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }
            delay(100);
            MotorWriting(0,0);
            break;
        case leftTurn:
            Serial.println("LEFT");
            quarterCircleLeft();
             /*
            MotorWriting(_Tp, _Tp); 
            delay(500);
            MotorWriting(0, 0);
            */
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
                if (on_node==0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }
            delay(100);
            MotorWriting(0,0);
            break;
            
        case NOTHING:
            break;
    }

    delay(1000);
    MotorWriting(0, 0);
    // 2. Change state if need
}

void Search() {
    // TODO: let your car search graph(maze) according to bluetooth command from python code
}
/*===========================define function===========================*/
