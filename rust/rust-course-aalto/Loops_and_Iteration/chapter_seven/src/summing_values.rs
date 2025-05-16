use std::collections::HashMap;

// Implement the function values_sum
fn values_sum(items: &HashMap<String, f32>) -> f32{
    items.values().sum()
}


fn main() {
    let mut fruit_prices = HashMap::new();
    fruit_prices.insert("mango".to_string(), 1.99);
    fruit_prices.insert("banana".to_string(), 0.49);
    fruit_prices.insert("pear".to_string(), 0.99);

    let total_prices = values_sum(&fruit_prices);
    println!("Individual prices: ");
    fruit_prices
        .iter()
        .for_each(|(key, value)| println!("  {key}: {value}"));
    println!("Total price: {total_prices}");
}

