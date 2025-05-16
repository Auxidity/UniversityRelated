fn is_valid_password(password: &str) -> bool {
    if password.contains(char::is_numeric) &&
    password.contains(char::is_lowercase) &&
    password.contains(char::is_uppercase) &&
    password.len() >= 10 {
        return true
    }
    else {
        return false
    }

}

fn main() {
    println!("{:?}", is_valid_password("no_uppercase_chars0"));
    println!("{:?}", is_valid_password("NO_LOWERCASE_CHARS0"));
    println!("{:?}", is_valid_password("noNumbersHere:("));
    println!("{:?}", is_valid_password("Short0"));
    println!("{:?}", is_valid_password("shouldBeS4fE"));
}


