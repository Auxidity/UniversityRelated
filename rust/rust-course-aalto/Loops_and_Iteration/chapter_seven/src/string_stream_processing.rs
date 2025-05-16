fn longest_string_length(input: &[String]) -> Option<usize> {
    if input.is_empty(){
        return None
    }
    let longest_input = input.iter().map(|string| string.len()).max().unwrap();
    Some(longest_input)
}

fn ascii_strings_only(input: &[String]) -> Vec<String> {
    input
        .iter()
        .filter_map(|s|{
            if s.is_ascii() {
                Some(s.clone())
            } else {
            None
            }
        })
        .collect()
}

fn main() {
    let strings = vec![
        "This is ASCII",
        "This is not -> ä",
        "Valid ASCII again!",
        "And then 🚫",
    ];
    let strings = strings
        .into_iter()
        .map(|s| s.to_string())
        .collect::<Vec<String>>();
    println!("{:?}", longest_string_length(&strings)); // Some(18)

    println!("{:?}", ascii_strings_only(&strings)); // ["This is ASCII", "Valid ASCII again!"]
}


