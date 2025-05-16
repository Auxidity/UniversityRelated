use std::{env, io, path::PathBuf, fs};

use serde::{Serialize, Deserialize};

//Struct for storing contents.json entries
#[derive(Serialize,Deserialize,Clone)]                 
pub struct Entry {
    pub id: String,                     
    pub email: String,                                                         
    pub pw: String,    
    pub handle: String,                                                   
} 

//Data folder base path for config.json & contents.json
pub fn get_base_path() -> io::Result<PathBuf> {
    let mut base_path = env::current_dir()?;
    base_path.push("data");
    
    //create_dir would also work, all lets you change data to data/whatever/whatever2 if neccesary
    if !base_path.exists() {
        fs::create_dir_all(&base_path)?;
    }

    Ok(base_path)
}

