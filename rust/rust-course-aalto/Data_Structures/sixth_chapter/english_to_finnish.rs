// Implement the translate_fin function here

use std::collections::HashMap;

fn eng_fin_dictionary() -> HashMap<String, String> {
    let dictionary = HashMap::from([
        ("bear".to_string(), "karhu".to_string()),
        ("paw".to_string(), "tassu".to_string()),
        ("tail".to_string(), "häntä".to_string()),
        ("ear".to_string(), "korva".to_string()),
    ]);

    return dictionary;
}

fn translate_fin(dictionary: &HashMap<String, String>, search_term: &str) -> String {
    if let Some(finnish_search_term) = dictionary.get(search_term) {
        return format!("{} in Finnish is {}", search_term, finnish_search_term);
    }

    for (term , translated_term) in dictionary {
        if translated_term == search_term {
            return format!("{} in Finnish is {}", term, translated_term);
        }
    }
    format!("Sorry, no translation for {} available", search_term)
}

fn main() {
    let dictionary: HashMap<String, String> = eng_fin_dictionary();
    println!("{}", translate_fin(&dictionary, "bear"));
    println!("{}", translate_fin(&dictionary, "paw"));
    println!("{}", translate_fin(&dictionary, "tail"));
    println!("{}", translate_fin(&dictionary, "🐻"));
}


