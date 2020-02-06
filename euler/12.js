function triangle(num){
  var sum = 0;
  for(var i = 1; i<num+1; i++){
    sum += i;
  }
  return(sum);
}

function divisor(num){
  var sum = triangle(num);
  var divisorArray = [];
  for(var i = 1; i<sum+1; i++){
    if(sum % i == 0){
      divisorArray.push(i);
    }
  }
  return(divisorArray);
}

function howManyDivisors(number){
  var length = 0;
  var num = 0;
  while(true){
    length = divisor(num).length
    if(length != number){
      num++;
      //console.log(num);
    }else{
      break;
    }
  }
  console.log(triangle(num));
  console.log(divisor(num));
}

howManyDivisors(50);
