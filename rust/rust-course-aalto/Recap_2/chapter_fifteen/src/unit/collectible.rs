use crate::point::Point2d;
use crate::traits::Position;
use rand::{
    distributions::{uniform::SampleUniform, Standard},
    prelude::Distribution,
    rngs::ThreadRng,
    Rng,
};
use std::ops::Range;

#[derive(Default)]
#[allow(unused)]
pub struct Collectible {
    pub position: Point2d<u16>
}

impl Collectible {
    pub fn new(position: Point2d<u16>) -> Self {
        Collectible { position }
    }
}

impl Position<u16> for Collectible {
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


impl std::fmt::Display for Collectible {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "&")
    }
}

