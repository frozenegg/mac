function largestPrime(num){
  var factor = 2;
  var largest = 1;

  while(num != 1){
    if(num % factor == 0){
      num = num / factor;
      largest = factor;
    }else{
      factor++;
    }
  }
  return(largest);
};

function primes(num){
  primeArray = [];
  for(var i = 2; i<num+1; i++){
    var prime = largestPrime(i);
    if(primeArray.indexOf(prime) == -1){
      primeArray.push(prime);
    }
  }
  return(primeArray);
}

function evenlyDivisible(num){
  var answer = 1;

  var newPrimesArray = primes(num);


  for(var j = 1; j<num+1; j++){
    var save = j;
    for(var i = 0; i<newPrimesArray.length; i++){
      if(j % newPrimesArray[i] == 0){
        j = j / newPrimesArray[i];
      }
    }
    if(j != 1){
      for(var i = newPrimesArray.length; i>-1; i--){
        if(j % newPrimesArray[i] == 0){
          j = j / newPrimesArray[i];
          newPrimesArray.push(newPrimesArray[i]);
        }
      }
    }
    j = save;
  }

  console.log(newPrimesArray);
  for(var i = 0; i<newPrimesArray.length; i++){
    answer = answer * newPrimesArray[i];
  }
  console.log(answer);
}

evenlyDivisible(20);
