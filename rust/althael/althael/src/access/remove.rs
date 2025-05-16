use std::fs;
use std::io::{ErrorKind, Error};

use crate::common::get_base_path;
use crate::encryption::encryption::{decrypt, encrypt}; // Import encrypt and decrypt functions
use serde_json::Value;

#[allow(dead_code)]
pub fn remove(id_to_remove: String, password: &str) -> Result<(), Error> {
    let mut path = get_base_path()?;
    path.push("contents.json");

    // Read the encrypted contents from the file
    let encrypted_data = fs::read(&path)?;

    // Decrypt the data
    let mut old_data = decrypt(&encrypted_data, password)
        .map_err(|e| Error::new(ErrorKind::InvalidData, e.to_string()))?;

    // Ensure old_data is an array
    if let Value::Array(ref mut array) = old_data {
        // Check if the entry exists and remove it
        if array.iter().any(|item| item["id"] == id_to_remove) {
            array.retain(|item| item["id"] != id_to_remove);

            // Encrypt the updated data before writing back to the file
            let encrypted_content = encrypt(&serde_json::to_string(array)?, password)
                .map_err(|e| Error::new(ErrorKind::Other, e.to_string()))?;

            // Write the encrypted content back to the file
            fs::write(&path, encrypted_content)?;

            Ok(())
        } else {
            Err(Error::new(ErrorKind::NotFound, "Entry not found"))
        }
    } else {
        Err(Error::new(ErrorKind::InvalidData, "Expected old data to be an array"))
    }
}
