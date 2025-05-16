use althael::generate_name;

#[test]
fn test_genname_within_bounds() {
    let min = 7;
    let max = 12;
    let result = generate_name(min, max);
    assert!(result.is_ok());
    let name = result.unwrap();
    assert!(name.len() >= min && name.len() <= max);
}

#[test]
fn test_genname_too_small(){
    let min = 2;
    let max= 14;
    let result = generate_name(min,max);
    assert!(result.is_err());
}

#[test]
fn test_genname_too_large(){
    let min = 7;
    let max= 24;
    let result = generate_name(min,max);
    assert!(result.is_err());
}

#[test]
fn test_genname_min_bigger_than_max(){
    let min = 12;
    let max= 7;
    let result = generate_name(min,max);
    assert!(result.is_err());
}

#[test]
fn test_exact_length(){
    let min = 7;
    let max = 7;
    let result = generate_name(min,max);
    assert!(result.is_ok());
    
    let name = result.unwrap();
    assert!(name.len() == max);
}

