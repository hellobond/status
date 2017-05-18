//============================================================================
// Name        : status.cpp
// Author      : Galen Church
// Version     :
// Copyright   : 
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <cstdlib>

#include <wiringPi.h>

#define SHUTDOWN_SW	28
#define STATUS_LED	26

using namespace std;

int shutdown_pressed = 0;

void shutSWISR(){
	shutdown_pressed = 1;
}

int main() {
	shutdown_pressed = 0;
	wiringPiSetup();
	pinMode(STATUS_LED, OUTPUT);
	pinMode(SHUTDOWN_SW, INPUT);
	pullUpDnControl(SHUTDOWN_SW, PUD_UP);

	wiringPiISR(SHUTDOWN_SW, INT_EDGE_FALLING, *shutSWISR);

	for(;;){
		if(!shutdown_pressed){
			digitalWrite(STATUS_LED, HIGH);
			delay(500);
			digitalWrite(STATUS_LED, LOW);
			delay(500);
		}
		else{
			shutdown_pressed = 0;
			digitalWrite(STATUS_LED, HIGH);
			delay(3000);
			if(digitalRead(SHUTDOWN_SW) == 0){
				cout << "ShuttingDown..." << endl;
				int ret = system("sudo shutdown now");
				cout << WEXITSTATUS(ret) << endl;
				delay(500);
				digitalWrite(STATUS_LED, LOW);
				break;
			}
		}
	}

	return 0;
}
