// Implement the ith_element function to return the ith element of the array.

fn ith_element(array: [u16; 3], i: usize)-> u16 {
    if i > 2 {
        panic!("Out of bounds");
    } else {
        array[i]
    }
}

fn main() {
    let a = [1, 5, 9];
    let i = 1;
    println!("{}", ith_element(a, i));
}



