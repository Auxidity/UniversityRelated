

macro_rules! impl_display {
    ($type: ty, $field: ident) => {
        impl ::std::fmt::Display for $type {
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                write!(f, "{}", self.$field)
            }
        }
    };
    ($type: ty: $($field:ident),*) => {
        impl ::std::fmt::Display for $type {
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let fields = vec![
                    $(format!("{:}", self.$field)),*
                ];
                
                write!(f, "{}", fields.join(", "))
            }
        }
    };
    ($type: ty: $($field:ident)*) => {
        impl ::std::fmt::Display for $type {
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let fields = vec![
                    $(format!("{:}", self.$field)),*
                ];
                
                write!(f, "{}", fields.join(" "))
            }
        }
    };
}

struct Cat {
    name: String,
    weight: f64,
    age: u8,
}

struct Dog {
    name: String,
    weight: f64,
    age: u8,
}

struct Mouse {
    name: String,
    weight: f64,
    age: u8,
}

struct FullName {
    first: String,
    last: String,
}

impl_display!(Cat, name);
impl_display!(Dog: name);
impl_display!(Mouse: name, age, weight);
impl_display!(FullName: first last);

fn main() {
    let cat = Cat {
        name: "Felix".to_string(),
        weight: 4.5,
        age: 5,
    };

    let dog = Dog {
        name: "Innocentius".to_string(),
        weight: 30.5,
        age: 3,
    };

    let mouse = Mouse {
        name: "Hilarius".to_string(),
        weight: 0.03,
        age: 1,
    };

    let name = FullName {
        first: "Pope".to_string(),
        last: "Linus".to_string(),
    };

    println!("{cat}"); // should print "Felix"
    println!("{dog}"); // should print "Innocentius"
    println!("{mouse}");  // should print "Hilarius, 1, 0.03"
    println!("{name}");  // should print "Pope Linus"
}
