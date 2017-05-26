//============================================================================
// Name        : status.cpp
// Author      : Galen Church
// Version     :
// Copyright   : 
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <cstdlib>
#include <time.h>

#include <wiringPi.h>

#define SHUTDOWN_SW	28
#define STATUS_LED	26

using namespace std;

int shutdown_pressed = 0;
int shutdown_released = 0;

void shutSWISR(){
	shutdown_pressed = 1;
}

int main() {
	shutdown_pressed = 0;
	wiringPiSetup();
	pinMode(STATUS_LED, OUTPUT);
	pinMode(SHUTDOWN_SW, INPUT);
	pullUpDnControl(SHUTDOWN_SW, PUD_UP);

	timespec down, up;
	long delta;

	int state = 0;

	wiringPiISR(SHUTDOWN_SW, INT_EDGE_BOTH, *shutSWISR);


	for(;;){
		if(shutdown_pressed && state == 0){
			if (digitalRead(SHUTDOWN_SW) == 0){
				clock_gettime(CLOCK_MONOTONIC, &down);
				shutdown_pressed = 0;
				shutdown_released = 0;
				cout << "ShuttingDown...started: " << down.tv_sec << endl;
				delayMicroseconds(50);
				shutdown_pressed = 0;
				state = 1;
			}

		}
		if(state == 1){
			clock_gettime(CLOCK_MONOTONIC, &up);
			delta = up.tv_sec - down.tv_sec;

			if (shutdown_pressed && digitalRead(SHUTDOWN_SW) == 1){
				state = 0;
			}
			else{
				if(delta >= 3){
					cout << "Shutdown Now (down)!" << endl;
					int ret = system("sudo supervisorctl stop all");
					cout << WEXITSTATUS(ret) << endl;
					int ret1 = system("sudo shutdown now");
					cout << WEXITSTATUS(ret1) << endl;
					break;
				}
			}
		}
	}

	return 0;
}
