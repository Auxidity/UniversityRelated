mod quiz;
mod util;

use clap::{Arg, Command};

use quiz::{practice_problems_random_order, read_problems_from_csv};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    
    let matches = Command::new("Quiz")
        .version("0.1")
        .author("Me")
        .about("Quizzes from a csv file")
        .arg(
            Arg::new("problem-csv")
            .long("problem-csv")
            .value_name("CSV_FILE")
            .help("Sets the source file for problems to practice")
            .required(true)
            )
        .get_matches();

    let csv_file = matches.get_one::<String>("problem-csv").unwrap();
    
    let problems = read_problems_from_csv(csv_file)?;
    let problems = problems
        .iter()
        .map(|(q, a)| (q.as_str(), a.as_str()))
        .collect::<Vec<_>>();
    practice_problems_random_order(&problems);
    Ok(())
    
}
