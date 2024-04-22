/***************************************************************************/
// File        [track.h]
// Author      [Erik Kuo]
// Synopsis    [Code used for tracking]
// Functions   [MotorWriting, MotorInverter, tracking]
// Modify      [2020/03/27 Erik Kuo]
/***************************************************************************/

#include <Arduino.h>

#ifndef TRACK_H
#define TRACK_H


class TrackClass {
    public:
		TrackClass();
		void SETUP();
        void MotorWriting(double vL, double vR);
        void MotorCheck();
        void MotorInverter(int motor, bool& dir);
        void Tracking(int l2, int l1, int m0, int r1, int r2);
        void QuarterCircleLeft();
        void QuarterCircleRight();
        void UTurn();
        void OldUTurn();
        void OldQuarterCircleR();
        void OldQuarterCircleL();
        void SlowDown();
        void LeftTurn3rd();
        void RightTurn3rd();
        void UTurn3rd();
};

extern TrackClass track;

extern int _Tp;
extern double last_error;

#endif // TRACK_H