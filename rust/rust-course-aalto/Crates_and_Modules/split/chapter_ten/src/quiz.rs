use crate::util::io;

pub fn ask_question(question: &str, correct_answer: &str) -> bool {
    println!("{}", question);
    let user_answer = io::read_input();
    user_answer == correct_answer
}

pub fn practice_problems(problems: &[(&str, &str)]) {
    let mut score = 0;
    for (question, correct_answer) in problems {
        let correct = ask_question(question, correct_answer);
        if correct {
            score += 1;
            println!("Correct!");
        } else {
            println!("Incorrect! The correct answer is {}", correct_answer);
        }
    }
    println!("You got {} out of {} correct!", score, problems.len());
}

