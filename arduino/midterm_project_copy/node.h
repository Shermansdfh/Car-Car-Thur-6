/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on your own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/

#ifndef _NODE_H_
// #include "track.h"
#define _NODE_H_

/*===========================import variable===========================*/
int extern _Tp;
/*===========================import variable===========================*/

// TODO: add some function to control your car when encounter a node
// here are something you can try: left_turn, right_turn... etc.



bool NodeDetected(int l2, int l1, int m0, int r1, int r2) {
    if (l2 && l1 && m0 && r1 && r2) {
        return true;
    }
    else 
        return false;
}

#endif