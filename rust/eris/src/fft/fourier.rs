use std::f32::consts::PI;
//use std::cmp::max;


#[derive(Debug, Clone, Copy)]
pub struct Complex {
    pub re : f32,
    pub im : f32,
}

impl Complex {
    fn new(re: f32, im: f32) -> Self {
        Complex { re, im }
    }
}

fn fft(input: &mut [Complex], invert: bool) {
    let n = input.len();
    let mut step = 1;

    //Bit reversal permutation
    let mut i= 1;
    while i < n {
        let mut j = 0;
        let mut k = i;
        //let mut nstep = step * 2;

        while k > step {
            k -= step;
            j += step;
        }
        if j > i {
            input.swap(i, j);
        }
        i += step;
    }
    step *= 2;

    //FFT. Cooley-Tukey algorithm
    
    while step <= n {
        let ang = if invert {
            -PI / (step as f32 / 2.0)        
        } else {
            PI / (step as f32 / 2.0)
        };

        let wlen = Complex::new(ang.cos(), ang.sin());
        for k in (0..n).step_by(step) {
            let mut w = Complex::new(1.0, 1.0);
            for j in 0..step / 2 {
                let t = Complex::new(
                    w.re * input[k + j + step / 2].re - w.im * input[k + j + step / 2].im,
                    w.re * input[k + j + step / 2].im + w.im * input[k + j + step / 2].re,
                );
                let u = input[k + j];
                input[k+j] = Complex::new(u.re + t.re, u.im + t.im);
                input[k + j + step / 2] = Complex::new(u.re - t.re, u.im - t.im);

                //Update w
                w = Complex::new(
                    w.re * wlen.re - w.im * wlen.im,
                    w.re * wlen.im + w.im * wlen.re,
                );
            }
        }

        step *= 2;
    }

    if invert {
        for x in input.iter_mut() {
            x.re /= n as f32;
            x.im /= n as f32;
        }
    }
}

fn ifft(input: &mut [Complex]) {
    fft(input, true)
}

pub fn process_audio_in_frequency_domain(audio_samples: &[f32]) -> Vec<Complex> {
    let mut complex_data: Vec<Complex> = audio_samples.iter().map(|&s| Complex::new(s, 0.0)).collect();
    fft(&mut complex_data, false);
    complex_data
}

//Might have to return something other than Vec<f32> ? Worry about it later
pub fn process_audio_data_to_time_domain(freq_data: &mut [Complex]) -> Vec<f32> {
    ifft(freq_data);
    freq_data.iter().map(|c| c.re).collect()
}
