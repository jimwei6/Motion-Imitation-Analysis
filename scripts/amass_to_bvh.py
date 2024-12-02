import argparse
import os
from ./CharacterAnimationTools/anim import amass
from ./CharacterAnimationTools/anim import bvh

def process_directory(amass_dir, smplh_path, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each subdirectory in the AMASS directory
    for object_name in os.listdir(amass_dir):
        object_path = os.path.join(amass_dir, object_name)

        # Ensure it's a directory
        if os.path.isdir(object_path):
            # Iterate through all .npz files in the current object directory
            for file_name in os.listdir(object_path):
                if file_name.endswith('.npz'):
                    # Construct the full file path
                    amass_motion_path = os.path.join(object_path, file_name)
                    try:
                        # Load the animation data from the .npz file
                        anim = amass.load(
                            amass_motion_path=amass_motion_path,
                            smplh_path=smplh_path
                        )
                    except Exception as e:
                        print(e)
                        continue

                    # Define the output path for the corresponding BVH file
                    output_path = os.path.join(output_dir, f"{object_name}_{file_name.replace('.npz', '.bvh')}")

                    # Save the animation as a BVH file
                    bvh.save(
                        filepath=output_path,
                        anim=anim
                    )

                    print(f"Processed {amass_motion_path} -> {output_path}")

def main(amass_dir, smplh_path, output_dir):
    process_directory(amass_dir, smplh_path, output_dir)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert AMASS motion data in directories to BVH format.")
    parser.add_argument('amass_dir', type=str, help="Path to the AMASS directory containing subdirectories with .npz files.")
    parser.add_argument('output_dir', type=str, help="Directory to save the resulting BVH files.")
    parser.add_argument('smpl_model', type=str, help="DIrectory to smpl model .npz file")
    # Parse the arguments
    args = parser.parse_args()

    # Run the main function with the provided arguments
    main(args.amass_dir, args.smpl_model, args.output_dir)