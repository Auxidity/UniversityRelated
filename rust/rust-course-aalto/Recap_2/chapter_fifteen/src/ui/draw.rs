use crate::{
    traits::Position,
    unit::{Collectible, Enemy, Player, Wall},
    hud::Hud,
};
use std::{fmt::Display, io::Write};

use crossterm::style::Stylize;
use num::{traits::NumAssign, NumCast};

// this is only an example, modify it to your needs or remove entirely
pub trait Draw<T: NumAssign + Copy + NumCast>: Position<T> + Display {
    fn draw(&self, buffer: &mut impl Write) {
        let position = self.position();

        crossterm::queue!(
            buffer,
            crossterm::cursor::MoveTo(
                position
                    .x
                    .to_f64()
                    .expect("could not convert position x to f64")
                    .round() as u16
                    + 1,
                position
                    .y
                    .to_f64()
                    .expect("could not convert position y to f64")
                    .round() as u16
                    + 1,
            ),
            crossterm::style::Print(self)
        )
        .unwrap();
    }
}

impl Draw<u16> for Wall {
}

impl Draw<u16> for Collectible {
}

impl Draw<f64> for Player {
}

impl Draw<f64> for Enemy {
}

impl <'a> Draw<u16> for Hud<'a> { }
