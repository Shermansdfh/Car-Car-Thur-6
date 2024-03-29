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
/*===========================import variable===========================*/

// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
    // TODO: use TB6612 to control motor voltage & direction
}  // MotorWriting

// Handle negative motor_PWMR value.
void MotorInverter(int motor, bool& dir) {
    // Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
}  // MotorInverter

// P/PID control Tracking
void tracking(int l2, int l1, int m0, int r1, int r2) {
    // TODO: find your own parameters!
    double _w0 = 0;  //
<<<<<<< HEAD
    double _w1 = 2;  //
    double _w2 = 10;  //
    double _Kp = 30;  // p term parameter
    double Tp = 140;
=======
    double _w1;  //
    double _w2;  //
    double _Kp;  // p term parameter
>>>>>>> d5af5a39ce1f2df72017e11d2b68d6e4fad25252
    double _Kd;  // d term parameter (optional)
    double _Ki;  // i term parameter (optional) (Hint: 不要調太大)
    double error;
    if (l1 + l2 + r1 + r2)
        double error = (l2 * (-_w2) + l1 * (-_w1) + m0 * _w0 + r1 * _w1 + r2 * _w2)/(l1 + l2 + r1 + r2);
    else error = 0;
    double powerCorrection = _Kp * error;
    double vR, vL;  // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
    vR = Tp - powerCorrection; 
    vL = Tp + powerCorrection;
    double adj_R = 1, adj_L = 1;  // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。

    // TODO: complete your P/PID tracking code

    // end TODO
    MotorWriting(adj_L * vL, adj_R * vR);
}  // tracking
