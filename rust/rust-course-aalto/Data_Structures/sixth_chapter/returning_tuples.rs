// Implement the function multiplied_by_2() that takes two arguments and returns a tuple of the arguments multiplied by 2.
fn multiplied_by_2(a: i32, b: f32) -> (i32, f32){
    (a * 2, b * 2.0)
}

fn main() {
    let (a, b) = multiplied_by_2(1, 2.0);
    println!("a={}, b={}", a,b);
}


fn second(t: (u8, u16, u32)) -> u16 {
    t.1.try_into().unwrap()
}


