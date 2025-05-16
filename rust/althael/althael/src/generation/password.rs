use rand::{Rng, thread_rng};
use rand::distributions::Alphanumeric;

#[allow(dead_code)]
pub fn generate_password(length: usize) -> String {
    let rand_string: String = thread_rng()
        .sample_iter(&Alphanumeric)
        .take(length)
        .map(char::from)
        .collect();

    rand_string
}
