use std::collections::HashMap;

fn translate_fin(dictionary: &HashMap<String, String>, word: &str, log: &mut HashMap<String, u32>) -> String {
    let count = log.entry(word.to_string()).or_insert(0);
    *count += 1;

    match dictionary.get(word) {
        Some(translation) => format!("{word} in Finnish is {translation}"),
        None => format!("sorry, no translation for {word} available"),
    }
}

fn eng_fin_dictionary() -> HashMap<String, String> {
    let dictionary = HashMap::from([
        ("bear".to_string(), "karhu".to_string()),
        ("paw".to_string(), "tassu".to_string()),
        ("tail".to_string(), "häntä".to_string()),
        ("ear".to_string(), "korva".to_string()),
    ]);

    return dictionary;
}



fn main() {
    let mut usage_log = HashMap::new();
    let dictionary = eng_fin_dictionary();
    let _ = translate_fin(&dictionary, "bear", &mut usage_log);
    let _ = translate_fin(&dictionary, "paw", &mut usage_log);
    let _ = translate_fin(&dictionary, "bear", &mut usage_log);
    let _ = translate_fin(&dictionary, "🐻", &mut usage_log);
    println!("{usage_log:?}"); // {"bear": 2, "paw": 1, "🐻": 1} (may be in different order)
}

