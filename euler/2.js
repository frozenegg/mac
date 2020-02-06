function rubbish(){
/*
function fibonacci(num){
  const array = [];
  array[0] = 1;
  array[1] = 2;
  for(var i = 2; i<num; i++){
    array.push(array[i-2] + array[i-1]);
  }
  console.log(array[num-1]);
}

//fibonacci(10);


function evenValuedSum(){
  var num = 1;

  while(true){
    var sum = 0;
    if(fibonacci(num) < 400){
      if(fibonacci(num) % 2 == 0){
        sum += fibonacci(num);
        num++;
      }else{
        num++;
      }
    }else{break};
  };

  console.log(sum);
}
*/
}

function evenValuedSumFibonacci(num){
  var num1 = 1;
  var num2 = 2;

  var sum = 2;

  while(true){
    var num3 = num1 + num2;
    num1 = num2;
    num2 = num3;

    if(num3 < num+1){
      if(num3 % 2 == 0){
        sum += num3;
      }
    }else{
      break
    };
  }

  console.log(sum);
};

evenValuedSumFibonacci(9);
