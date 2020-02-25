function digitSum(power){
  var num = 2 ** power;
  var numArray = num.toString().split('');
  var sum = 0;
  for(var i = 0; i<numArray.length; i++){
    sum += Number(numArray[i]);
  }
  console.log(sum);
}

digitSum(15);
