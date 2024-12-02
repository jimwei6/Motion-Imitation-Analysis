# Motion-Imitation-Analysis
Repository for analyzing SOTA methods on physics based motion imitation.

# Requirements

View the requirements for submodules: CharacterAnimation Tools and MoConVQ

Other requirements:

```python
pip install bvh
pip install bvhio
```

# Dataset

Please download from the [AMASS](https://amass.is.tue.mpg.de/) webpage.

Datasets used: ACCAD, BMLmovi, BMLRub, CMU, DanceDB, Eye-
sJapanDataset, MPI HDM05, EKUT,
SFU, Mosh, PosePrior, and Transitions.

# Scripts

Converting amass dataset folder (SFU, CMU...etc) to bvh files
```python
python ./scripts/amass_to_bvh.py <dataset_dir> <output_dir> <smpl_model_File>
```

Recentering bvh
```python
python ./scripts/recenter_bvh.py <input_dir> <output_dir>
```

Converting amass bvh to moconvq bvh
```python
python ./scripts/amass_to_moconvq_bvh.py <input_dir> <output_dir> ./moconvq.bvh
```

Pipeline for converting amass bvh to moconvq bvh and recentering

```bash
bash ./scripts/convert_amass_bvh.sh <input_dir> <output_dir>
```

Pipeline for tracking a directory with moconvq (does it file by file).
For folder based, please look at the MoConVQ submodule.
```bash
bash ./scripts/tracking_directory.sh <input_dir> <custom experiment name> <output_dir>
```

Resampling BVH to specified framerate (linear)
```python
python ./scripts/resample_bvh.py <truth_dir> <output_dir> <target fps>
```

Evaluating results
```python
python ./scripts/evaluate.py <truth_dir> <pred_dir> <experiment runtime json file> <output_csv_file>
```

Pipeline for running the whole thing (assumes amass datasets are already converted to bvh in ./amass_ds using ./scripts/amass_to_bvh.py)
```bash
bash ./scripts/experiment.sh
```