fn main() {
    println!("{}€/kg", price_per_kg(2.99, 450.0));
    println!("{}€/kg", price_per_kg(29.99, 1514.0));
}

fn price_per_kg(price: f64, weight_in_grams: f64) -> f64 {
    return price / weight_in_grams * 1000.0;
}
