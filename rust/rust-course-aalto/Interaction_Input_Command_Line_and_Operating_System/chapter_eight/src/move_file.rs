use std::io;
use std::fs;

fn mv(source: &str, destination: &str) -> io::Result<()>{
    fs::rename(source, destination);
    Ok(())
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: mv SOURCE DEST");
        std::process::exit(1);
    }
    let source = &args[1];
    let dest = &args[2];
    mv(source, dest)?;
    Ok(())
}


