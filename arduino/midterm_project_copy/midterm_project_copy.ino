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

/*=====Import header files=====*/
#include "RFID.h"
#include "bluetooth_copy.h"
#include "node.h"
#include "track_copy.h"
/*=====Import header files=====*/

/*============setup============*/
void setup() {
    BT.SETUP();
    track.SETUP();

    // RFID initial
    SPI.begin();
    mfrc522.PCD_Init();

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

/*===========================initialize variables===========================*/
int l2 = 0, l1 = 0, m0 = 0, r1 = 0, r2 = 0;  // 紅外線模組的讀值(0->white,1->black)
int _Tp = 150;                                // set your own value for motor power
double last_error = 0.0; 
bool state = false;     // set state to false to halt the car, set state to true to activate the car
BluetoothClass::BT_CMD _cmd = BluetoothClass::NOTHING;  // enum for bluetooth message, reference in bluetooth.h line 2
/*===========================initialize variables===========================*/

/*===========================declare function prototypes===========================*/
void Search();    // search graph
void SetState();  // switch the state
/*===========================declare function prototypes===========================*/

/*===========================define function===========================*/
void loop() {
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
        byte& idSize = mfrc522.uid.size;
        rfid(idSize);
        byte* uid = rfid(idSize);
        BT.send_byte(uid, idSize); // Send the UID over Bluetooth
    }
    /*
    if (!state)
        track.MotorWriting(0, 0);
    else
        Search();
    // BTtest();  
    SetState();
    */
}

/*
void BTtest() {
    _cmd = ask_BT(); // Get command from bluetooth
    
    switch(_cmd) {
        case forward:       
            Serial.println("FORWARD");
            track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
            delay(150);
            track.MotorWriting(0,0);
            break;
        case backward:
            Serial.println("BACKWARD");
            old_u_turn();
            track.MotorWriting(0,0);
            break;
        case rightTurn:
            Serial.println("RIGHT");
            old_quarter_circle_R();
            track.MotorWriting(0,0);
            break;
        case leftTurn:
            Serial.println("LEFT");
            old_quarter_circle_L();
            track.MotorWriting(0,0);
            break;
            
        case NOTHING:
            break;
    }

    delay(1000);
    track.MotorWriting(0, 0);
    // 2. Change state if need
}
*/

void SetState() {
    _cmd = BT.ask_BT(); // Get command from bluetooth

    l2 = digitalRead(IRpin_LL);
    l1 = digitalRead(IRpin_L);
    m0 = digitalRead(IRpin_M);
    r1 = digitalRead(IRpin_R);
    r2 = digitalRead(IRpin_RR);

    bool on_node = 0;   // 用來記錄node
    switch(_cmd) {
        case BluetoothClass::Forward:       
            Serial.println("FORWARD");
            /*
            track.MotorWriting(_Tp, _Tp); 
            delay(500);
            track.MotorWriting(0, 0);
            */

            /*
            while(!(on_node && l2 == 0 && r2 == 0)){
                track.Tracking(l2, l1, m0, r1, r2);
                if (on_node==0 && l2 && l1 && m0 && r1 && r2) {
                    on_node = 1;
                }
            }
            */
            
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));   
                rfid(mfrc522.uid.size);
                if (on_node==0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }

            track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
            delay(150);
            track.MotorWriting(0,0);
            break;
        case BluetoothClass::Backward:
            Serial.println("BACKWARD");
            track.OldUTurn();
            /*
            track.MotorWriting(_Tp, _Tp); 
            delay(500);
            track.MotorWriting(0, 0);
            */
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
                rfid(mfrc522.uid.size);
                if (on_node == 0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }
            track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
            delay(100);
            track.MotorWriting(0, 0);
            break;
        case BluetoothClass::RightTurn:
            Serial.println("RIGHT");
            track.OldQuarterCircleR();
      
             /*
            track.MotorWriting(_Tp, _Tp); 
            delay(500);
            track.MotorWriting(0, 0);
            */
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
                rfid(mfrc522.uid.size);
                if (on_node==0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }
            track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
            delay(150);
            track.MotorWriting(0,0);
            break;
        case BluetoothClass::LeftTurn:
            Serial.println("LEFT");
            track.OldQuarterCircleL();
             /*
            track.MotorWriting(_Tp, _Tp); 
            delay(500);
            track.MotorWriting(0, 0);
            */
            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)){
                track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
                rfid(mfrc522.uid.size);
                if (on_node==0 && digitalRead(IRpin_LL) && digitalRead(IRpin_L) && digitalRead(IRpin_M) && digitalRead(IRpin_R) && digitalRead(IRpin_RR)) {
                    on_node = 1;
                }
            }
            track.Tracking(digitalRead(IRpin_LL), digitalRead(IRpin_L), digitalRead(IRpin_M), digitalRead(IRpin_R), digitalRead(IRpin_RR));
            delay(150);
            track.MotorWriting(0,0);
            break;
            
        case BluetoothClass::NOTHING:
            break;
    }

    delay(1000);
    track.MotorWriting(0, 0);
    // 2. Change state if need
}

void Search() {
    // TODO: let your car search graph(maze) according to bluetooth command from python code
}
/*===========================define function===========================*/