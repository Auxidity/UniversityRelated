use althael::config::{get_max, get_min, get_pwlen, update_config};
use std::fs;
use std::path::Path;

#[test]
fn test_defaults() {
    let fp = Path::new("data/config.json");

    if fp.exists() {
        match fs::remove_file(fp) {
            Ok(_) => println!("config.json removed for default testing") ,
            Err(e) => panic!("Failed to remove file for default testing. Error: {}", e),
        }
    } else {
        println!("config.json not found, continuing");
    }

    let min = get_min();
    let max = get_max();
    let pw_len = get_pwlen();
    //The following are the hard coded default values that can be found in config.rs in the event
    //that config.json is missing
    assert!(min == 7 && max == 14 && pw_len == 16);
}

#[test]
fn test_updated_values() -> std::io::Result<()> {
    update_config(6, 13, 15)?;
    
    let min = get_min();
    let max = get_max();
    let pw_len = get_pwlen();

    assert!(min == 6 && max == 13 && pw_len == 15);

    Ok(())
}

