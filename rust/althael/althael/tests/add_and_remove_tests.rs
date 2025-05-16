use std::fs;
use serde_json::Value;
use althael::{access::{fetch::fetch_id, remove::remove}, common::get_base_path, config::{get_max, get_min, get_pwlen}, generation::combined::generate};

#[test]
fn test_add_an_entry() {
    let test_id = "add an entry test".to_string();
    let test_email = "addanentry@test.fi".to_string();
    
    if let Err(e) = generate(test_id.clone(), test_email.clone(), get_pwlen(), get_min(),get_max()){
        eprintln!("Error: {}", e);
        panic!("generate() failed");
    }

    let mut path = get_base_path().unwrap();
    path.push("contents.json");

    let file_content = fs::read_to_string(&path).expect("Failed to read file");
    let parsed: Value = serde_json::from_str(&file_content).expect("Failed to parse file");

    let mut found = false;

    if let Value::Array(items) = parsed {
        for item in items {
            if let Ok(entry) = serde_json::from_value::<Value>(item) {
                if entry.get("id") == Some(&Value::String(test_id.clone())) &&
                    entry.get("email") == Some(&Value::String(test_email.clone())) {
                    found = true;
                    break;
                    }
            }
        }
    }
    
    assert!(found, "Expected entry with id: {}, email: {} not found", test_id.clone(), test_email);
    let _ = remove(test_id);
}


#[test]
fn test_search_with_match() {

    let test_id = "add an entry test".to_string();
    let test_email = "addanentry@test.fi".to_string();
    let _ = generate(test_id.clone(), test_email, get_pwlen(), get_min(), get_max());

    let result = fetch_id(test_id.clone());

    match result {
        Ok(entries) => {
            let contains_test_id = entries.iter().any(|entry| entry.id == test_id);
            assert!(contains_test_id, "Expected at least one entry with id {}", test_id.clone());
        },
        Err(e) => {
            eprintln!("Error: {}", e);
            panic!("fetch_id() failed");
        }
    }
    let _ = remove(test_id);
}

#[test]
fn test_search_no_match() {
    let test_id = "add an entry test that doesn't exist".to_string();

    let result = fetch_id(test_id.clone());

    match result {
        Ok(entries) => {
            assert!(entries.is_empty(), "Expected no entries but found some");
        },
        Err(e) => {
            eprintln!("Error: {}", e);
            panic!("fetch_id() failed");
        }
    }
}

#[test]
fn test_remove() {

    let test_id = "add an entry test".to_string();
    let test_email = "addanentry@test.fi".to_string();
    
    if let Err(e) = generate(test_id.clone(), test_email.clone(), get_pwlen(), get_min(),get_max()){
        eprintln!("Error: {}", e);
        panic!("generate() failed");
    }


    remove(test_id.clone()).expect("Failed to remove entry");
    
    let result = fetch_id(test_id.clone());

    match result {
        Ok(entries) => {
            assert!(entries.is_empty(), "Expected entry to be removed but found anyway");
        },
        Err(e) => {
            eprintln!("Error: {}", e);
            panic!("remove() failed");
        }
    }
}


