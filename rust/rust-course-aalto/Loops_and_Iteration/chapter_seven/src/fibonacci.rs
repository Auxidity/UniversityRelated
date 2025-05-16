fn fibonacci_n_first(n: u32) -> Vec<u32> {
    let mut a = 0;
    let mut b = 1;
    let mut fibs = vec![a, b];
    for _ in 0..n {
        let c = a + b;
        fibs.push(c);
        a = b;
        b = c;
    }
    fibs
}

fn fibonacci_until(n: u32) -> Vec<u32>{
    let mut a = 0;
    let mut b = 1;

    let mut fibs = vec![a, b];

    loop {
        let c = a + b;
        if c > n {
            break;
        }
    fibs.push(c);
    a = b;
    b = c;
    } fibs
}

fn main() {
    println!("{:?}", fibonacci_until(10));
    println!("{:?}", fibonacci_until(100));
    println!("{:?}", fibonacci_until(1000));
}


