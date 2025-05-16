/*
 Complete the implementation of read_problems function in main.rs so that it returns a vector of trait objects that contains both multiple choice question and open text practice problems from the two files inside the resources directory.


 */


fn read_problems() -> Result<Vec<Box<dyn Practice>>, std::io::Error> {
    let mcq_problems =
        read_multiple_choice_problems_from_jsonl_serde("src/resources/mcq-problems.jsonl")?;

    let open_problems =
        read_open_text_problems_from_csv_serde("src/resources/open-text-problems.csv")?;

    let mut problems: Vec<Box<dyn Practice>> = Vec::new();

    for mcq in mcq_problems{
        problems.push(Box::new(mcq));
    }

    for open in open_problems {
        problems.push(Box::new(open));
    }

    Ok(problems)
}
