/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

/*===========================import variable===========================*/
int extern _Tp;
double extern lastError;
/*===========================import variable===========================*/

// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
    // use TB6612 to control motor voltage & direction
    //vL, vR belongs to [-255, 255]
    if (vL >= 0) { //L forward
        analogWrite(MotorL_PWML, vL); 
        digitalWrite(MotorL_I1, LOW);
        digitalWrite(MotorL_I2, HIGH);
    }
    else { //L backward
        analogWrite(MotorL_PWML, -vL); 
        digitalWrite(MotorL_I1, HIGH);
        digitalWrite(MotorL_I2, LOW);
    }
    if (vR >= 0) { //R forward
        analogWrite(MotorR_PWMR, vR); 
        digitalWrite(MotorR_I3, HIGH);
        digitalWrite(MotorR_I4, LOW);
    }
    else { //R backward
        analogWrite(MotorR_PWMR, -vR); 
        digitalWrite(MotorR_I3, LOW);
        digitalWrite(MotorR_I4, HIGH);
    }
}

void MotorCheck() {
  MotorWriting(100, 100); //forward
  delay(5000); 
  MotorWriting(-100, -100); //backward
  delay(5000); 
  MotorWriting(-100, 100); //left turn
  delay(5000); 
  MotorWriting(100, 100); //right turn
  delay(5000); // 轉五秒
}

// Handle negative motor_PWMR value.
void MotorInverter(int motor, bool& dir) {
    // Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
}  // MotorInverter

// P/PID control Tracking
void tracking(int l2, int l1, int m0, int r1, int r2) {
    // TODO: find your own parameters!
    double _w0 = 0;  //
    double _w1 = 0.5;  //
    double _w2 = 3;  //
    double _Kp = 20;  // p term parameter
    double Tp = 200;
    double _Kd = 60;  // d term parameter (optional)
    double _Ki;  // i term parameter (optional) (Hint: 不要調太大)
    double error;
    if (l1 + l2 + r1 + r2)
        double error = (l2 * (-_w2) + l1 * (-_w1) + m0 * _w0 + r1 * _w1 + r2 * _w2)/(l1 + l2 + r1 + r2);
    else error = 0;
    double dError = error - lastError;
    double powerCorrection = _Kp * error + _Kd * dError;
    lastError = error;
    
    // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
    // Update vR, vL
    double vR = Tp - powerCorrection; 
    double vL = Tp + powerCorrection;
    // TODO: check what is adjustment parameter
    double adj_R = 1, adj_L = 1;  // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。

    // TODO: complete your P/PID tracking code

    if (vR > 255) vR = 255;
    if (vL > 255) vL = 255;
    if (vR < -255) vR = -255;
    if (vL < -255) vL = -255;

    // end TODO
    MotorWriting(adj_L * vL, adj_R * vR);
}  // tracking

void quarterCircleLeft() {
    MotorWriting(-150, 150);
    delay(425);
}

void quarterCircleRight() {
    MotorWriting(150, -150);
    delay(425);
}

void uTurn() {
    MotorWriting(250, -250);
    delay(575);
}

void slowDown() {
    delay(500);
}