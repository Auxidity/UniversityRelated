fn main() {
    let mut x = 5;
    let y = &mut x;
    *y += 1;
    let z = &x;
    println!("x={x}, y={y}, z={z}");
}
