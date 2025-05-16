use std::collections::HashMap;

// Implement the reverse_index function here that takes a slice of strings and returns a HashMap of the strings and their indices
fn reverse_index(string: &[String]) -> HashMap<String,usize>{
    string
        .iter()
        .enumerate()
        .map(|(index, string)| (string.clone(), index))
        .collect()
} 



fn main() {
    let fruits = [
        "🥭".to_string(),
        "🍑".to_string(),
        "🍐".to_string(),
    ];
    let fruit_indices = reverse_index(&fruits);
    println!("{:#?}", fruit_indices);
    println!("value at index 2 = {}", fruits[2]);
    println!("index of 🍐 = {}", fruit_indices[&"🍐".to_string()]);
}


