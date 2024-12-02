import os
import numpy as np
from scipy.interpolate import interp1d

class BVH:
    def __init__(self, filepath):
        self.filepath = filepath
        self.header = []
        self.motion_data = None
        self.frame_time = None
        self.num_frames = None
        self.load_bvh()

    def load_bvh(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        motion_start_idx = None
        for i, line in enumerate(lines):
            self.header.append(line)
            if "Frame Time:" in line:
                self.frame_time = float(line.split(":")[1].strip())
            if "Frames:" in line:
                self.num_frames = int(line.split(":")[1].strip())
            if "MOTION" in line:
                motion_start_idx = i + 3
                break

        if motion_start_idx is not None:
            motion_lines = lines[motion_start_idx:]
            self.motion_data = np.array(
                [list(map(float, line.strip().split())) for line in motion_lines]
            )

    def save_bvh(self, filepath, motion_data, frame_time):
        with open(filepath, 'w') as f:
            for line in self.header:
                if "Frames:" in line:
                    f.write(f"Frames: {motion_data.shape[0]}\n")
                elif "Frame Time:" in line:
                    f.write(f"Frame Time: {frame_time:.6f}\n")
                else:
                    f.write(line)
            for frame in motion_data:
                f.write(" ".join(map(str, frame)) + "\n")

def resample_motion(data, original_frame_time, target_frame_time):
    original_times = np.arange(data.shape[0]) * original_frame_time
    target_times = np.arange(0, original_times[-1], target_frame_time)
    resampled_data = np.zeros((len(target_times), data.shape[1]))
    for i in range(data.shape[1]):
        interpolator = interp1d(original_times, data[:, i], kind='linear')
        resampled_data[:, i] = interpolator(target_times)
    return resampled_data

def resample_bvh(input_file, output_file, target_fps):
    bvh = BVH(input_file)
    target_frame_time = 1.0 / target_fps

    resampled_data = resample_motion(bvh.motion_data, bvh.frame_time, target_frame_time)
    bvh.save_bvh(output_file, resampled_data, target_frame_time)

def process_directory(input_dir, output_dir, target_fps):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".bvh"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            print(f"Processing: {input_path} -> {output_path}")
            resample_bvh(input_path, output_path, target_fps)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resample all BVH files in a directory to a specified FPS.")
    parser.add_argument("input_dir", type=str, help="Path to the input directory containing BVH files.")
    parser.add_argument("output_dir", type=str, help="Path to the output directory for resampled BVH files.")
    parser.add_argument("target_fps", type=float, help="Target frames per second.")

    args = parser.parse_args()
    process_directory(args.input_dir, args.output_dir, args.target_fps)
