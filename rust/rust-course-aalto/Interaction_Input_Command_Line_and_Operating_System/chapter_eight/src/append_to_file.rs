use std::fs;
use std::io::{self, Write};
use std::path::Path;

fn append_to_file(source: &str, dest: &str) -> io::Result<()>{
    let content = fs::read(source)?;
    
    if !Path::new(dest).exists(){
        fs::write(dest, "").expect("Unable to write to file");        
    }
    let mut file = fs::OpenOptions::new()
        .append(true)
        .open(dest)?;
    
    file.write_all(&content)?;

    Ok(())
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: append SOURCE DEST");
        std::process::exit(1);
    }
    let source = &args[1];
    let dest = &args[2];
    append_to_file(source, dest)?;
    Ok(())
}


