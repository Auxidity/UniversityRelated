use rand::{Rng, thread_rng};

#[allow(dead_code)]
pub fn generate_name(min_length: usize, max_length: usize) -> Result<String, String> {
    if min_length < 5 {
        return Err("Minimum length must be at least 5.".to_string());
    }

    if max_length > 16 {
        return Err("Maximum length must be under 16.".to_string());
    }

    if min_length > max_length {
        return Err("Minimum length cannot be larger than maximum length.".to_string());
    }
    /*Very simple logic for now, can add more to choose from later */
    let prefixes = ["Ar", "Bran", "Cen", "Dara", "El", "Fen"];
    let middle = ["al", "an", "el", "in", "or", "un"];
    let suffixes = ["dor", "thal", "mir", "ron", "ven", "wyn"];

    let mut rng = thread_rng();
    let mut name = format!(
        "{}{}{}",
        prefixes[rng.gen_range(0..prefixes.len())],
        middle[rng.gen_range(0..middle.len())],
        suffixes[rng.gen_range(0..suffixes.len())]
        );

    // Pad the name if it's too short
    while name.len() < min_length {
        let extra_middle = middle[rng.gen_range(0..middle.len())];
        let insert_pos = rng.gen_range(0..name.len() - suffixes[0].len());
        name.insert_str(insert_pos, extra_middle);
    }

    // Trim the name if it's too long
    while name.len() > max_length {
        // Try to find a middle part to remove
        let mut removed = false;
        for part in middle.iter() {
            if let Some(pos) = name.rfind(part) {
                let end_pos = pos + part.len();
                name.replace_range(pos..end_pos, "");
                removed = true;
                break;
            }
        }
        if !removed {
            // Name should be valid if we reach here..
            break;
        }
    }
    //Final check for option, might need to make more robust later
    if name.len() >= min_length && name.len() <= max_length {
        Ok(name)
    } else {
        Err(
            "Failed to generate a name within specified boundaries".to_string(),
        )
    }
}
