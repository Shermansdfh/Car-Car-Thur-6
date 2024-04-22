/*****************************************************************************/
// File [bluetooth.h]
// Author [Erik Kuo]
// Synopsis [Code for bluetooth communication]
// Functions [ask_BT, send_msg, send_byte]
// Modify [2020/03/27 Erik Kuo]
/*****************************************************************************/

#include <Arduino.h>

#ifndef _BLUETOOTH_H_
#define _BLUETOOTH_H_


class BluetoothClass {
    public:
		BluetoothClass();
		void SETUP();
		enum BT_CMD { NOTHING, Forward, Backward, RightTurn, LeftTurn, Start, EndProcess };
		BT_CMD ask_BT();
		void send_msg(const char& msg);
		void send_byte(byte* id, byte& idSize);
};

extern BluetoothClass BT;

#endif // BLUETOOTH_H