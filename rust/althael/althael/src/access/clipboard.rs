use clipboard::ClipboardProvider;
use clipboard::ClipboardContext;

//Set text to clipboard for ctrl v pasting, call in app on fetched field
pub fn copy_to_clipboard(text: &str) {
    let mut ctx: ClipboardContext = ClipboardProvider::new().unwrap();
    ctx.set_contents(text.to_owned()).unwrap();
}
