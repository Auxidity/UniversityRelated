// build.rs
fn main() {
    println!("cargo:rustc-link-search=native=lib");
    println!("cargo:rustc-link-lib=dylib=rubberband_wrapper");
    println!("cargo:rustc-link-arg=-Wl,-rpath=lib");
}
