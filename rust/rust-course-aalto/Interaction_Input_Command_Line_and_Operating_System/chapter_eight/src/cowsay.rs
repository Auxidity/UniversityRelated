use std::env;

const COWSAY: &str = r#"
\  ^__^
 \ (oo)\_______
   (__)\       )\/\
       ||----w |
       ||     ||
"#;

fn prepend_spaces(s: &str, n: usize) -> String {
    let mut s = s.to_string();
    s.insert_str(0, &" ".repeat(n));
    s
}

fn read_line() -> String {
    let cl_args = env::args().skip(1);
    let concatenated_args = cl_args.collect::<Vec<String>>().join(" ");
    concatenated_args
}

fn main() {
    let mut message = read_line();
    if message.is_empty() {
        message.replace_range(.., "Moo!");
    }

    println!("< {} >", message);
    let indent = |s| prepend_spaces(s, message.len() + 4);
    let cow = COWSAY
        .trim()
        .split("\n")
        .map(indent)
        .collect::<Vec<String>>()
        .join("\n");
    println!("{cow}");
}


