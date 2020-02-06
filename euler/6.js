function difference(){
  var squareSum = 0;
  var sumSquare = 0;

  for(var i = 1; i<101; i++){
    squareSum += i * i;
    sumSquare += i;
  }
  sumSquare = sumSquare * sumSquare;

  var difference = sumSquare - squareSum;
  console.log(difference);
}

difference();
