// Write the function `remove_string`
fn remove_string(vector: &mut Vec<String>, index: usize) -> Option<String> {
    if index < vector.len() {
        if vector[index] == "🐻".to_string() || vector[index] ==  "🐼".to_string(){
            None
        } else {
            Some(vector.remove(index))
        }
    } else {
        None
    }
} 


fn main() {
    let mut bears = vec![
        "🐻".to_string(),
        "🐨".to_string(),
        "🐼".to_string(),
    ];
    let not_bear = remove_string(&mut bears, 1);
    println!("{not_bear:?}"); // 🐨
    println!("{bears:?}"); // ["🐻", "🐼"]
}


