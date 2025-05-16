use std::io;

// Modify read_line to work with the updated main function
fn read_line() -> Result<String, io::Error> {
    let mut line = String::new();
    io::stdin().read_line(&mut line)?;
    Ok(line.trim().to_string())
}

fn main() {
    let accepted_answers = vec!["yes", "y", "no", "n"];

    println!("Do you like Rust? Yes or no (y/n)?");

    let mut answer = String::new();
    while !accepted_answers.contains(&answer.as_str()) {
        let maybe_answer = read_line();
        answer = match maybe_answer {
            Ok(answer) => answer.to_lowercase(),
            Err(_) => {
                println!("What is this nonsense?");
                continue;
            }
        };
        match answer.as_str() {
            "yes" | "y" => println!("Awesome!"),
            "no" | "n" => println!("Oh :("),
            _ => println!("Unrecognized answer, please answer yes or no (y/n)"),
        }
    }
}


