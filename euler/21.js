function d(num){
  var sum = 0;
  for(var i = 1; i<num; i++){
    if(num % i == 0){
      sum += i;
    }
  }
  return(sum);
}

function amicable(num){
  var amicableArray = [];
  for(i = 1; i<num; i++){
    if(i == d(d(i))){
      amicableArray.push(i);
    }
  }
  console.log(amicableArray);
}

amicable(10000);
