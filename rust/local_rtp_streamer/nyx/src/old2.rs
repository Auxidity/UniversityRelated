/*
*
* READ THIS:
This file is a demonstration of using funDSP to build an output stream.
While plausible, the nature of the signal processing eats a single core entirely because we are processing every frame
instead of processing chunks. This means quite literally 44.1k samples per second on a single core. In the case of reverb,
I tried to use multipass which supposedly should internally work multithreaded.
Issue is, it underruns consistently. Now, I did the testing in resource constrained environment and I am perfectly aware of that fact.
I left this more as reference of something that actually works though, and might return to this if I need by frame DSP. However,
all things considered Im most likely interested in chunk processing, and I am too dumb to implement one (I mean, you could iteratively build a chunk
sized queue and ring buffer the queues, but I think there will be plenty of issues with this approach on funDSP's side that I cant immediately see. I'll revisit this idea later
for feasibility checking)
*/

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::{FromSample, SizedSample};
use fundsp::hacker32::*;

use crossbeam_channel::{Receiver, Sender, bounded};

#[derive(Clone)]
pub struct InputNode {
    receiver: Receiver<(f32, f32)>,
}

impl InputNode {
    pub fn new(receiver: Receiver<(f32, f32)>) -> Self {
        InputNode { receiver }
    }
}

impl AudioNode for InputNode {
    const ID: u64 = 87;
    type Inputs = U0;
    type Outputs = U2;

    #[inline]
    fn tick(&mut self, _input: &Frame<f32, Self::Inputs>) -> Frame<f32, Self::Outputs> {
        let (left, right) = self.receiver.try_recv().unwrap_or((0.0, 0.0));
        [left, right].into()
    }
}

fn main() {
    // Sender / receiver for left and right channels (stereo mic).
    let (sender, receiver) = bounded(4096);

    let host = cpal::default_host();
    let in_device = host.default_input_device().unwrap();
    let in_config = in_device.default_input_config().unwrap();
    match in_config.sample_format() {
        cpal::SampleFormat::F32 => run_in::<f32>(&in_device, &in_config.into(), sender),
        cpal::SampleFormat::I16 => run_in::<i16>(&in_device, &in_config.into(), sender),
        cpal::SampleFormat::U16 => run_in::<u16>(&in_device, &in_config.into(), sender),
        format => eprintln!("Unsupported sample format: {}", format),
    }

    let out_device = host.default_output_device().unwrap();
    let out_config = out_device.default_output_config().unwrap();
    match out_config.sample_format() {
        cpal::SampleFormat::F32 => run_out::<f32>(&out_device, &out_config.into(), receiver),
        cpal::SampleFormat::I16 => run_out::<i16>(&out_device, &out_config.into(), receiver),
        cpal::SampleFormat::U16 => run_out::<u16>(&out_device, &out_config.into(), receiver),
        format => eprintln!("Unsupported sample format: {}", format),
    }
    println!("Processing stereo input to stereo output.");
    loop {
        std::thread::sleep(std::time::Duration::from_secs(1));
    }
}

fn run_in<T>(device: &cpal::Device, config: &cpal::StreamConfig, sender: Sender<(f32, f32)>)
where
    T: SizedSample,
    f32: FromSample<T>,
{
    let channels = config.channels as usize;
    let err_fn = |err| eprintln!("an error occurred on stream: {}", err);
    let stream = device.build_input_stream(
        config,
        move |data: &[T], _: &cpal::InputCallbackInfo| read_data(data, channels, sender.clone()),
        err_fn,
        None,
    );
    if let Ok(stream) = stream {
        if let Ok(()) = stream.play() {
            std::mem::forget(stream);
        }
    }
    println!("Input stream built.");
}

fn read_data<T>(input: &[T], channels: usize, sender: Sender<(f32, f32)>)
where
    T: SizedSample,
    f32: FromSample<T>,
{
    for frame in input.chunks(channels) {
        let mut left = 0.0;
        let mut right = 0.0;
        for (channel, sample) in frame.iter().enumerate() {
            if channel & 1 == 0 {
                left = sample.to_sample::<f32>();
            } else {
                right = sample.to_sample::<f32>();
            }
        }
        if let Ok(()) = sender.try_send((left, right)) {}
    }
}

fn run_out<T>(device: &cpal::Device, config: &cpal::StreamConfig, receiver: Receiver<(f32, f32)>)
where
    T: SizedSample + FromSample<f32>,
{
    let channels = config.channels as usize;

    println!("Debug info: \n{:?}", config);

    let input = An(InputNode::new(receiver));
    //So the reason we dont add reverb is because we underflow if we start to do this. a single
    //core is not enough for this output stream for real time.. Chorus with these parameters is
    //BARELY doable.
    // let reverb = reverb2_stereo(20.0, 3.0, 1.0, 0.2, highshelf_hz(1000.0, 1.0, db_amp(-1.0)));
    let chorus = chorus(0, 0.0, 0.03, 0.2) | chorus(1, 0.0, 0.03, 0.2);
    let graph = input >> chorus;
    // >> (0.8 * reverb & 0.2 * multipass());
    let mut graph = BlockRateAdapter::new(Box::new(graph));
    graph.set_sample_rate(config.sample_rate.0 as f64);

    let mut next_value = move || graph.get_stereo();

    let err_fn = |err| eprintln!("An error occurred on stream: {}", err);
    let stream = device.build_output_stream(
        config,
        move |data: &mut [T], _: &cpal::OutputCallbackInfo| {
            write_data(data, channels, &mut next_value);
        },
        err_fn,
        None,
    );

    if let Ok(stream) = stream {
        if let Ok(()) = stream.play() {
            std::mem::forget(stream);
        }
    }

    println!("Output stream built.");
}

fn write_data<T>(output: &mut [T], channels: usize, next_sample: &mut dyn FnMut() -> (f32, f32))
where
    T: SizedSample + FromSample<f32>,
{
    for frame in output.chunks_mut(channels) {
        let sample = next_sample();
        let left = T::from_sample(sample.0);
        let right = T::from_sample(sample.1);

        for (channel, sample) in frame.iter_mut().enumerate() {
            if channel & 1 == 0 {
                *sample = left;
            } else {
                *sample = right;
            }
        }
    }
}
