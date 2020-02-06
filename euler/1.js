function number1(below){
  var sum = 0;
  var num1 = 0;
  var num2 = 0;
  var num3 = 0;
  
  while(3 * num1 < below){
    sum += 3 * num1;
    num1++;
  }
  while(5 * num2 < below){
    sum += 5 * num2;
    num2++;
  }
  while(15 * num3 < below){
    sum -= 15* num3;
    num3++;
  }
  console.log(sum);
};

number1(1000);

/*
do{
  (loop)
}while();
*/
