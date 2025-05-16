// Implement the function is_valid_password to check if a password is valid.
fn is_valid_password(password: &str) -> Result<(), String> {
    if !password.contains(char::is_numeric){
        Err("at least one number required".to_string())
    } else if !password.contains(char::is_lowercase) {
        Err("at least one lowercase letter required".to_string())
    } else if !password.contains(char::is_uppercase) {
        Err("at least one uppercase letter required".to_string())
    } else if password.len() < 10 {
        Err("length should be at least 10".to_string())
    } else {
        Ok(())
    } 
}


fn main() {
    println!("{:?}", is_valid_password("no_uppercase_chars0"));
    println!("{:?}", is_valid_password("NO_LOWERCASE_CHARS0"));
    println!("{:?}", is_valid_password("noNumbersHere:("));
    println!("{:?}", is_valid_password("Short0"));
    println!("{:?}", is_valid_password("shouldBeS4fE"))
}

