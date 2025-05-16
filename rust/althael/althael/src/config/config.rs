use serde::{Serialize, Deserialize};
use std::{fs, io};
use once_cell::sync::Lazy;
use std::sync::Mutex;

use crate::common::get_base_path;

#[derive(Serialize, Deserialize, Debug)]
pub struct Config {
    pub min_length: usize,
    pub max_length: usize,
    pub pw_length: usize,
}

impl Config {
    pub fn load_from_file() -> io::Result<Self> {
        let mut path = get_base_path()?;
        path.push("config.json");
        
        match fs::read_to_string(&path) {
            Ok(file_content) => {
                match serde_json::from_str(&file_content) {
                    Ok(config) => Ok(config),
                    Err(_) => {
                        println!("Failed to parse config file, defaulting to defaults");
                        let default_config = Self::default();
                        default_config.save_to_file()?;
                        Ok(default_config)
                    }
                }
            }
            Err(_) => {
                println!("Failed to read config file, defaulting to defaults");
                let default_config = Self::default();
                default_config.save_to_file()?;
                Ok(default_config)
            }
        }
    }

    pub fn save_to_file(&self) -> io::Result<()> {
        let mut path = get_base_path()?;
        path.push("config.json");
        let json_content = serde_json::to_string_pretty(&self).expect("Failed to serialize data");
        fs::write(path, json_content)?;
        Ok(())
    }
}

impl Default for Config {
    fn default() -> Self {
        Config {
            min_length: 7,
            max_length: 14,
            pw_length: 16,
        }
    }
}


pub static CONFIG: Lazy<Mutex<Config>> = Lazy::new(|| Mutex::new(Config::load_from_file().expect("Failed to load file")));


pub fn update_config(min_length: usize, max_length: usize, pw_length: usize) -> io::Result<()> {
    let mut config = CONFIG.lock().unwrap();
    config.min_length = min_length;
    config.max_length = max_length;
    config.pw_length = pw_length;
    config.save_to_file()?;

    Ok(())
}

pub fn get_min() -> usize {
    let config = CONFIG.lock().unwrap();
    config.min_length
}
pub fn get_max() -> usize {
    let config = CONFIG.lock().unwrap();
    config.max_length
}
pub fn get_pwlen() -> usize {
    let config = CONFIG.lock().unwrap();
    config.pw_length
}
