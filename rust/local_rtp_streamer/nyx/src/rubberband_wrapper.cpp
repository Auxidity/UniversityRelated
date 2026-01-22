#include "RubberBandStretcher.h"
#include <cstddef>
#include <cstdint>
#include <vector>

extern "C" {

using RubberBandHandle = void*;

RubberBandHandle rb_create(int sample_rate, int channels, float pitch_ratio) {
    return static_cast<RubberBandHandle>(
        new RubberBand::RubberBandStretcher(
            sample_rate,
            channels,
            RubberBand::RubberBandStretcher::OptionProcessRealTime |
            RubberBand::RubberBandStretcher::OptionPitchHighQuality,
            1.0f, pitch_ratio
        )
    );
}

void rb_destroy(RubberBandHandle handle) {
    delete static_cast<RubberBand::RubberBandStretcher*>(handle);
}

int rb_process(
    RubberBandHandle handle,
    const float** input,
    int input_frames,
    float** output,
    int max_output_frames
) {
    auto* shifter = static_cast<RubberBand::RubberBandStretcher*>(handle);
    shifter->process(input, input_frames, false);
    return shifter->retrieve(output, max_output_frames);
}
}
