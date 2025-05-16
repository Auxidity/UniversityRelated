use std::fs;
use std::io;
use std::path::{Path, PathBuf};

fn list_dir_entry_paths(dir_path: &str) -> io::Result<()> {
    // Create a PathBuf from the provided directory path
    let path = Path::new(dir_path);

    // Read the contents of the directory
    let entries = fs::read_dir(path)?;

    // Iterate over the directory entries
    for entry in entries {
        let entry = entry?;

        // Get the file name or directory name as a PathBuf
        let entry_path = entry.path();

        // Print the path
        if entry_path.is_dir() {
            // For directories, add a trailing slash to indicate it's a directory
            println!("{}{}", entry_path.display(), "/");
        } else {
            println!("{}", entry_path.display());
        }
    }

    Ok(())
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: find PATH");
        std::process::exit(1);
    }
    let path = &args[1];
    list_dir_entry_paths(path)?;
    Ok(())
}


