function collatz(num){
  if(num % 2 == 0){
    num = num / 2;
  }else{
    num = 3 * num + 1;
  }
  return(num);
}

function iteration(num){
  var init = num;
  var iter = 1;
  var chain = [num];
  while(num != 1){
    num = collatz(num);
    iter++;
    chain.push(num);
  };
  //console.log(chain);
  //console.log(init, iter);
  return(iter);
}

//iteration(13);

function largestChain(start){
  var largestIter = 0;
  var initial = 0;
  for(var i = 1; i<start; i++){
    if(iteration(i)>largestIter){
      largestIter = iteration(i);
      initial = i;
      console.log(largestIter, initial)
    }
  }
  console.log(largestIter, initial);
}

largestChain(1000);
