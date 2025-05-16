fn miles_as_kilometers(miles: f64) -> f64 {
    miles * 1.609344
}

fn miles_to_kilometers(miles: &[f64]) -> Vec<f64> {
    miles
        .iter()
        .map(|&mile| mile * 1.609344)
        .collect()
}


fn main() {
    let distances = [1.0f64, 3.0, 10.0, 100.0]; // in miles
    println!("Distances in miles: {:?}", distances);
    // convert to kilometers
    let distances = miles_to_kilometers(&distances);
    println!("Distances in kilometers: {:?}", distances);
}

