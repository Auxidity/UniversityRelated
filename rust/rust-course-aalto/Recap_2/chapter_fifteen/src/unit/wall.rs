use crate::point::Point2d;
use crate::traits::Position;
//Draw
use std::fmt;
//Poisition
use rand::{
    distributions::{uniform::SampleUniform, Standard},
    prelude::Distribution,
    rngs::ThreadRng,
    Rng,
};
use std::ops::Range;

#[derive(Default)]
#[allow(unused)]
pub struct Wall {
    position: Point2d<u16>
}

impl Wall {
    pub fn new( x:u16, y:u16 ) -> Self {
        Wall 
        {
            position: Point2d { x, y }, 
        }
    }
}

impl Position<u16> for Wall {
    fn position(&self) -> Point2d<u16> {
        self.position
    }

    fn set_position(&mut self, position: Point2d<u16>) {
        self.position = position;
    }

    fn set_rand_position(&mut self, rng: &mut ThreadRng, x_range: Range<u16>, y_range: Range<u16>)
    where
        usize: PartialOrd + SampleUniform,
        Standard: Distribution<u16>, {
            let new_position = Point2d::new(rng.gen_range(x_range), rng.gen_range(y_range));
            self.set_position(new_position);
    }
}

impl fmt::Display for Wall {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "#")
    }
}

