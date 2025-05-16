#[derive(Debug)]
struct Point2d {
    x: f64,
    y: f64,
}

// implement associated functions new and from_tuple for Point2d
impl Point2d {
    fn new(x: f64, y:f64) -> Self {
         Self { x, y }
    }

    fn from_tuple(tuples: (f64, f64)) -> Self {
        Self {
            x: tuples.0,
            y: tuples.1,
        }
    }

    fn add(&self, tuple: &Point2d) -> Point2d{
        Point2d{
            x: self.x + tuple.x,
            y: self.y + tuple.y,
        }   
    }

    fn multiply(&self, multiplier: f64) -> Point2d{
        Point2d {
            x: self.x * multiplier,
            y: self.y * multiplier,
        }
    }

    fn add_inplace(&mut self, tuple: &Self) {
        self.x += tuple.x;
        self.y += tuple.y;
    }

    fn multiply_inplace(&mut self, multiplier: f64){
        self.x *= multiplier;
        self.y *= multiplier;
    }
}

fn main() {
    let direction = Point2d::new(1.0, 0.0);
    let velocity = 5.5;
    let movement = direction.multiply(velocity);

    let mut triangle = [(1.2, 1.1), (5.8, 10.9), (6.5, -3.5)]
        .into_iter()
        .map(Point2d::from_tuple)
        .collect::<Vec<_>>();

    println!("Triangle coordinates:");
    triangle
        .iter()
        .for_each(|point| println!("  x: {}, y: {}", point.x, point.y));

    println!(
        "Moving triangle by: x: {}, y: {}...",
        direction.x, direction.y
    );

    triangle
        .iter_mut()
        .for_each(|point| point.add_inplace(&movement));

    println!("Triangle coordinates:");
    triangle
        .iter()
        .for_each(|point| println!("  x: {}, y: {}", point.x, point.y));
}

