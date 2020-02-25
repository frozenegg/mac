import UIKit

func fibonacci(until n : Int){
    print(0)
    print(1)
    
    var num1 = 0
    var num2 = 1
    
    for _ in 1...n{
        let num = num1 + num2
        print(num)
        num1 = num2
        num2 = num
    }
    
}

fibonacci(until: 8)
