// Implement the function nth_chars
fn nth_chars(emojis: &str,indices: &[usize]) -> String {
    let chars: Vec<char> = emojis.chars().collect();
    let mut result = String::new();

    for &index in indices {
        if index >= chars.len() {
            panic!("Index out of bounds. {}", index);
        }
        result.push(chars[index]);
    }
    result
}


fn main() {
    let emojis =
        "🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐕🐖🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐩🐪🐫🐳";
    let common_pets = nth_chars(emojis, &[7, 8, 20]);
    println!("Common pets: {common_pets}");
}


