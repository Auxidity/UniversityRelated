

#[derive(Copy, Clone, Debug, PartialEq)]
struct Miles(f32);

#[derive(Copy, Clone, Debug, PartialEq)]
struct Kilometers(f32);

const KILOMETERS_PER_MILE: f32 = 1.609344;

impl PartialEq<Kilometers> for Miles {
    fn eq(&self, other: &Kilometers) -> bool{
        self.0 == other.0 / KILOMETERS_PER_MILE
    }
}
impl PartialEq<Miles> for Kilometers {
    fn eq(&self, other: &Miles) -> bool {
        self.0 / KILOMETERS_PER_MILE == other.0
    }
}

fn main() {
    let miles = Miles(1.0);
    let kilometers = Kilometers(1.609344);
    println!("{}", miles == kilometers);
    println!("{}", kilometers != miles);
}
