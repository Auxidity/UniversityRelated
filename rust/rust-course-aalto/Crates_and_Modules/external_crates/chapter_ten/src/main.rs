mod quiz;
mod util;

use quiz::practice_problems_random_order;

fn main() {
    let problems = [
        ("What year was Speedcoding first released?", "1953"),
        ("What year was Fortran first released?", "1957"),
        ("What year was Lisp first released?", "1958"),
        ("What year was BASIC first released?", "1964"),
        ("What year was B first released?", "1969"),
        ("What year was C first released?", "1972"),
        ("What year was Bourne shell first released?", "1979"),
        ("What year was C++ first released?", "1985"),
        ("What year was Python first released?", "1991"),
        ("What year was JavaScript first released?", "1995"),
        ("What year was Java first released?", "1995"),
    ];
    practice_problems_random_order(&problems);
}
