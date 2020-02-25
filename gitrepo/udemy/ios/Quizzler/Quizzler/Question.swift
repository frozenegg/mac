//
//  Question.swift
//  Quizzler
//
//  Created by silicondoo on 2019/09/25.
//  Copyright © 2019 London App Brewery. All rights reserved.
//

import Foundation

class Question{
    
    let questionText : String
    let answer : Bool
    
    init(text: String, correctAnswer: Bool){
        questionText = text
        answer = correctAnswer
    }
    func doSomething(){
        //do something
    }
    
}

/*
class myOtherClass{
    let question = Question(text: "What's the meaning of life?", correctAnswer: true)
    let question2
}
 
 */
