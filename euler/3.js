let num = 600851475143;
let ber = 21;

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
  console.log(largest);
};

largestPrime(num);
