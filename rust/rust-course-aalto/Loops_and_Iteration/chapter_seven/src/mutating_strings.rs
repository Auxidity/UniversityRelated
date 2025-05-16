fn lowercase(input: &mut [String]) {
    for i in input {
        *i = i.to_lowercase();
    }
}

fn ellipse(sentences: &mut [String], max_len: usize) {
    for s in sentences {
        if s.len() > max_len {
            let end_idx = max_len -3;
            s.replace_range(end_idx.., "...");
        }
    }
}

fn main() {
    let strings = vec![
        "This is ASCII",
        "This is not -> ä",
        "Valid ASCII again!",
        "And then not 🐈",
    ];
    let mut strings = strings
        .into_iter()
        .map(|s| s.to_string())
        .collect::<Vec<String>>();

    lowercase(&mut strings);
    println!("{:?}", strings); // ["this is ascii", "this is not -> ä", "valid ascii again!", "and then not 🐈"]

    ellipse(&mut strings, 10);
    println!("{:?}", strings); // ["this is...", "this is...", "valid a...", "and the..."]
}


