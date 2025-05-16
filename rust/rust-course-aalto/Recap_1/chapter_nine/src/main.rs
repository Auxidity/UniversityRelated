use std::fs;
use std::path::Path;
use std::env;

const INDENT_SIZE: usize = 4;


fn print_indented(string: &str, indent_count: usize) -> () {
    let indentation: String = " ".repeat(INDENT_SIZE*indent_count);
    println!("{}{}", indentation, string);
}

fn eprint_indented(string: &str, indent_count: usize) -> (){
    let indentation: String= " ".repeat(INDENT_SIZE * indent_count);
    eprintln!("{}Error: {}", indentation, string);
   
}

fn print_indented_dirname(path: &Path, depth: usize) {
    if path.is_dir(){
        let dir = fs::read_dir(path);
        let dirname = path
            .file_name()
            .unwrap_or(path.as_os_str())
            .to_string_lossy();
        
        print_indented(&dirname, depth);

    } else {
        eprint_indented("No such file or directory (os error 2)", depth);
    }
}

fn print_dir_and_contents(path: &Path, depth: usize) {
    let dir = match fs::read_dir(path) {
        Ok(dir) => dir,
        Err(err) => {
            eprint_indented(&err.to_string(), depth);
            return;
        }
    };

    let dirname = path
        .file_name()
        .unwrap_or(path.as_os_str())
        .to_string_lossy();

    print_indented(&dirname, depth);

    for entry in dir {
        if let Ok(entry) = entry{
            let entry_path = entry.path();
            if entry_path.is_dir(){
                print_dir_and_contents(&entry_path, depth+1);
            } else{
                let filename = entry_path
                    .file_name()
                    .unwrap_or(entry_path.as_os_str())
                    .to_string_lossy();
                print_indented(&filename, depth+1);
            }
        }
    }
}

fn tree(path: &Path, depth: usize) {
    if let Ok(dir) = fs::read_dir(path){
        let dirname = path
            .file_name()
            .unwrap_or(path.as_os_str())
            .to_string_lossy();
        print_indented(&dirname, depth);

        let mut entries: Vec<_> = dir.filter_map(Result::ok).collect();
        entries.sort_by(|a, b| a.file_name().cmp(&b.file_name()));

        for entry in entries {
            let entry_path = entry.path();
            if entry_path.is_dir(){
                tree(&entry_path, depth+1);
            }else {
                print_indented(
                    &entry_path
                        .file_name()
                        .unwrap_or(entry_path.as_os_str())
                        .to_string_lossy(),
                    depth + 1,
                );
            }
        }
    } else {
        let err = std::io::Error::last_os_error();
        eprint_indented(&err.to_string(), depth);
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let path = if args.len() > 1 {
        Path::new(&args[1])
    } else {
        Path::new(".")
    };

    tree(path, 0);
}
