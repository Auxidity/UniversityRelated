use std::io::{self,Write};
use std::thread::sleep;
use std::time::Duration;
use termion::event::Key;
use termion::cursor;
use termion::input::TermRead;
use termion::raw::IntoRawMode;
use crate::access::clipboard::copy_to_clipboard;
use crate::access::fetch::{fetch_all_ids, fetch_email, fetch_handle, fetch_id, fetch_pw};
use crate::access::remove::remove;
use crate::config::{get_max, get_min, get_pwlen, update_config};
use crate::encryption::encryption::generate_salt;
use crate::generation::combined::{edit, generate, verification};

#[derive(PartialEq)]
enum Mode {
    Init,
    InitDoubleCheck,
    Normal,
    Command,
    Append,
    Remove,
    Config,
    SetPwlen,
    SetNamemin,
    SetNamemax,
    AppendHandle,
    AppendEmail,
    Edit,
    Fetch,
    PostFetch,
    EditPW,
    EditEmail,
    SelectHandle,
    List,
}

pub fn app() {
    let stdin = io::stdin();
    let stdout = io::stdout().into_raw_mode().unwrap();
    let mut stdout = io::BufWriter::new(stdout);
    
    let mut mode = Mode::Init;
    
    fn display_mode<W: Write>(stdout: &mut W, mode: &Mode) {
        let (_, height) = termion::terminal_size().unwrap();
        write!(
            stdout,
            "{}{}{}",
            cursor::Goto(1, height),
            termion::clear::CurrentLine,
            match mode {
                Mode::Init => format!("INIT").to_string(),
                Mode::InitDoubleCheck => format!("INIT - VERIFICATION").to_string(),
                Mode::Normal => format!("NORMAL").to_string(),
                Mode::Command => format!("COMMAND").to_string(),
                Mode::Append => format!("APPEND").to_string(),
                Mode::Remove => format!("REMOVE").to_string(),
                Mode::Config => format!("CONFIG").to_string(),
                Mode::SetPwlen => format!("CONFIG - PWLEN").to_string(),
                Mode::SetNamemin => format!("CONFIG - NAME MIN").to_string(),
                Mode::SetNamemax => format!("CONFIG - NAME MAX").to_string(),
                Mode::AppendHandle => format!("APPEND - HANDLE").to_string(),
                Mode::AppendEmail => format!("APPEND - EMAIL").to_string(),
                Mode::Edit => format!("EDIT").to_string(),
                Mode::Fetch => format!("FETCH").to_string(),
                Mode::PostFetch => format!("POST-FETCH").to_string(),
                Mode::EditPW => format!("EDIT - PW").to_string(),
                Mode::EditEmail => format!("EDIT - EMAIL").to_string(),
                Mode::SelectHandle => format!("EDIT - SELECT HANDLE").to_string(),
                Mode::List => format!("LIST").to_string(),
            }
        )
        .unwrap();
        stdout.flush().unwrap();
    }

    fn reposition_cursor<W: Write>(stdout: &mut W, buffer: &str, mode: &Mode) {
        let (_, height) = termion::terminal_size().unwrap();
        write!(stdout, "{}{}", cursor::Goto(1, height - 1), termion::clear::CurrentLine).unwrap();
        // If we're in Mode::Init, replace input with asterisks
        let display_buffer = if *mode == Mode::Init || *mode == Mode::InitDoubleCheck {
            std::iter::repeat("*").take(buffer.len()).collect::<String>()
        } else {
            buffer.to_string()  // Just show the input buffer as is
        };
        write!(stdout, "{}", display_buffer).unwrap();

        let buffer_length = display_buffer.chars().count() as u16;
        let cursor_pos = buffer_length + 1;
        if buffer_length > 0 {
            write!(stdout, "{}",
                cursor::Goto(cursor_pos, height -1)
                ).unwrap();
        }


        stdout.flush().unwrap();
    }

    //Insert a cool ascii art here later. Initialization happens here
    writeln!(stdout, "{}", termion::clear::All).unwrap();
    writeln!(stdout, "If you are using the program for the first time, set the password that will be used to access the accounts\r\n").unwrap();
    writeln!(stdout, "Otherwise, enter the password to access the program. Press Esc to exit\r\n\n").unwrap();
    stdout.flush().unwrap();

    //Initialized variables
    let mut input_buffer = String::new();
    let mut handle = String::new();
    let mut email = String::new();
    let mut pw_boolean = false;

    //Testing variable
    //let test_pw = generate_salt("password");
    let mut final_pw = String::new();
    let mut first_password = String::new();

    //Display current mode line below user input
    display_mode(&mut stdout, &mode);
    reposition_cursor(&mut stdout, &input_buffer.clone(), &mode);

    
    //Key press listener, all app logic will be here and changes to logic should be made here.
    for c in stdin.keys() {
        match mode {
            Mode::Init => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        first_password = input_buffer.clone();
                        input_buffer.clear();
                        writeln!(stdout, "\r\nEnter the password again\r\n").unwrap();
                        mode = Mode::InitDoubleCheck;
                    }
                    Key::Esc => {
                        break;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    _ => {
                        mode = Mode::Init;
                    }
                }
            }

            Mode::InitDoubleCheck => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        if first_password == input_buffer {
                            final_pw = generate_salt(&first_password);
                            first_password.clear();
                            input_buffer.clear();
                            
                            //Clear the first & second pw from memory, and run the verification
                            //function. It attempts to decrypt the data and returns result. In case
                            //there is no contents file, it will specifically give a message but
                            //doesn't return an error (decrypt function that verification uses
                            //would fail on empty file hence it gets skipped if the file doesnt
                            //exist, since it will be generated on runtime).
                            match verification(&final_pw) {
                                Ok(Some(message)) => {
                                    writeln!(stdout, "{}", termion::clear::All).unwrap();
                                    writeln!(stdout, "\r\n{}\r\n\n", message).unwrap();
                                    writeln!(stdout, "\r\n\tAlthael 0.1.0\r\n").unwrap();
                                    writeln!(stdout, "Made by Daniel Kortesmaa, all rights reserved\r\n\n").unwrap();
                                    writeln!(stdout, "Press 'h' to see a full list of commands.\r\nPress 'q' to exit the program.\r\n").unwrap();
                                    mode = Mode::Normal;
                                }
                                Ok(None) => {
                                    writeln!(stdout, "{}", termion::clear::All).unwrap();
                                    writeln!(stdout, "\r\n\tAlthael 0.1.0\r\nMade by Daniel Kortesmaa, all rights reserved\r\n").unwrap();
                                    writeln!(stdout, "Press 'h' to see a full list of commands.\r\nPress 'q' to exit the program.\r\n").unwrap();
                                    mode = Mode::Normal;
                                } 
                                Err(e) => {
                                    writeln!(stdout, "\r\nError: {}\r\n\n",e).unwrap();
                                    mode = Mode::Init;
                                }
                            }
                        } else {
                            writeln!(stdout, "\r\nThe passwords do not match, try again\r\n\n").unwrap();
                            first_password.clear();
                            input_buffer.clear();
                            mode = Mode::Init;
                        }
                    }
                    Key::Esc => {
                        break;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    _ => {
                        mode = Mode::InitDoubleCheck;
                    }
                }
            }
            Mode::Normal => {
                match c.unwrap() {
                    Key::Char('h') => {
                        writeln!(stdout, "\r\nNORMAL MODE\r\nh - View this message\r\n: - Enter command mode\r\nc - View the current configuration\r\nl - Lists the currently stored handles\r\nq - Exit the program\r\n").unwrap();
                        writeln!(stdout, "COMMAND MODE\r\na - Enter append mode\r\nr - Enter remove mode\r\nc - Enter config mode\r\nf - Enter fetch mode\r\ne - Enter edit mode\r\nESC - Return to normal mode\r\n").unwrap();
                        writeln!(stdout, "APPEND MODE\r\n1 - Type the identifier for the account (e.g. 'youtube') and press enter\r\n2 - Type email which you want to be associated with the account\r\n3 - After setting identifier and email, press 3 to append it\r\nESC - Return to command mode\r\n").unwrap();
                        writeln!(stdout, "REMOVE MODE\r\nType the identifier for the account (e.g. 'youtube') and press enter to remove the account details\r\nESC - Return to command mode\r\n").unwrap();
                        writeln!(stdout, "CONFIG MODE\r\nSelect one of the following to configure the contents of config file for autogeneration\r\n1 - Sets the length of password\r\n2 - Sets the minimum length for autogenerated handles\r\n3 - Sets the maximum length for autogenerated handles\r\nESC - Return to command mode\r\n").unwrap();
                        writeln!(stdout, "EDIT MODE\r\n1 - Type the identifier of the account you wish to edit (e.g. 'youtube') and press enter\r\n2 - Type the new email you wish to associate with the account\r\n3 - Enter EDITPW submode\r\n4 - Edits the selected account\r\nESC - Return to command mode\r\n").unwrap();
                        writeln!(stdout, "EDIT PW SUBMODE\r\n0 - Set the boolean value to regenerate password upon edit to false (default value)\r\n1 - Set the boolean value to regenerate password upon edit to true (will reset back to false upon next succesful edit or leaving edit mode)\r\n").unwrap();
                        writeln!(stdout, "FETCH MODE\r\nType the handle to fetch to perform post-fetch operations\r\n").unwrap();
                        writeln!(stdout, "POST-FETCH MODE\r\nFollowing operations are performed on the performed fetch\r\n1 - Copy name to clipboard\r\n2 - Copy password to clipboard\r\n3 - Copy email to clipboard\r\nEsc - Return to command mode\r\n").unwrap();
                        writeln!(stdout, "LIST MODE\r\nEnter - Prints a list of currently stored handles\r\nESC - Return to normal mode.\r\n\n").unwrap();
                    }
                    Key::Char(':') => {
                        mode = Mode::Command;
                    }
                    Key::Char('l') => {
                        writeln!(stdout, "Press enter to view a list of current handles. Press ESC to return back to normal mode.\r\n").unwrap();
                        mode = Mode::List;
                    }
                    Key::Char('c') => {
                        let current_pwlen = get_pwlen();
                        let current_namemin = get_min();
                        let current_namemax = get_max();
                        writeln!(stdout, "Current password length is set at {}\r\nCurrent autogenerated handle minimum length is set at {}\r\nCurrent autogenerated handle maximum length is set at {}\r\n\n", current_pwlen,current_namemin,current_namemax).unwrap();
                    }
                    Key::Esc => break,
                    Key::Char('q') => break,
                    _ => {
                        writeln!(stdout, "Unrecognized command. Press 'h' to view all available commands.\r\n").unwrap();
                    }
                }
            }
            Mode::Command => {
                match c.unwrap() {
                    Key::Char('a') => {
                        writeln!(stdout, "\r\nPress 1 to set handle with which to search the account later (e.g. 'youtube')\r").unwrap();
                        writeln!(stdout, "Press 2 to set the email associated with the handle\r").unwrap();
                        writeln!(stdout, "Press 3 to save the handle + email combination and generate random name and password for them\r\n").unwrap();
                        mode = Mode::Append;
                    }
                    Key::Char('r') => {
                        writeln!(stdout, "\r\nType the handle which you wish to delete and press enter (Note, this will only delete it from being stored locally, the account itself will still exist and you need to delete it from service providers side to entirely delete it\r\n)").unwrap();
                        mode = Mode::Remove;
                    }
                    Key::Char('c') => {
                        writeln!(stdout, "\r\nPress 1 to configure password length (e.g. 8 for 8 character password)\r").unwrap();
                        writeln!(stdout, "Press 2 to configure the minimum handle length (e.g. 6 for names like 'Altruist')\r").unwrap();
                        writeln!(stdout, "Press 3 to configure the maximum handle length (e.g. 12 to prevent names like 'Iamareallylongnamefornogoodreason')\r").unwrap();
                        writeln!(stdout, "Press esc to return to command mode\r\n").unwrap();
                        mode = Mode::Config;
                    }
                    Key::Char('f') => {
                        writeln!(stdout, "\r\nType the handle that you wish to fetch e-mail, password and name for. After that you enter post-fetch mode where pressing 1, 2 and 3 will copy contents to clipboard for use.\r\n").unwrap();
                        mode = Mode::Fetch;
                    }
                    Key::Char('e') => {
                        writeln!(stdout, "\r\nPress 1 to select the handle with which the account details that would be edited are searched\r").unwrap();
                        writeln!(stdout, "Press 2 to prepare new email address for the handle\r").unwrap();
                        writeln!(stdout, "Press 3 to select whether or not a new password should be generated\r").unwrap();
                        writeln!(stdout, "Press 4 to commit changes\r\n").unwrap();
                        mode = Mode::Edit;
                    }
                     Key::Esc => {
                        mode = Mode::Normal;
                    }
                      _ => {
                        mode = Mode::Command;
                    }
                }
            }
            Mode::SetPwlen => {
                let old_max = get_max();
                let old_min = get_min();
                match c.unwrap() {
                    Key::Char('\n') => {
                        match input_buffer.trim().parse::<usize>() {
                            Ok(number) => {
                                let _ = update_config(old_min,old_max,number);
                                writeln!(stdout, "\r\nPassword length updated succesfully\r\n\n").unwrap();
                                mode = Mode::Config;
                            }
                            Err(_) => {
                                writeln!(stdout, "\r\nPassword length must be given as an integer\r\n\n").unwrap();
                                input_buffer.clear();
                            }
                        }
                        input_buffer.clear();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Config;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    _ => {
                        mode = Mode::SetPwlen;
                    }
                }
            }
            Mode::SetNamemin => {
                let old_max = get_max();
                let old_pwlen = get_pwlen();
                match c.unwrap() {
                    Key::Char('\n') => {
                        match input_buffer.trim().parse::<usize>() {
                            Ok(number) => {
                                if number < old_max {
                                let _ = update_config(number,old_max, old_pwlen);
                                writeln!(stdout, "\r\nName minimum length updated succesfully\r\n\n").unwrap();
                                mode = Mode::Config;
                                } else {
                                    writeln!(stdout, "\r\nName minimum length must be smaller than the maximum length\r\n\n").unwrap();
                                    input_buffer.clear();
                                }
                            }
                            Err(_) => {
                                writeln!(stdout, "\r\nName minimum length must be given as an integer\r\n\n").unwrap();
                                input_buffer.clear();
                            }
                        }
                        input_buffer.clear();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Config;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    _ => {
                        mode = Mode::SetNamemin;
                    }
                }
            }
            Mode::SetNamemax => {
                let old_min = get_min();
                let old_pwlen = get_pwlen();
                match c.unwrap() {
                    Key::Char('\n') => {
                        match input_buffer.trim().parse::<usize>() {
                            Ok(number) => {
                                if number > old_min {
                                    let _ = update_config(old_min,number, old_pwlen);
                                    writeln!(stdout, "\r\nName maximum length updated succesfully\r\n\n").unwrap();
                                    mode = Mode::Config;
                                } else {
                                    writeln!(stdout, "\r\nName maximum length must be larger than minimum length\r\n\n").unwrap();
                                    input_buffer.clear();
                                }
                            }
                            Err(_) => {
                                writeln!(stdout, "\r\nName maximum length must be given as an integer\r\n\n").unwrap();
                                input_buffer.clear();
                            }
                        }
                        input_buffer.clear();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Config;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    _ => {
                        mode = Mode::SetNamemax;
                    }
                }
            }
            Mode::Config => {
                match c.unwrap() {
                    Key::Char('1') => {
                        mode = Mode::SetPwlen;
                    }

                    Key::Char('2') => {
                        mode = Mode::SetNamemin;
                    }
                    Key::Char('3') => {
                        mode = Mode::SetNamemax;
                    }
                    Key::Backspace => {
                        mode = Mode::Command;
                    }
                    Key::Esc => {
                        mode = Mode::Normal;
                    }
                    _ => {
                        mode = Mode::Config;
                    }
                }
            }

            Mode::Append => {
                match c.unwrap() {
                    Key::Char('1') => {
                        mode = Mode::AppendHandle;
                    }
                    Key::Char('2') => {
                        mode = Mode::AppendEmail;
                    }
                    Key::Char('3') => {
                    //Append to file
                        if handle.clone().is_empty() {
                            writeln!(stdout, "\r\nHandle is not set\r\n\n").unwrap();
                            mode = Mode::AppendHandle;
                        } else if email.clone().is_empty() {
                            writeln!(stdout, "\r\nEmail is not set\r\n\n").unwrap();
                            mode = Mode::AppendEmail;
                        } else {
                            match generate(handle.clone(), email.clone(), get_pwlen(), get_min(), get_max(), &final_pw) {
                                Ok(_) => {
                                    writeln!(stdout, "\r\nSuccesfully appended an entry\r\n\n").unwrap();
                                    handle.clear();
                                    email.clear();
                                    mode = Mode::Append;
                                }
                                Err(e) => {
                                    //Commented out below is for debugging when error propagation doesn't work.. REMEMBER TO \r\n AT END
                                    //writeln!(stdout, "\r\nError encountered\r\n\n").unwrap();
                                    writeln!(stdout, "\r\nError during appending: {}\r\n\n", e).unwrap();
                                }
                            }
                        }
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        email.clear();
                        handle.clear();
                        mode = Mode::Normal;
                    }
                    Key::Backspace => {
                        input_buffer.clear();
                        mode = Mode::Command;
                    }
                    _ => {
                        mode = Mode::Append;
                    }
                }
            }
            Mode::AppendHandle => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        handle = input_buffer.clone();
                        if handle.clone().is_empty() {
                            writeln!(stdout, "\r\nHandle can't be an empty string\r\n").unwrap();
                            mode = Mode::AppendHandle;
                        } else {
                            writeln!(stdout, "\r\nHandle set as {}\r\n\n", handle.clone()).unwrap();
                            input_buffer.clear();
                            mode = Mode::Append;
                        }
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Append;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    _ => {
                        mode = Mode::AppendHandle;
                    }
                }
            }
            Mode::AppendEmail => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        email = input_buffer.clone();
                        if email.clone().is_empty() {
                            writeln!(stdout, "\r\nEmail can't be an empty string\r\n").unwrap();
                            mode = Mode::AppendEmail;
                        } else {
                            writeln!(stdout, "\r\nEmail set as {}\r\n\n", email.clone()).unwrap();
                            input_buffer.clear();
                            mode = Mode::Append;
                        }
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Append;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    _ => {
                        mode = Mode::AppendEmail;
                    }
                }
            }
            Mode::Remove => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        if input_buffer.clone().is_empty() {
                            writeln!(stdout, "\r\nCannot remove an empty string\r\n\n").unwrap();
                            mode = Mode::Remove;
                        } else {
                            match remove(input_buffer.clone(), &final_pw) {
                                Ok(_) => {
                                    writeln!(stdout, "\r\nSuccesfully removed {}\r\n\n", input_buffer.clone()).unwrap();
                                    input_buffer.clear();
                                    mode = Mode::Command;
                                }
                                Err(e) => {
                                    writeln!(stdout, "\r\nError during removal: {}\r\n\n", e).unwrap();
                                    mode = Mode::Remove;
                                }
                            }
                        }
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Command;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    _ => {
                        mode = Mode::Remove;
                    }

                }
            }
            Mode::Fetch => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        if input_buffer.clone().is_empty() {
                            writeln!(stdout, "\r\nCannot search an empty string\r\n\n").unwrap();
                            mode = Mode::Fetch;
                        } else {
                            match fetch_id(input_buffer.clone(), &final_pw) {
                                Ok(matching_items) => {
                                    if matching_items.is_empty() {
                                        writeln!(stdout, "\r\nNo matches found with {}\r\n\n", input_buffer.clone()).unwrap();
                                        input_buffer.clear();
                                        mode = Mode::Fetch;
                                    } else {
                                        writeln!(stdout, "\r\nSuccesfully fetched {}\r\n\n", input_buffer.clone()).unwrap();
                                        handle = input_buffer.clone();
                                        input_buffer.clear();
                                        mode = Mode::PostFetch;
                                    }
                                }
                                Err(e) => {
                                    writeln!(stdout, "\r\nError during fetching: {}\r\n\n", e).unwrap();
                                    input_buffer.clear();
                                    mode = Mode::Fetch;
                                }
                            }
                        }
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Command;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    _ => {
                        mode = Mode::Fetch;
                    }

                }
            }
            Mode::PostFetch => {
               match c.unwrap() {
                    Key::Char('1') => {
                        let cloned_handle = handle.clone();
                        if let Ok(fetched) = fetch_handle(cloned_handle, &final_pw) {
                            if let Some(first) = fetched.get(0) { 
                                copy_to_clipboard(&first);
                                writeln!(stdout, "\r\nAccount handle copied to clipboard\r\n").unwrap();
                                mode = Mode::PostFetch;
                            }
                        }
                    }
                    Key::Char('2') => {
                        let cloned_handle = handle.clone();
                        if let Ok(fetched) = fetch_pw(cloned_handle, &final_pw) {
                            if let Some(first) = fetched.get(0) { 
                                copy_to_clipboard(&first);
                                writeln!(stdout, "\r\nAccount password copied to clipboard\r\n").unwrap();
                                mode = Mode::PostFetch;
                            }
                        }
                    }
                    Key::Char('3') => {
                        let cloned_handle = handle.clone();
                        if let Ok(fetched) = fetch_email(cloned_handle, &final_pw) {
                            if let Some(first) = fetched.get(0) { 
                                copy_to_clipboard(&first);
                                writeln!(stdout, "\r\nAccount email copied to clipboard\r\n").unwrap();
                                mode = Mode::PostFetch;
                            }
                        }
                    }
                    Key::Esc => {
                        handle.clear();
                        mode = Mode::Command;
                    }
                    _ => {
                        mode = Mode::PostFetch;
                    }
               }
            }
            Mode::Edit => {
                match c.unwrap() {
                    Key::Char('1') => {
                        writeln!(stdout, "\r\nType the identifier for the account that you wish to edit\r\n\n").unwrap();
                        mode = Mode::SelectHandle;
                    }
                    Key::Char('2') => {
                        writeln!(stdout, "\r\nType the new email address and press enter\r\n\n").unwrap();
                        mode = Mode::EditEmail;
                    }
                    Key::Char('3') => {
                        writeln!(stdout, "\r\nPress 0 to disable password regeneration\r\nPress 1 to enable password regeneration\r\n\n").unwrap();
                        mode = Mode::EditPW;
                    }
                    Key::Char('4') => {
                    //Edit in place
                        if handle.clone().is_empty() {
                            writeln!(stdout, "\r\nHandle that would be edited was not selected\r\n\n").unwrap();
                            mode = Mode::SelectHandle;
                        } else {
                            let option_email: Option<String> = if email.clone().is_empty() { None } else { Some(email.clone()) };
                            let option_pw : Option<usize> = if pw_boolean == true { Some(get_pwlen()) } else { None };
                            match edit(handle.clone(), option_email, option_pw, &final_pw) {
                                Ok(_) => {
                                    writeln!(stdout, "\r\nSuccesfully attempted to edit {}\r", handle.clone()).unwrap();
                                    if email.clone().is_empty() { writeln!(stdout, "\rEmail was not set to be changed so it wasn't edited.\r\n").unwrap(); }
                                    email.clear();
                                    if pw_boolean == false { writeln!(stdout, "\rPassword was not set to be changed so it wasn't regenerated.\r\n").unwrap(); }
                                    pw_boolean = false;
                                    handle.clear();
                                    mode = Mode::Command;
                                }
                                Err(e) => {
                                    writeln!(stdout, "\r\nError during editing: {}\r\n\n", e).unwrap();
                                }
                            }
                        }
                    }
                    Key::Esc => {
                        email.clear();
                        pw_boolean = false;
                        handle.clear();
                        mode = Mode::Command;
                    }
                    _ => {
                        mode = Mode::Edit;
                    }
                }
            }
            Mode::EditEmail => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        email = input_buffer.clone();
                        if email.clone().is_empty() {
                            writeln!(stdout, "\r\nEmail can't be an empty string\r\n").unwrap();
                            mode = Mode::AppendEmail;
                        } else {
                            writeln!(stdout, "\r\nEmail wil be set as {} upon edit\r\n\n", email.clone()).unwrap();
                            input_buffer.clear();
                            mode = Mode::Edit;
                        }
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Edit;
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    _ => {
                        mode = Mode::EditEmail;
                    }
                }
            }
            Mode::EditPW => {
                match c.unwrap() {
                    Key::Char('0') => {
                        writeln!(stdout, "\r\nPassword will not be regenerated when an entry is edited\r\n").unwrap();
                        pw_boolean = false;
                        mode = Mode::Edit;
                    }
                    Key::Char('1') => {
                        writeln!(stdout, "\r\nPassword will be regenerated when an entry is edited\r\n").unwrap();
                        pw_boolean = true;
                        mode = Mode::Edit;
                    }
                    Key::Esc => {
                        mode = Mode::Edit;
                    }
                    _ => {
                        mode = Mode::EditPW;
                    }
                }
            }
            Mode::SelectHandle => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        if input_buffer.clone().is_empty() {
                            writeln!(stdout, "\r\nHandle cannot be an empty string\r\n\n").unwrap();
                            mode = Mode::Fetch;
                        } else {
                            match fetch_id(input_buffer.clone(), &final_pw) {
                                Ok(matching_items) => {
                                    if matching_items.is_empty() {
                                        writeln!(stdout, "\r\nNo matches found with {}\r\n\n", input_buffer.clone()).unwrap();
                                        input_buffer.clear();
                                        mode = Mode::Edit;
                                    } else {
                                        writeln!(stdout, "\r\nSuccesfully found {}, this entry is the target to be edited now\r\n", input_buffer.clone()).unwrap();
                                        handle = input_buffer.clone();
                                        input_buffer.clear();
                                        mode = Mode::Edit;
                                    }
                                }
                                Err(e) => {
                                    writeln!(stdout, "\r\nError during fetching: {}\r\n\n", e).unwrap();
                                    input_buffer.clear();
                                    mode = Mode::Edit;
                                }
                            }
                        }
                    }
                    Key::Backspace => {
                        input_buffer.pop();
                    }
                    Key::Char(c) => {
                        input_buffer.push(c);
                    }
                    Key::Esc => {
                        input_buffer.clear();
                        mode = Mode::Edit;
                    }
                    _ => {
                        mode = Mode::SelectHandle;
                    }
                }
            }
            Mode::List => {
                match c.unwrap() {
                    Key::Char('\n') => {
                        match fetch_all_ids(&final_pw) {
                            Ok(ids) => {
                                if ids.is_empty() {
                                    writeln!(stdout, "\r\nNo handles have been stored\r\n\n").unwrap();
                                    mode = Mode::List;
                                } else {
                                    writeln!(stdout, "\r\nFollowing handles have been found:\r\n{}", ids.join("\r\n")).unwrap();
                                    //Line below fixes visual bug where last entry is being
                                    //overwritten by input entry field. I dont know what causes it.
                                    writeln!(stdout, "").unwrap();
                                }
                            }
                            Err(e) => {
                                writeln!(stdout, "\r\nError during fetching: {}\r\n\n", e).unwrap();
                                mode = Mode::List;
                                }
                        }

                    }
                    Key::Esc => {
                        mode = Mode::Normal;
                    }
                    _ => {
                        mode = Mode::List;
                    }
                }
            }
        }

        //Update mode
        display_mode(&mut stdout, &mode);
        reposition_cursor(&mut stdout, &input_buffer.clone(), &mode);


        stdout.flush().unwrap();
        //to avoid high cpu useage, probably lower this to about 20?
        sleep(Duration::from_millis(20));
    }

    //Clear status line before exit
    write!(stdout, "{}{}", cursor::Goto(1, termion::terminal_size().unwrap().1), termion::clear::CurrentLine).unwrap();
    //Exit message and stdout flush
    writeln!(stdout, "Goodbye\r\n").unwrap();
    stdout.flush().unwrap();

}
