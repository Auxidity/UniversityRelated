use std::{
    collections::VecDeque,
    ffi::c_void,
    sync::{
        Arc, Mutex,
        atomic::{AtomicBool, Ordering},
    },
};

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};

const BLOCK_SIZE: usize = 512;
const WARMUP_THRESHOLD: usize = BLOCK_SIZE * 4;

unsafe extern "C" {
    fn rb_create(sample_rate: i32, channels: i32, pitch_ratio: f32) -> *mut std::ffi::c_void;
    fn rb_destroy(handle: *mut std::ffi::c_void);
    fn rb_process(
        handle: *mut std::ffi::c_void,
        input: *const *const f32,
        input_frames: i32,
        output: *mut *mut f32,
        max_output_Frames: i32,
    ) -> i32;
}

fn pitch_shift_with_rubberband(
    left: &[f32],
    right: &[f32],
    handle: *mut std::ffi::c_void,
) -> (Vec<f32>, Vec<f32>) {
    let input_frames = left.len() as i32;
    assert_eq!(right.len(), left.len());
    let input_ptrs = [left.as_ptr(), right.as_ptr()];

    let mut left_out = vec![0.0f32; input_frames as usize * 2];
    let mut right_out = vec![0.0f32; input_frames as usize * 2];

    let mut output_ptrs = [left_out.as_mut_ptr(), right_out.as_mut_ptr()];

    let frames_retrieved = unsafe {
        rb_process(
            handle,
            input_ptrs.as_ptr(),
            input_frames,
            output_ptrs.as_mut_ptr(),
            input_frames,
        )
    };

    if frames_retrieved < 0 {
        panic!("Rubberband processing error");
    }

    left_out.truncate(frames_retrieved as usize);
    right_out.truncate(frames_retrieved as usize);

    (left_out, right_out)
}

struct RubberBandHandle(*mut c_void);
unsafe impl Send for RubberBandHandle {}
unsafe impl Sync for RubberBandHandle {}

fn main() {
    let running = Arc::new(AtomicBool::new(true));
    let running_clone = running.clone();

    ctrlc::set_handler(move || {
        running_clone.store(false, Ordering::SeqCst);
        println!("Cleaning up.");
    })
    .expect("Error setting up handler..");

    let input_buffer = Arc::new(Mutex::new(VecDeque::<f32>::with_capacity(10 * BLOCK_SIZE)));
    let output_buffer = Arc::new(Mutex::new(VecDeque::<f32>::with_capacity(10 * BLOCK_SIZE)));

    let input_buffer_thread = Arc::clone(&input_buffer);
    let output_buffer_thread = Arc::clone(&output_buffer);

    let host = cpal::default_host();
    let in_device = host.default_input_device().unwrap();
    let in_config_supported = in_device.default_input_config().unwrap();
    let in_config: cpal::StreamConfig = in_config_supported.clone().into();

    let sample_rate = in_config.sample_rate.0 as i32;
    let channels = 2;
    let pitch_ratio = 0.7;
    let rb_handle_raw = unsafe { rb_create(sample_rate, channels, pitch_ratio) };
    assert!(!rb_handle_raw.is_null());
    let rb_handle = Arc::new(Mutex::new(RubberBandHandle(rb_handle_raw)));
    let rb_handle_thread = Arc::clone(&rb_handle);

    let err_fn = |err| eprintln!("an error occurred on stream: {}", err);

    let in_stream = in_device.build_input_stream(
        &in_config,
        move |data: &[f32], _: &cpal::InputCallbackInfo| {
            let mut input = input_buffer.lock().unwrap();
            for frame in data.chunks(2) {
                input.push_back(frame[0]);
                input.push_back(frame[1]);
            }
        },
        err_fn,
        None,
    );

    if let Ok(stream) = in_stream {
        if let Ok(()) = stream.play() {
            std::mem::forget(stream);
        }
    }

    let running_thread = Arc::clone(&running);

    let processing = std::thread::spawn(move || {
        while running_thread.load(Ordering::SeqCst) {
            let mut input = input_buffer_thread.lock().unwrap();
            if input.len() >= 2 * BLOCK_SIZE {
                let mut block = vec![0.0f32; 2 * BLOCK_SIZE];
                for i in 0..(2 * BLOCK_SIZE) {
                    block[i] = input.pop_front().unwrap();
                }
                drop(input);

                let (l, r): (Vec<f32>, Vec<f32>) = block.chunks(2).map(|s| (s[0], s[1])).unzip();

                let handle = rb_handle_thread.lock().unwrap();
                let (l_out, r_out) = pitch_shift_with_rubberband(&l, &r, handle.0);
                drop(handle);

                let mut output = output_buffer_thread.lock().unwrap();
                for (&l, &r) in l_out.iter().zip(r_out.iter()) {
                    output.push_back(l);
                    output.push_back(r);
                }
            } else {
                drop(input);
                std::thread::sleep(std::time::Duration::from_millis(1));
            }
        }
    });

    let output_buffer = Arc::clone(&output_buffer);
    let out_device = host.default_output_device().unwrap();
    let out_config_supported = out_device.default_output_config().unwrap();
    let out_config: cpal::StreamConfig = out_config_supported.clone().into();

    println!("Output buffer fillup");
    loop {
        let output_len = output_buffer.lock().unwrap().len();
        if output_len >= WARMUP_THRESHOLD * 2 {
            break;
        };
        std::thread::sleep(std::time::Duration::from_millis(10));
    }
    println!("Starting output stream");

    let out_stream = out_device.build_output_stream(
        &out_config,
        move |data: &mut [f32], _: &cpal::OutputCallbackInfo| {
            let mut output = output_buffer.lock().unwrap();
            for frame in data.chunks_mut(2) {
                if output.len() >= 2 {
                    frame[0] = output.pop_front().unwrap_or(0.0);
                    frame[1] = output.pop_front().unwrap_or(0.0);
                } else {
                    frame[0] = 0.0;
                    frame[1] = 0.0;
                }
            }
        },
        err_fn,
        None,
    );

    if let Ok(stream) = out_stream {
        if let Ok(()) = stream.play() {
            std::mem::forget(stream);
        }
    }

    while running.load(Ordering::SeqCst) {
        std::thread::sleep(std::time::Duration::from_millis(100));
    }

    processing.join().unwrap();
    let handle = rb_handle.lock().unwrap();
    unsafe {
        rb_destroy(handle.0);
    }
}
