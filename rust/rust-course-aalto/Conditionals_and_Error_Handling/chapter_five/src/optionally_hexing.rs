fn get_color_hex(color_name: &str) -> String {
    match color_name {
        "black" => "#000000".to_string(),
        "white" => "#FFFFFF".to_string(),
        "red" => "#FF0000".to_string(),
        "green" => "#00FF00".to_string(),
        "blue" => "#0000FF".to_string(),
        _ => "".to_string(), // Return empty string for unknown colors
    }
}

fn main() {
    println!("{:?}", get_color_hex("black"));
    println!("{:?}", get_color_hex("white"));
    println!("{:?}", get_color_hex("blue"));
    println!("{:?}", get_color_hex("pink"));
}
