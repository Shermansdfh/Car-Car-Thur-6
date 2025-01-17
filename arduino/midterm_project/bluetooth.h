/***************************************************************************/
// File			  [bluetooth.h]
// Author		  [Erik Kuo]
// Synopsis		[Code for bluetooth communication]
// Functions  [ask_BT, send_msg, send_byte]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 2*/

enum BT_CMD {
    NOTHING,
    forward,
    backward,
    rightTurn,
    leftTurn,
    endProcess
};

BT_CMD ask_BT() {
    BT_CMD message = NOTHING;
    char cmd;
    if (Serial1.available()) {
        cmd = Serial1.read();                // get cmd from Serial1(bluetooth serial)
        Serial.println(cmd);
        if (cmd == 'f') {
            message = forward;
            // Serial.println("f");
        }
        else if (cmd == 'b') {
            message = backward;
            // Serial.println("b");
        }
        else if (cmd == 'r') {
            message = rightTurn;
            // Serial.println("r");
        }
        else if (cmd == 'l') {
            message = leftTurn;
            // Serial.println("l");
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
void send_msg(const char& msg) {
  // TODO:
}  // send_msg

// send UID back through Serial1(bluetooth serial)
void send_byte(byte* id, byte& idSize) {
  for (byte i = 0; i < idSize; i++) {  // Send UID consequently.
    Serial1.write(id[i]);
  }

#ifdef DEBUG
  Serial.print("Sent id: ");
  for (byte i = 0; i < idSize; i++) {  // Show UID consequently.
    if (id[i] < 10) Serial.print(0);
    Serial.print(id[i], HEX);
  }
  Serial.println();
#endif

}  // send_byte
