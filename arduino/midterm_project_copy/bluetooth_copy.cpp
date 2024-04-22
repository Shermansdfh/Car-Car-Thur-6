/*****************************************************************************/
// File [bluetooth.cpp]
// Author [Erik Kuo]
// Synopsis [Implementation of bluetooth communication functions]
// Modify [2020/03/27 Erik Kuo]
/*****************************************************************************/

#include "bluetooth_copy.h"
#include <Arduino.h>

const int rxPIN = 19;
const int txPIN = 18;

BluetoothClass::BluetoothClass() {}

void BluetoothClass::SETUP() {
    Serial1.begin(9600);
    Serial.begin(9600);
}

BluetoothClass::BT_CMD BluetoothClass::ask_BT() {
    BluetoothClass::BT_CMD message = BluetoothClass::NOTHING;
    char cmd;
    if (Serial1.available()) {
        cmd = Serial1.read(); // get cmd from Serial1(bluetooth serial)
        Serial.println(cmd);
        if (cmd == 'f') {
            message = BluetoothClass::Forward;
        } else if (cmd == 'b') {
            message = BluetoothClass::Backward;
        } else if (cmd == 'r') {
            message = BluetoothClass::RightTurn;
        } else if (cmd == 'l') {
            message = BluetoothClass::LeftTurn;
        } else if (cmd == 's') {
            message = BluetoothClass::Start;
        } else if (cmd == 'e') {
            message = BluetoothClass::EndProcess;
        }
        // link bluetooth message to BT_CMD command type

#ifdef DEBUG
        Serial.print("cmd : ");
        Serial.println(cmd);
#endif

    }
    return message;
}

// send msg back through Serial1(bluetooth serial)
// can use send_byte alternatively to send msg back
// (but need to convert to byte type)
void BluetoothClass::send_msg(const char& msg) {
    Serial1.write(msg);
}

// send UID back through Serial1(bluetooth serial)
void BluetoothClass::send_byte(byte* id, byte& idSize) {
    ///Serial1.write('$');
    for (byte i = 0; i < idSize; i++) {
        // Send UID consequently.
        if (id[i] < 10)
            Serial1.write(0);
        Serial1.write(id[i]);
    }

#ifdef DEBUG
    Serial.print("Sent id: ");
    for (byte i = 0; i < idSize; i++) {
        // Show UID consequently.
        /*
        if (id[i] < 10)
            Serial.print(0);
        */
        Serial.print(id[i], HEX);
    }
    Serial.println();
#endif

}

BluetoothClass BT = BluetoothClass();