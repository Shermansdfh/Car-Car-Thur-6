/*****************************************************************************/
// File [bluetooth.cpp]
// Author [Erik Kuo]
// Synopsis [Implementation of bluetooth communication functions]
// Modify [2020/03/27 Erik Kuo]
/*****************************************************************************/

#include "track_copy.h"
#include <Arduino.h>


const int MotorL_I1 = 2;     
const int MotorL_I2 = 3; 
const int MotorL_PWML = 11;
const int MotorR_I3 = 5;    
const int MotorR_I4 = 6; 
const int MotorR_PWMR = 12;

TrackClass::TrackClass() {}

void TrackClass::SETUP() {
    pinMode(MotorL_I1, OUTPUT);
    pinMode(MotorL_I2, OUTPUT);
    pinMode(MotorR_I3, OUTPUT);
    pinMode(MotorR_I4, OUTPUT);
    pinMode(MotorL_PWML, OUTPUT);
    pinMode(MotorR_PWMR, OUTPUT);
}

void TrackClass::MotorWriting(double vL, double vR) {
    // use TB6612 to control motor voltage & direction
    // vL, vR belongs to [-255, 255]
    double adj_R = 1.06, adj_L = 1;
    vL *= adj_L;
    vR *= adj_R;

    if (vL >= 0) { //L forward
        analogWrite(MotorL_PWML, vL); 
        digitalWrite(MotorL_I1, LOW);
        digitalWrite(MotorL_I2, HIGH);
    } else { //L backward
        analogWrite(MotorL_PWML, -vL); 
        digitalWrite(MotorL_I1, HIGH);
        digitalWrite(MotorL_I2, LOW);
    }

    if (vR >= 0) { //R forward
        analogWrite(MotorR_PWMR, vR); 
        digitalWrite(MotorR_I3, HIGH);
        digitalWrite(MotorR_I4, LOW);
    } else { //R backward
        analogWrite(MotorR_PWMR, -vR); 
        digitalWrite(MotorR_I3, LOW);
        digitalWrite(MotorR_I4, HIGH);
    }
}

void TrackClass::MotorCheck() {
    TrackClass::MotorWriting(100, 100); // forward
    delay(5000);

    TrackClass::MotorWriting(-100, -100); // backward
    delay(5000);

    TrackClass::MotorWriting(-100, 100); // left turn
    delay(5000);

    TrackClass::MotorWriting(100, 100); // right turn
    delay(5000); // 轉五秒
}

// Handle negative motor_PWMR value.
void TrackClass::MotorInverter(int motor, bool& dir) {
    // Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
}

// P/PID control Tracking
void TrackClass::Tracking(int l2, int l1, int m0, int r1, int r2) {

    // PD control parameters 
    double _w0 = 0;  //
    double _w1 = 0.5;  //
    double _w2 = 3;  //
    double _Kp = 20;  // p term parameter
    double Tp = 150;
    double _Kd = 60;  // d term parameter (optional)
    double _Ki;  // i term parameter (optional) (Hint: 不要調太大)
    double error;

    if (l1 + l2 + r1 + r2) {
        error = (l2 * (-_w2) + l1 * (-_w1) + m0 * _w0 + r1 * _w1 + r2 * _w2) / (l1 + l2 + r1 + r2);
    } else {
        error = 0;
    }

    double error_difference = error - last_error;
    double power_correction = _Kp * error + _Kd * error_difference;
    last_error = error;
    
    // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
    // Update vR, vL
    double vR = Tp - power_correction; 
    double vL = Tp + power_correction;
    
    // double adj_R = 1.055, adj_L = 1; // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。

    if (vR > 255)
        vR = 255;
    if (vL > 255)
        vL = 255;
    if (vR < -255)
        vR = -255;
    if (vL < -255)
        vL = -255;

    TrackClass::MotorWriting(vL, vR);
}  // tracking

void TrackClass::QuarterCircleLeft() {
    TrackClass::MotorWriting(-120, 120);
    delay(50);
    while (!(digitalRead(40) == 0 && digitalRead(38) == 0 && digitalRead(36) == 0 && digitalRead(34) == 0 && digitalRead(32) == 0)) {
        TrackClass::MotorWriting(-120, 120);
    }

    while (digitalRead(36) == 0) {
        TrackClass::MotorWriting(-120, 120);
    }
}

void TrackClass::QuarterCircleRight() {
    TrackClass::MotorWriting(120, -120);
    delay(50);
    while (!(digitalRead(40) == 0 && digitalRead(38) == 0 && digitalRead(36) == 0 && digitalRead(34) == 0 && digitalRead(32) == 0)) {
        TrackClass::MotorWriting(120, -120);
    }

    while (digitalRead(36) == 0) {
        TrackClass::MotorWriting(120, -120);
    }
}

void TrackClass::UTurn() {
    TrackClass::MotorWriting(150, -150);
    delay(50);
    while (!(digitalRead(40) == 0 && digitalRead(38) == 0 && digitalRead(36) == 0 && digitalRead(34) == 0 && digitalRead(32) == 0)) {
        TrackClass::MotorWriting(150, -150);
    }

    while (digitalRead(36) == 0) {
        TrackClass::MotorWriting(150, -150);
    }
}

void TrackClass::OldUTurn() {
    TrackClass::MotorWriting(250, -250);
    delay(575);
}

void TrackClass::OldQuarterCircleR() {
    TrackClass::MotorWriting(150, -150);
    delay(425);
}

void TrackClass::OldQuarterCircleL() {
    TrackClass::MotorWriting(-150, 150);
    delay(425);
}

/*以下為轉彎函數 by鄭睿昕
void LeftTurn3rd() {
    while(digitalRead(40) == 1 && digitalRead(32) == 1){    // 兩邊有任一偵測到白，則停止
        MotorWriting(50, 52);   //讓車自盡量不偏右
    }
    MotorWriting(50, 52);   //讓車自盡量不偏右
    delay(50); //往前走一小段，時間需調整
    if(digitalRead(36) == 1){   //車子在node中走得直
        while(digitalRead(36) == 1){
            MotorWriting(-100, 100);
        }
        while(digitalRead(36) == 0 && digitalRead(34) == 1){
            MotorWriting(-100, 100);
        }
        while(digitalRead(36) == 0 && digitalRead(34) == 0){
            MotorWriting(-100, 100);
        }
    }
    else if(digitalRead(36) == 0){  //車子在node中偏左或右，或前方無道路
        if(digitalRead(40) == 1 || digitalRead(38) == 1){  //偏右
            while(digitalRead(36) == 0){
                MotorWriting(-100, 100);
            }
            while(digitalRead(36) == 1){
            MotorWriting(-100, 100);
            }
            while(digitalRead(36) == 0 && digitalRead(34) == 1){
            MotorWriting(-100, 100);
            }
            while(digitalRead(36) == 0 && digitalRead(34) == 0){
                MotorWriting(-100, 100);
            }
        }
        else{   //偏左或前方無道路
            while(digitalRead(36) == 0 && digitalRead(34) == 0){
                MotorWriting(-100, 100);
            }
        }
    }
}

void RightTurn3rd() {
    while(digitalRead(40) == 1 && digitalRead(32) == 1){    // 兩邊有任一偵測到白，則停止
        MotorWriting(50, 52);   //讓車自盡量不偏右
    }
    MotorWriting(50, 52);   //讓車自盡量不偏右
    delay(50); //往前走一小段，時間需調整
    if(digitalRead(36) == 1){   //車子在node中走得直
        while(digitalRead(36) == 1){
            MotorWriting(100, -100);
        }
        while(digitalRead(36) == 0 && digitalRead(38) == 1){
            MotorWriting(100, -100);
        }
        while(digitalRead(36) == 0 && digitalRead(38) == 0){
            MotorWriting(100, -100);
        }
    }
    else if(digitalRead(36) == 0){  //車子在node中偏左或右，或前方無道路
        if(digitalRead(32) == 1 || digitalRead(34) == 1){  //偏左
            while(digitalRead(36) == 0){
                MotorWriting(100, -100);
            }
            while(digitalRead(36) == 1){
            MotorWriting(100, -100);
            }
            while(digitalRead(36) == 0 && digitalRead(38) == 1){
            MotorWriting(100, -100);
            }
            while(digitalRead(36) == 0 && digitalRead(38) == 0){
                MotorWriting(100, -100);
            }
        }
        else{   //偏右或前方無道路
            while(digitalRead(36) == 0 && digitalRead(38) == 0){
                MotorWriting(100, -100);
            }
        }
    }
}

void UTurn3rd() {
    while(digitalRead(40) == 1 && digitalRead(32) == 1){    // 兩邊有任一偵測到白，則停止
        MotorWriting(50, 52);   //讓車自盡量不偏右
    }
    MotorWriting(50, 52);   //讓車自盡量不偏右
    delay(50); //往前走一小段，時間需調整
    while(digitalRead(36) == 0 && digitalRead(34) == 0){
        MotorWriting(-100, 100);    //向左迴轉
    }
}
*/

void TrackClass::SlowDown() {
    delay(500);
}

TrackClass track = TrackClass();