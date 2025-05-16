use rand::seq::SliceRandom;

use crate::util::read_input;

use std::fs::File;
use std::io;
use csv::ReaderBuilder;

pub fn ask_question(question: &str, correct_answer: &str) -> bool {
    println!("{}", question);
    let user_answer = read_input();
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


pub fn practice_problems_random_order(problems: &[(&str, &str)]) {
    let mut problems = problems.to_vec();
    problems.shuffle(&mut rand::thread_rng());
    practice_problems(&problems);
}

// Implement public function read_problems_from_csv here
pub fn read_problems_from_csv(filename: &str) -> Result<Vec<(String,String)>, io::Error> {
    let file = File::open(filename)?;
    let mut rdr = ReaderBuilder::new().from_reader(file);
    
    let mut problems = Vec::new();

    for problem in rdr.records(){
        let record = problem?;
        if record.len() >= 2 {
            let question = record[0].to_string();
            let answer = record[1].to_string();
            problems.push((question, answer));
        } else {
            return Err(io::Error::new(io::ErrorKind::InvalidData, "Invalid CSV format. Please enter Question,Answer format"));
        }
    }Ok(problems)

}
