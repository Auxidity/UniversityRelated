fn is_finnish_domain(domain: &str) -> bool {
    domain.ends_with(".fi")
}

fn retain_finnish_domains(domains: &mut Vec<String>) {
    domains.retain(|d| is_finnish_domain(d));
}

fn remove_by_value_first(domains: &mut Vec<String>, remove_target: &str){
    if let Some(i) = domains.iter().position(|domain| domain == remove_target){
        domains.remove(i);
    }
}

fn remove_by_value_all(domains: &mut Vec<String>, remove_target: &str){
    domains.retain(|domain| domain != remove_target);
}
// Implement the remove_by_value_first function

// Implement the remove_by_value_all function

fn main() {
    let mut domains: Vec<String> = vec![
        "test.fi",
        "svenska.se",
        "aalto.fi",
        "commercial.com",
        "aalto.fi",
        "suomi.fi",
        "suomi.fi",
    ]
    .into_iter()
    .map(|x| x.to_string())
    .collect();

    // keep only Finnish domains
    retain_finnish_domains(&mut domains);
    println!("{:#?}", domains);
    // remove the first suomi.fi domain
    remove_by_value_first(&mut domains, "suomi.fi");
    println!("{:#?}", domains);
    // remove all aalto.fi domains
    remove_by_value_all(&mut domains, "aalto.fi");
    println!("{:#?}", &domains);
}



