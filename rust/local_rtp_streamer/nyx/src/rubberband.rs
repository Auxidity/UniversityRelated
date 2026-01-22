use std::os::raw::{c_float, c_int};

#[repr(C)]
pub struct RubberBandHandle;
#[link(name = "rubberband_wrapper")]
extern "C" {
    pub fn rb_create(
        sample_rate: c_int,
        channels: c_int,
        pitch_ratio: c_float,
    ) -> *mut RubberBandHandle;

    pub fn rb_destroy(handle: *mut RubberBandHandle);

    pub fn rb_process(
        handle: *mut RubberBandHandle,
        input: *const *const c_float,
        input_frames: c_int,
        output: *mut *mut c_float,
        max_output_frames: c_int,
    ) -> c_int;
}
