function palindromeProduct(){
  var paliMax = 0;
  for(var i = 100; i<1000; i++){
    for(var j = 100; j<1000; j++){
      multi = i * j;
      multiArray = String(multi);
      reversed = multiArray.split('').reverse().join('');
      if(multiArray == reversed && multi > paliMax){
        paliMax = multi;
      }
    }
  }
  console.log(paliMax);
};

palindromeProduct();
