fn inspect(target: Result<(), String>) -> () {
    match target {
        Ok(()) => println!("All ok!"),
        Err(e) => println!("Error: {}", e),
    }
}


fn main() {
    inspect(Ok(()));
    inspect(Err("Something went wrong!".to_owned()));
}

