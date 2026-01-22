use byteorder::{BigEndian, ReadBytesExt};
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use std::net::UdpSocket;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;

//NOTE!! This is not correct format, which will cause the stream to seem robotic

const RTP_PORT: u16 = 5004;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let host = cpal::default_host();
    let device = host
        .default_output_device()
        .expect("No output device available");
    let config = device.default_output_config()?.config();

    println!("Output device: {:?}", device.name()?);
    println!("Using config: {:?}", config);

    let socket = UdpSocket::bind(("0.0.0.0", RTP_PORT))?;
    println!("Listening for RTP on port {}", RTP_PORT);

    let audio_buffer = Arc::new(Mutex::new(Vec::<i16>::new()));
    let audio_buffer_clone = Arc::clone(&audio_buffer);

    // Audio playback stream
    let stream = device.build_output_stream(
        &config,
        move |output: &mut [i16], _| {
            let mut buffer = audio_buffer_clone.lock().unwrap();
            let len = output.len().min(buffer.len());
            output[..len].copy_from_slice(&buffer[..len]);
            buffer.drain(..len);
        },
        |err| eprintln!("Stream error: {}", err),
        None,
    )?;
    stream.play()?;

    // Receiver loop
    thread::spawn(move || {
        let mut buf = [0u8; 1500];
        loop {
            match socket.recv(&mut buf) {
                Ok(size) if size > 12 => {
                    let payload = &buf[12..size]; // Skip RTP header
                    let mut cursor = std::io::Cursor::new(payload);
                    let mut samples = Vec::new();
                    while let Ok(sample) = cursor.read_i16::<BigEndian>() {
                        samples.push(sample);
                    }

                    let mut buffer = audio_buffer.lock().unwrap();
                    buffer.extend(samples);
                }
                Ok(_) => continue,
                Err(e) => {
                    eprintln!("Receive error: {}", e);
                }
            }
        }
    });

    println!("Receiving and playing audio. Press Ctrl+C to exit.");
    loop {
        std::thread::sleep(std::time::Duration::from_secs(1));
    }
}
