use althael::access::clipboard::copy_to_clipboard;
use clipboard::{ClipboardContext, ClipboardProvider};

#[test]
fn test_copy_to_clipboard() {
    let text = "Clipboard test";
    copy_to_clipboard(text);

    let mut ctx: ClipboardContext = ClipboardProvider::new().unwrap();

    let clipboard_contents = ctx.get_contents().unwrap();

    assert_eq!(clipboard_contents, text);
}
