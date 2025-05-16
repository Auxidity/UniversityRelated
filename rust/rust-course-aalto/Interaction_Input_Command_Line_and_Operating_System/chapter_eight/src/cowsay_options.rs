use std::env;

const COWSAY: &str = r#"
\  ^__^
 \ (oo)\_______
   (__)\       )\/\
       ||----w |
       ||     ||
"#;

const TUXSAY: &str = r#"
\   .--.
 \ |o_o |
   |:_/ |
  //   \ \
 (|     | )
/'\_   _/`\
\___)=(___/
"#;

const DRAGONSAY: &str = r#"
\
 \                       / \  //\
  \        |\___/|      /   \//  \\
   \       /0  0  \__  /    //  | \ \
    \     /     /  \/_/    //   |  \  \
          @_^_@'/   \/_   //    |   \   \
          //_^_/     \/_ //     |    \    \
       ( //) |        \///      |     \     \
     ( / /) _|_ /   )  //       |      \     _\
   ( // /) '/,_ _ _/  ( ; -.    |    _ _\.-~        .-~~~^-.
 (( / / )) ,-{        _      `-.|.-~-.           .~         `.
(( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \
(( /// ))      `.   {            }                   /      \  \
 (( / ))     .----~-.\        \-'                 .~         \  `. \^-.
            ///.----..>        \             _ -~             `.  ^-`  ^-_
              ///-._ _ _ _ _ _ _}^ - - - - ~                     ~-- ,.-~
                                                                 /.-~
"#;

fn prepend_spaces(s: &str, n: usize) -> String {
    let mut result = " ".repeat(n);
    result.push_str(s);
    result
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let (animal, message) = match args.len() {
        1 => ("cow".to_string(), "Moo!".to_string()),
        2 => ("cow".to_string(), args[1].clone()),
        _ => {
            let animal = args[1].clone();
            if animal != "cow" && animal != "tux" && animal != "dragon" {
                panic!("Unsupported animal: {}", animal);
            }
            let message = args[2..].join(" ");
            (animal, message)
        }
    };

    let animal_say = match animal.as_str() {
        "cow" => COWSAY,
        "tux" => TUXSAY,
        "dragon" => DRAGONSAY,
        _ => panic!("Unsupported animal: {}", animal),
    };

    println!("< {} >", message);

    let indent = |s| prepend_spaces(s, message.len() + 4);
    let formatted_say = animal_say
        .trim()
        .split("\n")
        .map(indent)
        .collect::<Vec<String>>()
        .join("\n");
    
    println!("{}", formatted_say);
}


