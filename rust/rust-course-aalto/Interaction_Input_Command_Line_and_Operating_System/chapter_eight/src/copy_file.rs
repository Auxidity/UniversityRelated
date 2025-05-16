use std::fs;
use std::io;

fn copy(source:&str, destination:&str) -> io::Result<()> {
    let content = fs::read(source)?;
    fs::write(destination, content)?;
    Ok(())
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: cp SOURCE DEST");
        std::process::exit(1);
    }
    let source = &args[1];
    let dest = &args[2];

    copy(source, dest)?;

    Ok(())
}


