use super::{password, account};
use std::fs::File;
use std::error::Error;
use std::io::{self, BufWriter,BufReader, Read, Write};
use serde_json::Value;

//Struct
use crate::common::Entry;
//Data folder location
use crate::common::get_base_path;
//Encryption & Decryption functions
use crate::encryption::encryption::{decrypt, encrypt};

#[allow(dead_code)]
pub fn generate(id: String, email: String, pw_len: usize, name_len_min: usize, name_len_max: usize, password: &str) -> io::Result<()> {
    let mut path = get_base_path()?;
    path.push("contents.json");

    // Open the file for reading
    let file = match File::open(&path) {
        Ok(f) => f,
        Err(ref e) if e.kind() == io::ErrorKind::NotFound => {
            File::create(&path)?;

            match File::open(&path) {
                Ok(f) => f,
                Err(e) => return Err(e)
            }
        },
        Err(e) => return Err(e),
    };

    let reader = BufReader::new(file);

    // Load old contents from file
    let encrypted_data: Vec<u8> = reader.bytes().collect::<Result<_, _>>()?;

    let old_data = if !encrypted_data.is_empty() {
        // Decrypt the data if it's not empty
        decrypt(&encrypted_data, password)
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e.to_string()))?
    } else {
        // If encrypted data is empty, initialize old_data as an empty array
        Value::Array(Vec::new())
    };

    // Ensure `old_data` is an array
    let mut entries = if let Value::Array(array) = old_data {
        // Convert the array to a Vec<Entry> for easy manipulation
        let entries: Vec<Entry> = array.into_iter()
            .filter_map(|v| serde_json::from_value(v).ok()) // Safely convert to Entry
            .collect();

        // Check if the new ID already exists
        if entries.iter().any(|entry| entry.id == id) {
            return Err(io::Error::new(io::ErrorKind::AlreadyExists, "ID already exists"));
        }

        entries // Proceed with adding the new entry
    } else {
        return Err(io::Error::new(io::ErrorKind::InvalidData, "Expected old data to be an array"));
    };

    let pw = password::generate_password(pw_len);

    // Generate random account handle
    let handle = match account::generate_name(name_len_min, name_len_max) {
        Ok(h) => h,
        Err(e) => return Err(io::Error::new(io::ErrorKind::Other, e)),
    };

    // Generate new entry
    let new_data = Entry { id, email, pw, handle, };
    
    //Add the new entry to existing entries
    entries.push(new_data);

    // Encrypt the updated data before writing back to the file
    let encrypted_content = encrypt(&serde_json::to_string(&entries)?, password)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;

    let file = File::create(&path)?;
    let mut writer = BufWriter::new(file);
    writer.write_all(&encrypted_content)?;

    Ok(())
}

#[allow(dead_code)]
pub fn edit(id: String, new_email: Option<String>, new_pwlen: Option<usize>, password: &str) -> io::Result<()> {
    let mut path = get_base_path()?;
    path.push("contents.json");

    let file = match File::open(&path) {
        Ok(f) => f,
        Err(e) => return Err(e),
    };

    let reader = BufReader::new(file);

    // Load old contents from file
    let encrypted_data: Vec<u8> = reader.bytes().collect::<Result<_, _>>()?;
    let mut old_data = decrypt(&encrypted_data, password)
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e.to_string()))?;

    if let Value::Array(ref mut array) = old_data {
        if let Some(entry) = array.iter_mut().find(|e| e["id"] == id) {
            // Update email if provided
            if let Some(email) = new_email {
                entry["email"] = serde_json::json!(email);
            }
            // Update password if new password length is provided
            if let Some(pw_len) = new_pwlen {
                let new_pw = password::generate_password(pw_len);
                entry["pw"] = serde_json::json!(new_pw);
            }
        } else {
            // Entry with the given ID was not found in the array
            return Err(io::Error::new(io::ErrorKind::NotFound, "Handle not found"));
        }
    } else {
        return Err(io::Error::new(io::ErrorKind::InvalidData, "Expected an array of entries, found something else"));
    }

    let encrypted_content = encrypt(&serde_json::to_string(&old_data)?, password)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;

    let file = File::create(&path)?;
    let mut writer = BufWriter::new(file);
    writer.write_all(&encrypted_content)?;

    Ok(())
}

#[allow(dead_code)]
pub fn verification(pw: &str) -> Result<Option<String>, Box<dyn Error>> {
    let mut path = get_base_path()?; 
    path.push("contents.json");

    let file = match File::open(&path) {
        Ok(f) => f,
        Err(ref e) if e.kind() == io::ErrorKind::NotFound => {
            File::create(&path)?;

            match File::open(&path) {
                Ok(f) => f,
                Err(e) => return Err(Box::new(e)),
            }
        },
        Err(e) => return Err(Box::new(e)),
    };


    let reader = BufReader::new(file);
    
    let encrypted_data: Vec<u8> = reader.bytes().collect::<Result<_, _>>()?;

    if encrypted_data.len() == 0 {
        return Ok(Some("Contents file is empty, it will be created when attempting to append a new entry for the first time.".to_string()));
    }

    match decrypt(&encrypted_data, pw) {
        Ok(_) => Ok(None),
        Err(e) => Err(e), // Decryption failed, return the error
    }
}
