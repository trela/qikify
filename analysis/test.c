#include <iostream>
#include <string>

#include <sys/types.h>
#include <unistd.h>

#include <stdlib.h>

using namespace std;

int globalVariable = 2;

int main() {
	string sIdentifier;
	int iStackVariable = 20;
	
	pid_t pID = fork();
	if (pID == 0) {
		sIdentifier = "Child Process: ";
		globalVariable++;
		iStackVariable++;
	}
	else if (pID < 0) {
		cerr << "Failed to fork" << endl;
		exit(1);
	}
	else {
		sIdentifier = "Parent Process:";
	}
	
	cout << sIdentifier;
	cout << " Global variable: " << globalVariable;
	cout << " Stack variable: " << iStackVariable << endl;
}

