// Implement the read_line function to read a line from the user
use std::io;

fn read_line() -> String {
    let mut line = String::new();
    io::stdin().read_line(&mut line).unwrap();
    let trimmed = line.trim().to_string();
    trimmed
}


fn main() {
    let accepted_answers = vec!["yes", "y", "no", "n"];

    println!("Do you like Rust? Yes or no (y/n)?");

    let mut answer = String::new();
    while !accepted_answers.contains(&answer.as_str()) {
        answer = read_line();
        match answer.as_str() {
            "yes" | "y" => println!("Awesome!"),
            "no" | "n" => println!("Oh :("),
            _ => println!("Unrecognized answer, please answer yes or no (y/n)"),
        }
    }
}


