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
    let prime = largestPrime(i);
    if(primeArray.indexOf(prime) == -1){
      primeArray.push(prime);
    }
  }
  return(primeArray);
}

function thePrime(no){
  primes(no);
  console.log(primeArray);
  console.log(primeArray[10000]);
}

thePrime(130000);
