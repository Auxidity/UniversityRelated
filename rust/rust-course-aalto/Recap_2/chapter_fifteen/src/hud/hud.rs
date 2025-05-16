use crate::{traits::Position, unit:: Player, point::Point2d};
use std::fmt::{self, Display};

pub struct Hud<'a> {
    score: u32,
    player: &'a Player,
    y_position: u16,
}

impl<'a> Hud<'a> {
    pub fn new(score: u32, player: &'a Player, y_position: u16) -> Self {
        Self {score, player, y_position }
    }
}

impl<'a> Position<u16> for Hud<'a> {
    fn position(&self) -> crate::point::Point2d<u16> {
        Point2d{
            x: 0,
            y: self.y_position
        }
    }

    fn set_position(&mut self, position: crate::point::Point2d<u16>) {
        self.y_position = position.y
    }

    fn set_rand_position(&mut self, rng: &mut rand::prelude::ThreadRng, x_range: std::ops::Range<u16>, y_range: std::ops::Range<u16>)
    where
        u16: PartialOrd + rand::distributions::uniform::SampleUniform,
        rand::distributions::Standard: rand::prelude::Distribution<u16>, {
    }
}

impl <'a> Display for Hud <'a> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let player_position = self.player.position();
        write!(f, "Score: {}, Player position: ({}, {})", self.score, player_position.x, player_position.y)
    }
}
