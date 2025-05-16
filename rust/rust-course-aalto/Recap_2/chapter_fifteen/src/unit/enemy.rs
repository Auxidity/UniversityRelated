use crate::point::{self,Point2d};
use crate::unit::Player;
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
pub struct Enemy{
    speed: f64,
    position: Point2d<f64>,
}

impl Enemy {
    pub fn with_speed(speed:f64) -> Enemy {
        Enemy { speed , position: Point2d { x: 10.0, y: 10.0 } }
    }

    pub fn move_towards_player(&mut self, player: &Player){
            let direction = player.position() - self.position;

            let (norm_x, norm_y) = point::normalize((direction.x, direction.y));

            self.position.x += norm_x * self.speed;
            self.position.y += norm_y * self.speed;
    }
}


impl Position<f64> for Enemy {
    fn position(&self) -> Point2d<f64> {
        self.position
    }

    fn set_position(&mut self, position: Point2d<f64>) {
        self.position = position;
    }

    fn set_rand_position(&mut self, rng: &mut ThreadRng, x_range: Range<f64>, y_range: Range<f64>)
    where
        usize: PartialOrd + SampleUniform,
        Standard: Distribution<f64>, {
            let new_position = Point2d::new(rng.gen_range(x_range), rng.gen_range(y_range));
            self.set_position(new_position);
    }
}

impl std::fmt::Display for Enemy {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "+")
    }
}

