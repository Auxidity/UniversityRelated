
use std::fmt::Debug;
use std::cmp::Ord;


fn debug<T: Debug>(t: T) {
    println!("{t:?}");
}

fn sorted<T: Ord + Clone>(input: &[T])-> Vec<T>{
    let mut sorted_vec = input.to_vec();
    sorted_vec.sort();
    sorted_vec
}

fn main() {
    let vec = vec![10, -5, 30];
    let ar = ["🦫", "🦦", "🦥", "🦨", "🦡"];

    println!("{:?}", sorted(&vec));
    println!("{:?}", sorted(&ar));
}
