fn print_if_content(maybe_content: Option<&str>) {
    if let Some(value) = maybe_content{
        println!("{}",value);
    }
}

fn panic_if_no_content(maybe_content: Option<&str>) {
    if let None = maybe_content{
        panic!("No content!");
    }
}

fn check_content(maybe_content: Option<&str>) {
    if let None = maybe_content{
        println!("No content!");
    } if let Some(value) = maybe_content {
        println!("Has content: {}", value);
   }
}

fn main() {
    print_if_content(Some("✅")); // Should print "✅"
    print_if_content(None); // Should not print anything

    check_content(Some("✅")); // Should print "Has content: ✅"
    check_content(None); // Should print "No content!"

    panic_if_no_content(Some("✅")); // Should not panic
    panic_if_no_content(None); // Should panic with message "No content!"
}

