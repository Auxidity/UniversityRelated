use crate::point::{self, Direction};

use crate::point::Point2d;
use crate::traits::Position;
//Poisition
use rand::{
    distributions::{uniform::SampleUniform, Standard},
    prelude::Distribution,
    rngs::ThreadRng,
    Rng,
};
use std::ops::Range;


#[allow(unused)]
pub struct Player{
    speed: f64,
    health: u8,
    position: point::Point2d<f64>,
    direction: point::Direction
}

impl Default for Player {
    fn default() -> Self {
        let position = Point2d {
            x : 40.0,
            y: 24.0,
        };

        Player {
            speed: 0.0,
            health: 10,
            position,
            direction: Direction{x: 0.0, y: -1.0},
        }
    }
}

impl Player {
    pub fn is_alive(&self) -> bool {
        self.health > 0 
    }

    pub fn take_damage(&mut self, damage: u8) {
        self.health -= damage;
    }
    
    pub fn health(&self) -> u8 {
        self.health
    }

    pub fn speed(&self) -> f64 {
        self.speed
    }

    pub fn builder() -> PlayerBuilder {
        PlayerBuilder::default()
    }

    pub fn position(&self) -> point::Point2d<f64> {
        self.position
    }
    
    pub fn accelerate(&mut self) {
        if self.speed < 1.0 {
        self.speed = self.speed + 0.1;
        } else { self.speed = 1.0 }
    }
    pub fn decelerate(&mut self) {
        if self.speed > 0.0 {
        self.speed = self.speed - 0.1;
        } else {self.speed = 0.0 }
    }
    pub fn move_forward(&mut self) {
        self.position.x += self.direction.x * self.speed;
        self.position.y += self.direction.y * self.speed;
    }
    pub fn forward_position(&self) -> Point2d<u16> {
        let forward_x = self.position.x + self.direction.x * self.speed;
        let forward_y = self.position.y + self.direction.y * self.speed;

        Point2d { x: forward_x, y: forward_y }.to_u16()
    }

    pub fn turn_right(&mut self) {
        self.direction.turn_right();
    }

    pub fn turn_left(&mut self){
        self.direction.turn_left();
    }
}
impl Position<f64> for Player {
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

pub struct PlayerBuilder {
    speed: f64,
    health: u8,
    position: point::Point2d<f64>,
    direction: point::Direction,
}

impl Default for PlayerBuilder {
   fn default() -> Self {
        let default_player = Player::default();
        PlayerBuilder {
            speed: default_player.speed,
            health: default_player.health,
            position: default_player.position,
            direction: default_player.direction,
        }
   } 
}

impl PlayerBuilder {
    pub fn new() -> Self {
        Self::default()
    }
    pub fn build(self) -> Player {
        Player { speed: self.speed, health: self.health , position: self.position , direction: self.direction }
    }
    pub fn speed(mut self, speed: f64)-> Self {
        self.speed = speed;
        self
    }
    pub fn health(mut self, health: u8)-> Self {
        self.health=health;
        self
    }
    pub fn position(mut self, position: point::Point2d<f64>) -> Self {
        self.position = position;
        self
    }
    pub fn direction(mut self, direction_x:f64, direction_y:f64) -> Self {
        self.direction = point::Direction{ x: direction_x, y: direction_y };
        self
    }
}

impl std::fmt::Display for Player {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "*")
    }
}

