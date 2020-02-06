function power2(num){
  var largest = 0;
  var i = 0;
  while(num>largest){
    largest = 2**i;
    i++;
  }
  if(largest != 1){
    largest = largest / 2;
  }
  return(largest);
}

function binary(num){
  var binaryArray = [];
  binaryArray.push(power2(num));
  while(num >1){
    num = num - power2(num);
    binaryArray.push(power2(num));
  }
  return(binaryArray);
}


function listArray(num){
  var numArray = binary(num);
  var largest = numArray[0];
  var listArray = [];
  listArray.push(largest);
  while(true){
    if(largest % 2 == 0){
      largest = largest / 2;
      listArray.push(largest);
    }else{
      break;
    }
  }
  return(listArray);
}

function showBinary(num){
  var numArray = binary(num);
  var indexArray = [];
  for(var i = 0; i < listArray(num).length; i++){
    if(numArray.indexOf(listArray(num)[i]) == -1){
      indexArray.push(0);
    }else{
      indexArray.push(1);
    }
  }
  return(indexArray);
}

//showBinary(11);

function count(sum, width){
  var num = 2**sum;
  var sufficientArray = [];
  for(var i = 1; i<num+1; i++){
    //console.log(showBinary(i));
    var numberOf1s = 0;
    for(var j = 0; j < listArray(num).length; j++){
      if(showBinary(i)[j] == 1){
        numberOf1s++;
      }
    }
    if(numberOf1s == width){
      sufficientArray.push(i);
      console.log('Found ' + i);
    }
  }
  console.log(sufficientArray.length);
}

count(10, 5)
