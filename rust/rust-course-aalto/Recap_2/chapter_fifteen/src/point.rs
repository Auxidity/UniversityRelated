use std::f64::consts::PI;
use std::ops::Sub;


#[derive(PartialEq, Eq, Default, Debug, Clone, Copy)]
pub struct Point2d<T> {
    pub x: T,
    pub y: T,
}

impl<T> Point2d<T> 
where
    T: num::traits::NumAssign + Copy,
{
    pub fn new(x: T, y: T) -> Self {
    Self { x, y}
    }    

}

impl Point2d<f64> {
    pub fn round(&self) -> Point2d<f64> {
        Point2d {
            x: self.x.round(),
            y: self.y.round(),
        }
    }

    pub fn to_u16(&self) -> Point2d<u16>{
        Point2d {
            x: self.x as u16,
            y: self.y as u16,
        }
    }
}

impl <T> Sub for Point2d<T>
where
    T: Sub<Output = T>,
{
    type Output = Point2d<T>;

    fn sub(self, other: Point2d<T>) -> Point2d<T> {
        Point2d {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}


pub fn normalize<T>(xy: (T, T)) -> (T, T)
where
    T: num::Float,
{
    let (x, y) = xy;
    let magnitude = (x * x + y * y).sqrt();
    (x / magnitude, y / magnitude)
}

#[derive(Debug, PartialEq)]
pub struct Direction {
    pub x : f64,
    pub y : f64,
}

impl Default for Direction {
   fn default() -> Self {
        Direction { x: 0.0, y: -1.0 }
   } 
}

impl Direction {
    pub fn turn_right(&mut self) {
        let angle_increment = PI/4.0;
        let current_angle = self.y.atan2(self.x);
        let new_angle = current_angle + angle_increment;

        self.x = new_angle.cos();
        self.y = new_angle.sin();
    }

    pub fn turn_left(&mut self) {
        let angle_increment = PI/4.0;
        let current_angle = self.y.atan2(self.x);
        let new_angle = current_angle - angle_increment;

        self.x = new_angle.cos();
        self.y = new_angle.sin();
    }

}
