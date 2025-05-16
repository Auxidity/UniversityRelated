// The first value of the point tuple is the x coordinate and the second value is the y coordinate.
fn quadrant(point: (i32, i32)) -> Option<String> {
    let quadrant = match point {
        (x, y) if x > 0 && y > 0 => Some("north-east".to_string()),
        (x, y) if x > 0 && y < 0 => Some("south-east".to_string()),
        (x, y) if x < 0 && y > 0  => Some("north-west".to_string()),
        (x, y) if x < 0 && y < 0  => Some("south-west".to_string()),
        _ => None,
    };
    Some(quadrant?)
}

fn main() {
    let point = (1, 1);
    println!("The point {:?} is in {} quadrant", point, quadrant(point).unwrap_or("no".to_string()));
    let point = (0, -1);
    println!("The point {:?} is in {} quadrant", point, quadrant(point).unwrap_or("no".to_string()));
}


