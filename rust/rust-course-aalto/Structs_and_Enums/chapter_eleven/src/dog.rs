use rand::{thread_rng, Rng};

pub struct Dog {
    name: String,
    birth_year: u32,
    weight: f32,
}

pub fn rand_u32(min: u32, max: u32) -> u32 {
    return thread_rng().gen_range(min..=max);
}

pub fn rand_f32(min: f32, max: f32) -> f32 {
    return thread_rng().gen_range(min..=max);
}

pub fn rand_choice(choices: &[&str]) -> String {
    let i = thread_rng().gen_range(0..choices.len());
    choices[i].to_owned()
}

fn random_dog() -> Dog {
    let choices = ["Alpha","Beta","Celcius","Delta", "Echo","Gamma"];
    let bday = rand_u32(0, 2024);
    let rand_weight = rand_f32(0.0, 250.0);
    let rand_name = rand_choice(&choices);
    let dog = Dog{
        name: rand_name,
        birth_year: bday,
        weight:rand_weight,
    };
    dog
}

fn main() {
    let dog = random_dog();

    println!("Dog:");
    println!("  name: {}", dog.name);
    println!("  birth year: {}", dog.birth_year);
    println!("  weight: {:.2}", dog.weight);
}


