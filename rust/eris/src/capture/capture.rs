use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::SampleFormat;
//use cpal::{SampleFormat, Stream, StreamError};
//
use crate::fft::fourier::{process_audio_data_to_time_domain, process_audio_in_frequency_domain};

pub fn capture() {
    let host = cpal::default_host();
    let input_device = host
        .default_input_device()
        .expect("No input device available");

    let supported_configs = input_device
        .supported_input_configs()
        .expect("Error querying configs");

    let config = supported_configs
        .filter(|c| c.sample_format() == SampleFormat::F32)
        .next()
        .expect("No supported f32 input configs")
        .with_max_sample_rate()
        .into();

    let stream = input_device
        .build_input_stream(
            &config,
            move |data: &[f32], _: &cpal::InputCallbackInfo| {
                let mut freq_data = process_audio_in_frequency_domain(data);

                //maybe do sth?
                process_audio_data_to_time_domain(freq_data.as_mut_slice());
            },
            move |err| {
                eprintln!("Error: {:?}", err);
            },
            None,
        )
        .expect("Failed to create input stream");

    stream.play().expect("Failed to start input stream");
}
