/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

// #define DEBUG  // debug flag

// For RFID
#include <MFRC522.h>
#include <SPI.h>

/*===========================define pin & create module object================================*/
// BlueTooth
// BT connect to Serial1 (Hardware Serial)
// Mega               HC05
// Pin  (Function)    Pin
// 18    TX       ->  RX
// 19    RX       <-  TX
// TB6612

// IR
#define IRpin_LL 40
#define IRpin_L 38
#define IRpin_M 36
#define IRpin_R 34
#define IRpin_RR 32

// RFID
#define RST_PIN 9                 // 讀卡機的重置腳位
#define SS_PIN 53                  // 晶片選擇腳位
MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件
/*===========================define pin & create module object===========================*/

#include "bluetooth_copy.h"
#include "RFID.h"
#include "node.h"
#include "track_copy.h"

void setup() {
    BT.SETUP();
    track.SETUP();

    // RFID Initialization
    SPI.begin();
    mfrc522.PCD_Init();

    // IR sensors setup
    pinMode(IRpin_LL, INPUT);
    pinMode(IRpin_L, INPUT);
    pinMode(IRpin_M, INPUT);
    pinMode(IRpin_R, INPUT);
    pinMode(IRpin_RR, INPUT);
    
#ifdef DEBUG
    Serial.println("Start!");
#endif
}

/*===========================initialize variables===========================*/
int l2 = 0, l1 = 0, m0 = 0, r1 = 0, r2 = 0;  // 紅外線模組的讀值(0->white,1->black)
int _Tp = 150;                                // set your own value for motor power
double last_error = 0.0; 
bool state = false;     // set state to false to halt the car, set state to true to activate the car
bool RFID_scanned = false;
BluetoothClass::BT_CMD _cmd = BluetoothClass::NOTHING;  // enum for bluetooth message, reference in bluetooth.h line 2
/*===========================initialize variables===========================*/

/*===========================declare function prototypes===========================*/
void SetState();  // switch the state
/*===========================declare function prototypes===========================*/

/*===========================define function===========================*/
void loop() {
    if (!state) {
        track.MotorWriting(0, 0);
        if (BT.ask_BT() == BluetoothClass::Start) {
            state = true;
            Serial.print("Start cmd received!\n");
            BT.send_msg('g');
        }
    }
    else {
        SetState();
        // TODO: rfid early u turn
    }
}

void SetState() {
    _cmd = BT.ask_BT(); // Get command from bluetooth
    if (RFID_scanned) {
        RFID_scanned = false;
    }
    bool on_node = 0;   // 用來記錄是否在node上
    switch(_cmd) {
        case BluetoothClass::Forward:
            BT.send_msg('g');
            Serial.println("forward gotcha!");
            
            while (!(on_node && 
                    digitalRead(IRpin_LL) == 0 && 
                    digitalRead(IRpin_RR) == 0)) {
                
                track.Tracking(
                    digitalRead(IRpin_LL),
                    digitalRead(IRpin_L),
                    digitalRead(IRpin_M),
                    digitalRead(IRpin_R),
                    digitalRead(IRpin_RR)
                );
                
                if (DetectRFID()) {
                    RFID_scanned = true;
                    //BT.ask_BT(); // Clean cmd
                    //goto back;
                }

                if (on_node == 0 &&
                    NodeDetected(digitalRead(IRpin_LL),
                                digitalRead(IRpin_L),
                                digitalRead(IRpin_M),
                                digitalRead(IRpin_R),
                                digitalRead(IRpin_RR))) {
                    on_node = 1;
                }

            }

            track.MotorWriting(_Tp, _Tp);
            track.SlowDown();
            break;
        case BluetoothClass::RightTurn:
            BT.send_msg('g');
            Serial.println("right gotcha!");
            track.QuarterCircleRight();
      
            while (!(on_node && 
                    digitalRead(IRpin_LL) == 0 && 
                    digitalRead(IRpin_RR) == 0)) {
                
                track.Tracking(
                    digitalRead(IRpin_LL),
                    digitalRead(IRpin_L),
                    digitalRead(IRpin_M),
                    digitalRead(IRpin_R),
                    digitalRead(IRpin_RR)
                );
                
                if (DetectRFID()) {
                    RFID_scanned = true;
                    //BT.ask_BT(); // Clean cmd
                    //goto back;
                }

                if (on_node == 0 &&
                    NodeDetected(digitalRead(IRpin_LL),
                                digitalRead(IRpin_L),
                                digitalRead(IRpin_M),
                                digitalRead(IRpin_R),
                                digitalRead(IRpin_RR))) {
                    on_node = 1;
                }
            }

            track.MotorWriting(_Tp, _Tp);
            track.SlowDown();
            break;
        case BluetoothClass::LeftTurn:
            BT.send_msg('g');
            Serial.println("left gotcha!");
            track.QuarterCircleLeft();

            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)) {
                track.Tracking(
                    digitalRead(IRpin_LL),
                    digitalRead(IRpin_L),
                    digitalRead(IRpin_M),
                    digitalRead(IRpin_R),
                    digitalRead(IRpin_RR)
                );
                if (DetectRFID()) {
                    RFID_scanned = true;
                    //BT.ask_BT(); // Clean cmd
                    //goto back;
                }
                if (on_node == 0 &&
                    NodeDetected(digitalRead(IRpin_LL),
                                digitalRead(IRpin_L),
                                digitalRead(IRpin_M),
                                digitalRead(IRpin_R),
                                digitalRead(IRpin_RR))) {
                    on_node = 1;
                }
            }

            track.MotorWriting(_Tp, _Tp);
            track.SlowDown();
            break;

        case BluetoothClass::Backward:
        back:            
            BT.send_msg('g');
            Serial.println("backward gotcha!");
            track.UTurn();

            DetectRFID();

            while(!(on_node && digitalRead(IRpin_LL) == 0 && digitalRead(IRpin_RR) == 0)) {
                track.Tracking(
                    digitalRead(IRpin_LL),
                    digitalRead(IRpin_L),
                    digitalRead(IRpin_M),
                    digitalRead(IRpin_R),
                    digitalRead(IRpin_RR)
                );
                if (DetectRFID()) {
                    RFID_scanned = true;
                }
                if (on_node == 0 &&
                    NodeDetected(digitalRead(IRpin_LL),
                                digitalRead(IRpin_L),
                                digitalRead(IRpin_M),
                                digitalRead(IRpin_R),
                                digitalRead(IRpin_RR))) {
                    on_node = 1;
                }
            }
            track.MotorWriting(_Tp, _Tp);
            track.SlowDown();
            break;          
        case BluetoothClass::NOTHING:
            break;
    }
}

/*void BTtest() {
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
}*/