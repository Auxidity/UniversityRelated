// HashMap needs to be imported from the standard library before it can be used
use std::collections::HashMap;

// Implement the eng_fin_dictionary function here
/*
bear -> karhu
paw -> tassu
tail -> häntä
ear -> korva
*/

fn eng_fin_dictionary() -> HashMap<String, String>{
   let mut dictionary = HashMap::new();
    dictionary.insert("bear".to_string(), "karhu".to_string());
    dictionary.insert("paw".to_string(), "tassu".to_string());
    dictionary.insert("tail".to_string(), "häntä".to_string());
    dictionary.insert("ear".to_string(), "korva".to_string());
    dictionary
}

fn main() {
    let dictionary: HashMap<String, String> = eng_fin_dictionary();
    println!("{dictionary:#?}");
}



