#include <iostream>
#include <fstream>

using namespace std;

int main(){
  int num = 10;
  int *ptr;
  ptr = &num;
  cout << num << " :: " << ptr << endl;

  ofstream write("C:\\Users\\Creator\\OUR_FILE.txt"); //doesn't have to be "write". It can be any name.
  cout << "Random text goes here in case you did not know\nIn case you did write something" << endl;
  write << "Windows is awesome I like working in it, I like all the freedom that I have in it as opposed to linux." << endl;

  ifstream read("C:\\Users\\Creator\\OUR_FILE.txt");
  string x;
  read >> x;
  cout << x;

  return 0;
}
