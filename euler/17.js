function letter(num){
  var numArray = num.toString().split('');
  var digit1 = ['','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'];
  var teens = ['ten','eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
  var tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
  var oneThousand = ['', 'One Thousand'];
  var letterArray = [];
  var letter = [];

  if(numArray.length > 3){
    letterArray.push('Onethousand');
  }
  if(numArray.length > 2 && numArray[numArray.length - 3] != '0'){
    letterArray.push(digit1[numArray[numArray.length - 3]], 'hundred');
  }
  if(numArray.length > 2 && (numArray[numArray.length - 2] != '0' || numArray[numArray.length - 1] != '0')){
    letterArray.push('and');
  }
  if(numArray.length > 1 && numArray[numArray.length - 2] == '1'){
    letterArray.push(teens[numArray[numArray.length - 1]]);
  }else if(numArray.length > 1){
    letterArray.push(tens[numArray[numArray.length - 2]], digit1[numArray[numArray.length - 1]]);
  }
  if(numArray.length == 1){
    letterArray.push(digit1[numArray[numArray.length - 1]]);
  }
  console.log(letterArray);
  return(letterArray.join('').split('').length);
}

function letterCount(){
  var count = 0;
  for(var i = 1; i<1001; i++){
    count += letter(i);
  }

  console.log(count);
}

letterCount();
