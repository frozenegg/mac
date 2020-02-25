function factorial(num){
  var product = 1;
  for(var i = 1; i<num+1; i++){
    product *= i;
  }
  return(product);
}

//factorial(10);

function digitSum(num){
  var sum = 0;
  var numArray = factorial(num).toString().split('');
  for(var i = 0; i<numArray.length; i++){
    sum += Number(numArray[i]);
  }
  console.log(sum);
}


digitSum(20);
