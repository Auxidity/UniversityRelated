/* READ THIS
    This is my attempt at live streaming audio data.
    This was tested with apollo and vlc.
    Apollo is a real time receiver, but it distorts the audio on receive. This is entirely local testbed.
    VLC uses stream.sdp to build the output stream that you can RTP over to vlc. This worked just fine.
    Plan was to add signal processing to this, but this is purely for streaming. Keeping it as is for later reference
*/

// use byteorder::{BigEndian, WriteBytesExt};
// use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
// use std::fs::OpenOptions;
use std::io::Write;
use std::net::UdpSocket;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc::{self, Sender};

const RTP_DEST: &str = "192.168.1.176:5004"; //Reformat the aquisition of this

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let host = cpal::default_host();

    let device = host
        .default_input_device()
        .expect("No input device available");
    let config = device.default_input_config()?;
    println!("Input device: {:?}", device.name()?); //Debug
    println!("Default input config: {:?}", config);

    let (tx, rx) = mpsc::channel::<Vec<u8>>();

    std::thread::spawn(move || {
        let mut socket = loop {
            match UdpSocket::bind("0.0.0.0:0") {
                Ok(sock) => match sock.connect(RTP_DEST) {
                    Ok(_) => {
                        println!("[RTP] connected to {}", RTP_DEST);
                        break sock;
                    }
                    Err(e) => {
                        eprintln!(
                            "[RTP] failed to connect with error: {e}, retrying in 5 seconds..."
                        );
                        std::thread::sleep(std::time::Duration::from_secs(5));
                    }
                },
                Err(e) => {
                    eprintln!("[RTP] Bind failed with error: {e}, retrying in 5 seconds...");
                    std::thread::sleep(std::time::Duration::from_secs(5));
                }
            }
        };

        let mut sequence_number: u16 = 0;
        let mut timestamp: u32 = 0;
        for packet_data in rx {
            //Local debug version of audio data
            {
                let mut file = OpenOptions::new()
                    .create(true)
                    .append(true)
                    .open("debug_sender.raw")
                    .unwrap();
                let _ = file.write_all(&packet_data);
            }

            let samples_per_packet = (packet_data.len() / 2) / 2;

            // RTP header (12 bytes)0
            let mut rtp_packet = vec![];
            rtp_packet.push(0x80); // Version 2
            rtp_packet.push(96); // Payload type 96 (L16/44100/2)
            rtp_packet.write_u16::<BigEndian>(sequence_number).unwrap();
            rtp_packet.write_u32::<BigEndian>(timestamp).unwrap();
            rtp_packet.write_u32::<BigEndian>(12345).unwrap(); // SSRC. "random"

            rtp_packet.extend_from_slice(&packet_data);

            match socket.send(&rtp_packet) {
                Ok(_) => {
                    sequence_number = sequence_number.wrapping_add(1);
                    timestamp = timestamp.wrapping_add(samples_per_packet as u32);
                }
                Err(e) => {
                    eprintln!("[RTP] Send failed with error: {e}. Attempting to reconnect..");
                    loop {
                        match UdpSocket::bind("0.0.0.0:0") {
                            Ok(new_socket) => match new_socket.connect(RTP_DEST) {
                                Ok(_) => {
                                    println!("[RTP] connected to {}", RTP_DEST);
                                    socket = new_socket;
                                    break;
                                }
                                Err(e) => {
                                    eprintln!(
                                        "[RTP] failed to connect with error: {e}, retrying in a second..."
                                    );
                                    std::thread::sleep(std::time::Duration::from_secs(5));
                                }
                            },
                            Err(e) => {
                                eprintln!(
                                    "[RTP] Bind failed with error: {e}, retrying in a second..."
                                );
                                std::thread::sleep(std::time::Duration::from_secs(5));
                            }
                        }
                    }
                }
            }
        }
    });

    //Honestly, kind of unneccesary as is, but it might be that I need to manage multiple thread cleanup that I can hide behind this
    let running = Arc::new(AtomicBool::new(true));
    {
        let running = running.clone();
        ctrlc::set_handler(move || {
            running.store(false, Ordering::Relaxed);
        })?;
    }

    let sample_format = config.sample_format();

    let stream = match sample_format {
        cpal::SampleFormat::I16 => run_stream::<i16>(&device, &config.into(), tx),
        cpal::SampleFormat::U16 => run_stream::<u16>(&device, &config.into(), tx),
        cpal::SampleFormat::F32 => run_stream::<f32>(&device, &config.into(), tx),
        _ => todo!("Sample format {:?} not supported", sample_format),
    };

    println!("Recording and streaming via RTP.. Kill with ctrl+c");

    while running.load(Ordering::Relaxed) {
        std::thread::sleep(std::time::Duration::from_millis(10));
    }
    println!("\nCtrl+C pressed");
    drop(stream);

    Ok(())
}

fn run_stream<T>(
    device: &cpal::Device,
    config: &cpal::StreamConfig,
    tx: Sender<Vec<u8>>,
) -> Result<cpal::Stream, Box<dyn std::error::Error>>
where
    T: cpal::Sample + cpal::SizedSample + Into<f32>,
{
    let channels = config.channels as usize;

    let stream = device.build_input_stream(
        config,
        move |data: &[T], _: &cpal::InputCallbackInfo| {
            let mut buffer = vec![];
            for frame in data.chunks(channels) {
                for sample in frame {
                    let val: f32 = (*sample).into();
                    let int_val =
                        (val * i16::MAX as f32).clamp(i16::MIN as f32, i16::MAX as f32) as i16;
                    buffer.write_i16::<BigEndian>(int_val).unwrap();
                }
            }
            let _ = tx.send(buffer);
        },
        |err| eprintln!("an error occurred on stream: {}", err),
        None,
    )?;

    stream.play()?;
    Ok(stream)
}
