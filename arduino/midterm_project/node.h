/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on your own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/
//#include "track.h"
/*===========================import variable===========================*/
int extern _Tp;
/*===========================import variable===========================*/

// TODO: add some function to control your car when encounter a node
// here are something you can try: left_turn, right_turn... etc.



bool on_node(bool on_node, int l2, int l1, int m0, int r1, int r2) {
    while(!(on_node && l2 == 0 && r2 == 0)){
        //tracking(l2, l1, m0, r1, r2);
            if (on_node == 0 && l2 && l1 && m0 && r1 && r2) {
                return true;
            }
            else return false;
    }
}

/*
void left_turn{
    
}

void right_turn{
    
}

void u_turn{
    
}

void go_straight{

}
*/