use std::fs;
use std::io::Error;

use crate::common::Entry;
use crate::common::get_base_path;
use crate::encryption::encryption::decrypt;

#[allow(dead_code)]
pub fn fetch_id(id_to_fetch: String, password: &str) -> Result<Vec<Entry>, Error> {
    let mut path = get_base_path()?;
    path.push("contents.json");

    let encrypted_file_content = fs::read(&path)?;
    let decrypted_file_content = decrypt(&encrypted_file_content, password)
        .map_err(|e| Error::new(std::io::ErrorKind::InvalidData, e.to_string()))?; // Convert Box<dyn Error> to std::io::Error

    let items: Vec<Entry> = serde_json::from_value(decrypted_file_content)?;

    let matching_items : Vec<Entry> = items.into_iter()
                                           .filter(|item| item.id == id_to_fetch)
                                           .collect();
    
    Ok(matching_items)
}
//Could do as follows, leaving for now incase theres any need to go to this
/*
pub fn fetch_handle(id_to_fetch: String) -> Result<Vec<String>, Error> {
    let mut path = get_base_path()?;
    path.push("contents.json");

    let file_content = fs::read_to_string(&path)?;

    let items: Vec<Entry> = serde_json::from_str(&file_content)?;
    
    let matching_items : Vec<String> = items.into_iter()
                                           .filter(|item| item.id == id_to_fetch)
                                           .map(|item| item.handle)
                                           .collect();

    Ok(matching_items)
}
*/

#[allow(dead_code)]
pub fn fetch_all_ids(password: &str) -> Result<Vec<String>, Error> {
    let mut path = get_base_path()?;
    path.push("contents.json");

    let encrypted_file_content = fs::read(&path)?;
    let decrypted_file_content = decrypt(&encrypted_file_content, password)
        .map_err(|e| Error::new(std::io::ErrorKind::InvalidData, e.to_string()))?;

    let entries: Vec<Entry> = serde_json::from_value(decrypted_file_content)?;

    let ids: Vec<String> = entries.into_iter()
                                  .map(|entry| entry.id)
                                  .collect();
    Ok(ids)
}

#[allow(dead_code)]
fn extract_handle(entries: Vec<Entry>) -> Vec<String> {
    entries.into_iter()
                .map(|entry| entry.handle)
                .collect()
}
#[allow(dead_code)]
fn extract_pw(entries: Vec<Entry>) -> Vec<String> {
    entries.into_iter()
                .map(|entry| entry.pw)
                .collect()
}
#[allow(dead_code)]
fn extract_email(entries: Vec<Entry>) -> Vec<String> {
    entries.into_iter()
                .map(|entry| entry.email)
                .collect()
}

#[allow(dead_code)]
pub fn fetch_handle(id_to_fetch: String, password: &str) -> Result<Vec<String>, Error> {
    let entries = fetch_id(id_to_fetch, password)?;
    let handle = extract_handle(entries);
    Ok(handle)
}
#[allow(dead_code)]
pub fn fetch_pw(id_to_fetch: String, password: &str) -> Result<Vec<String>, Error> {
    let entries = fetch_id(id_to_fetch, password)?;
    let pw = extract_pw(entries);
    Ok(pw)
}
#[allow(dead_code)]
pub fn fetch_email(id_to_fetch: String, password: &str) -> Result<Vec<String>, Error> {
    let entries = fetch_id(id_to_fetch, password)?;
    let email = extract_email(entries);
    Ok(email)
}

//Tests missing do later
