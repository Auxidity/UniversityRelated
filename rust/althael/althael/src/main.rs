#[allow(unused_imports)]
use althael::generation;
#[allow(unused_imports)]
use althael::generation::combined::generate;
#[allow(unused_imports)]
use althael::access;
#[allow(unused_imports)]
use althael::config::{get_min, get_max, get_pwlen, update_config};
#[allow(unused_imports)]
use althael::encryption::encryption;
#[allow(unused_imports)]
use std::{fs,error::Error};
#[allow(unused_imports)]
use althael::common::get_base_path;

// Actual main for app

fn main() -> std::io::Result<()> {

    althael::app::app::app();

    Ok(()) 
}



/*
//Encryption tests
fn main() -> Result<(), Box<dyn Error>> {
    let password = "password";
    let real_salt = encryption::generate_salt(password);
    let fake_pw = "not_password";
    let real_pw_again = "password";
    let real_salt_two = encryption::generate_salt(real_pw_again);

    if real_salt == real_salt_two {
        println!("It wokrs!");
    } else {
        println!("It doesn't :(")
    }

    let fake_salt = encryption::generate_salt(fake_pw);
    let test_data = r#"[
  {
    "email": "something@gmail.com",
    "handle": "Elorron",
    "id": "youtube",
    "pw": "TTRhVXgwWVdpam5BZ2N1"
  }
]"#;

    let encrypted_data = encryption::encrypt(test_data, &real_salt)?;
    let mut path = get_base_path()?;
    path.push("encrypted_test_data.bin");
    fs::write(&path, &encrypted_data)?;
    //Correct pw
    let stored_data = fs::read(&path)?;
    match encryption::decrypt(&stored_data, &real_salt) {
        Ok(decrypted_data) => {
            println!("Decrypted data: {}", decrypted_data);
        },
        Err(e) => println!("Error: {}", e),
    }
    //Incorrect pw    
    let stored_data_2 = fs::read(path)?;
    match encryption::decrypt(&stored_data_2, &fake_salt) {
        Ok(decrypted_data) => {
            println!("Decrypted data: {}", decrypted_data);
        },
        Err(e) => println!("Error: {}", e),
    }

    Ok(())

}
*/


/* Uncomment if you wish to run this test main() (contains configs and account generation tests)
fn main() {
    let test_id = "test".to_string();
    let test_email = "abcd@testingmail.com".to_string();

    let test_id2 = "test2".to_string();
    let test_email2 = "abcd2@testingmail.com".to_string();
    
    println!("Initial min_len: {}", get_min());
    println!("Initial max_len: {}", get_max());
    println!("Initial pw_len: {}", get_pwlen());

    update_config(6, 12, 15)?;

    println!("Post_update min_len: {}", get_min());
    println!("Post_update max_len: {}", get_max());
    println!("Post_update pw_len: {}", get_pwlen());
    
    match generate(test_id, test_email, get_pwlen(), get_min(), get_max()) {
        Ok(_) => {
        println!("Succesfully added");
        }
        Err(e) => {
            eprintln!("Error: {}", e);
        }
    }

    match generate(test_id2.clone(), test_email2, get_pwlen(), get_min(), get_max()) {
        Ok(_) => {
        println!("Succesfully added2");
        }
        Err(e) => {
            eprintln!("Error: {}", e);
        }
    }
    
    match access::remove::remove(test_id2) {
        Ok(_) => {
            println!("Succesfully removed test_id2");
        }
        Err(e) => {
            eprintln!("Error: {}", e);
        }
    }

}
*/
