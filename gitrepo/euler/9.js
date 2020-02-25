function pythagorean(){
  var product = 0;
  var a = 0;
  var b = 0;
  var c2 = 0;
  for(var i = 1; i<998; i++){
    for(var j = 1; j<997; j++){
      var c = 1000 - i - j;
      if(i**2 + j**2 == c**2){
        product = i*j*c;
        a = i;
        b = j
        c2 = c;
      }
    }
  }
  console.log(product);
  console.log(a, b, c2, a+b+c2);
}

pythagorean();
