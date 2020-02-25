#include <iostream>
using namespace std;

double a, b;
double Sum(double a, double b);
void Welcome();
string Welcome2(string x);
string x;

int main(){
	cout << "The value of a is: ";
	cin >> a;
	cout << "The value of b is: ";
	cin >> b;
	cout << "The sum of a and b is: " << Sum(a,b) << endl;
	Welcome();
	cout << "Enter whatever you would like" << endl;
	cin >> x;
	cout << Welcome2(x) << endl;
	return 0;
}

double Sum(double a, double b){
	return a+b;
}

void Welcome(){
	cout <<  "Welcome to somewhere, where I have no idea" << endl;
}

string Welcome2(string x){
	return x;
}
