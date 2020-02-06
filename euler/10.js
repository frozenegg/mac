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

function sumPrime(below){
  var sum = 0;
  primeArray = primes(below);
  console.log(primeArray);
  for(var i = 0; i<primeArray.length; i++){
    sum += primeArray[i];
  }
  console.log(sum);
}

sumPrime(2000);
