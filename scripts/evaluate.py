import bvhio
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import argparse
import json
from scipy.spatial.transform import Rotation as R
from bvh import Bvh

JOINT_NAMES = None
TRUTH_ORDER = 'ZYX'
TEST_ORDER = 'XYZ'
# pos of joints with regards to root
# root is relative to its initial position
def get_relative_pos_of_joints(bvh, frame, min_frame, root_quat_rot, printR=False):
    root_pos_at_frame = bvh.loadPose(frame).layout()[0][0].PositionWorld
    root_pos_at_init = bvh.loadPose(min_frame).layout()[0][0].PositionWorld
    
    joint_dict = {}
    joint_dict['RootJoint'] = root_quat_rot.inv().apply(root_pos_at_frame - root_pos_at_init)
    
    # relative position to root
    for joint, _, _ in bvh.loadPose(frame).layout()[1:]:
        joint_dict[joint.Name] = root_quat_rot.inv().apply(joint.PositionWorld - root_pos_at_frame)
    
    return [joint_dict[name] for name in JOINT_NAMES]

# rotation of joints with regard to initial rotation
def get_relative_rot_of_joints(bvh, frame, min_frame, order='XYZ'):
    init_layout = np.array([R.from_euler(order,
                           [bvh.frame_joint_channel(min_frame, name, '{}rotation'.format(order[0])),
                            bvh.frame_joint_channel(min_frame, name, '{}rotation'.format(order[1])),
                            bvh.frame_joint_channel(min_frame, name, '{}rotation'.format(order[2]))], degrees=True).as_euler('XYZ')
                           for name in JOINT_NAMES])
    frame_layout = np.array([R.from_euler(order,
                           [bvh.frame_joint_channel(frame, name, '{}rotation'.format(order[0])),
                            bvh.frame_joint_channel(frame, name, '{}rotation'.format(order[1])),
                            bvh.frame_joint_channel(frame, name, '{}rotation'.format(order[2]))], degrees=True).as_euler('XYZ')
                           for name in JOINT_NAMES])

    return frame_layout - init_layout

def get_rot_of_root(bvh, frame, order='XYZ'):
    return R.from_euler(order,
                  [bvh.frame_joint_channel(frame, 'RootJoint', '{}rotation'.format(order[0])),
                    bvh.frame_joint_channel(frame, 'RootJoint', '{}rotation'.format(order[1])),
                    bvh.frame_joint_channel(frame, 'RootJoint', '{}rotation'.format(order[2]))], degrees=True)

def pos_imitation_successful(truth_pos, test_pos, min_frame, max_frame):   
    if min_frame == max_frame - 1:
        return False

    POS_DIFF = 0.08 # in meters
    pos_diff = np.absolute(truth_pos - test_pos)
    if np.any(pos_diff > POS_DIFF):
        return False
    return True

def rot_imitation_successful(truth_rot, test_rot, min_frame, max_frame):
    if min_frame == max_frame - 1:
        return False

    ROT_DIFF = 3 # degrees
    rot_diff = np.absolute(truth_rot - test_rot)
    if np.any(rot_diff > ROT_DIFF):
        return False
    return True

def mpjpe(truth_pos, test_pos):
    mean = np.mean(np.linalg.norm(truth_pos - test_pos, axis=-1), axis=0)
    res = {}
    for i, name in enumerate(JOINT_NAMES):
        res[name + '_MPE'] = mean[i]
    return res

def mpjre(truth_rot, test_rot):
    mean = np.mean(np.linalg.norm(truth_rot - test_rot, axis=-1), axis=0)
    res = {}
    for i, name in enumerate(JOINT_NAMES):
        res[name + '_MRE'] = mean[i]
    return res

def mpjpe_change(truth_pos, test_pos):
    truth_arr = np.diff(truth_pos, axis=0)
    test_arr = np.diff(test_pos, axis=0)
    mean = np.mean(np.linalg.norm(truth_arr - test_arr, axis=-1), axis=0)
    res = {}
    for i, name in enumerate(JOINT_NAMES):
        res[name + '_MPE_change'] = mean[i]
    return res


def mpjre_change(truth_rot, test_rot):
    mean = np.mean(np.linalg.norm(truth_rot - test_rot, axis=-1), axis=0)
    res = {}
    for i, name in enumerate(JOINT_NAMES):
        res[name + '_MRE_change'] = mean[i]
    return res

def frame_to_start(truth_bvh_pos, test_bvh_pos, truth_bvh_rot, test_bvh_rot, max_frame):
    POS_DIFF = 0.08
    ROT_DIFF = 3
    for i in range(max_frame):
        truth_pos = np.array(get_relative_pos_of_joints(truth_bvh_pos, i, 0, get_rot_of_root(truth_bvh_rot, i, TRUTH_ORDER)))
        test_pos = np.array(get_relative_pos_of_joints(test_bvh_pos, i, 0, get_rot_of_root(test_bvh_rot, i, TEST_ORDER)))
        truth_rot = np.array(get_relative_rot_of_joints(truth_bvh_rot, i, 0, TRUTH_ORDER))
        test_rot = np.array(get_relative_rot_of_joints(test_bvh_rot, i, 0, TEST_ORDER))
        
        if (not np.any(np.absolute(truth_pos - test_pos) > POS_DIFF)) and (not np.any(np.absolute(truth_rot - test_rot) > ROT_DIFF)):
            return i
    return 40 if 40 < max_frame else 0

def evaluate_directories(truth_dir, test_dir, time_file, output_csv):
    global JOINT_NAMES
    results = []
    
    truth_files = sorted(os.listdir(truth_dir))
    test_files = sorted(os.listdir(test_dir))
    # Ensure the files in both directories match
    # assert truth_files == test_files, "Filenames in both directories do not match!"

    time_data = None
    with open(time_file, 'r') as openfile:
        # Reading from json file
        time_data = json.load(openfile)

    i = 0
    for file_name in tqdm(truth_files, desc="Evaluating"):
        print(file_name)
        truth_bvh_rot = None 
        test_bvh_rot = None 
        truth_path = os.path.join(truth_dir, file_name)
        test_path = os.path.join(test_dir, file_name)
        try:
            with open(truth_path) as f:
                truth_bvh_rot = Bvh(f.read())
            with open(test_path) as f:
                test_bvh_rot = Bvh(f.read())
        except Exception as e:
            print(e)
            continue
        
        truth_bvh_pos = bvhio.readAsHierarchy(truth_path)
        test_bvh_pos = bvhio.readAsHierarchy(test_path)
        if JOINT_NAMES is None:
            JOINT_NAMES = [joint.Name for joint, _, _ in truth_bvh_pos.layout()]

        MAX_FRAME = min(truth_bvh_rot.nframes, test_bvh_rot.nframes)        
        starting_frame = frame_to_start(truth_bvh_pos, test_bvh_pos, truth_bvh_rot, test_bvh_rot, MAX_FRAME)
        MIN_FRAME = starting_frame
    
        truth_pos = np.array([get_relative_pos_of_joints(truth_bvh_pos, i, MIN_FRAME, get_rot_of_root(truth_bvh_rot, i, TRUTH_ORDER))
                for i in range(MIN_FRAME, MAX_FRAME)])
        test_pos = np.array([get_relative_pos_of_joints(test_bvh_pos, i, MIN_FRAME, get_rot_of_root(test_bvh_rot, i, TEST_ORDER))
                for i in range(MIN_FRAME, MAX_FRAME)])
        truth_rot = np.array([get_relative_rot_of_joints(truth_bvh_rot, i, MIN_FRAME, TRUTH_ORDER)  for i in range(MIN_FRAME, MAX_FRAME)])
        test_rot = np.array([get_relative_rot_of_joints(test_bvh_rot, i, MIN_FRAME, TEST_ORDER)  for i in range(MIN_FRAME, MAX_FRAME)])

        success = pos_imitation_successful(truth_pos, test_pos, MIN_FRAME, MAX_FRAME) and rot_imitation_successful(truth_rot, test_rot, MIN_FRAME, MAX_FRAME)
        mean_position_error = mpjpe(truth_pos, test_pos)
        mean_rotation_error = mpjre(truth_rot, test_rot)
        mean_position_change_error = mpjpe_change(truth_pos, test_pos)
        mean_rotation_change_error = mpjre_change(truth_rot, test_rot)
        
        # Store the results
        results.append({
          'file_name': file_name,
          'time_taken': time_data[file_name],
          'clip_time_origin': truth_bvh_rot.nframes * truth_bvh_rot.frame_time,
          'num_frames_origin': truth_bvh_rot.nframes,
          'frame_time_imit': truth_bvh_rot.frame_time,
          'clip_time_imit': test_bvh_rot.nframes * test_bvh_rot.frame_time,
          'num_frames_imit': test_bvh_rot.nframes,
          'frame_time_imit': test_bvh_rot.frame_time,
          'success': success,
          'frame_imit_starts': starting_frame,
          **mean_position_error,
          **mean_rotation_error,
          **mean_position_change_error,
          **mean_rotation_change_error})

    # Create a DataFrame and save as CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate BVH files using MPJPE.")
    parser.add_argument("truth_dir", type=str, help="Directory containing ground truth BVH files.")
    parser.add_argument("test_dir", type=str, help="Directory containing test BVH files.")
    parser.add_argument("time_file", type=str, help="Path for the time taken json file.")
    parser.add_argument("output_csv", type=str, help="Path to save the evaluation results CSV.")

    args = parser.parse_args()

    evaluate_directories(args.truth_dir, args.test_dir, args.time_file, args.output_csv)