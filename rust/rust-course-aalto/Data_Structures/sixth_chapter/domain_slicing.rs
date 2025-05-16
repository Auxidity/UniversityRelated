// Implement the is_finnish_domain function so that it returns true if the given domain is a Finnish domain.

//Hint: The len method might be useful for slicing the last three characters. Or there could be a method that does the same thing (the slice primitive documentation: https://doc.rust-lang.org/std/primitive.slice.html).

fn is_finnish_domain(domain: &str) -> bool {
   if let Some(pos) = domain.rfind('.'){
        return &domain[pos + 1..] == "fi";
   } 
   false
}

fn main() {
    println!("{}", is_finnish_domain("stackoverflow.com"));
    println!("{}", is_finnish_domain("aalto.fin.fi"));
}


