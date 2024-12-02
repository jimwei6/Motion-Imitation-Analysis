bash "./convert_amass_bvh.sh" "../amass_ds/accad/" "./amass_ds/accad"
bash "./convert_amass_bvh.sh" "../amass_ds/BMLmovi/" "./amass_ds/BMLmovi"
bash "./convert_amass_bvh.sh" "../amass_ds/BMLrub/" "./amass_ds/BMLrub"
bash "./convert_amass_bvh.sh" "../amass_ds/CMU/" "./amass_ds/CMU"
bash "./convert_amass_bvh.sh" "../amass_ds/EKUT/" "./amass_ds/EKUT"
bash "./convert_amass_bvh.sh" "../amass_ds/Eyes/" "./amass_ds/Eyes"
bash "./convert_amass_bvh.sh" "../amass_ds/KIT/" "./amass_ds/KIT"
bash "./convert_amass_bvh.sh" "../amass_ds/MPI_HDM05/" "./amass_ds/MPI_HDM05"
bash "./convert_amass_bvh.sh" "../amass_ds/MPI_Limits/" "./amass_ds/MPI_Limits"
bash "./convert_amass_bvh.sh" "../amass_ds/MPI_mosh/" "./amass_ds/MPI_mosh"
bash "./convert_amass_bvh.sh" "../amass_ds/SFU/" "./amass_ds/SFU"
bash "./convert_amass_bvh.sh" "../amass_ds/TotalCapture/" "./amass_ds/TotalCapture"
bash "./convert_amass_bvh.sh" "../amass_ds/Transitions/" "./amass_ds/Transitions"
bash "./convert_amass_bvh.sh" "../amass_ds/DanceDB/" "./amass_ds/DanceDB"

bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/accad/' 'accad' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/BMLmovi/' 'BMLmovi' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/BMLrub/' 'BMLrub' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/CMU/' 'CMU' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/EKUT/' 'EKUT' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/Eyes/' 'Eyes' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/KIT/' 'KIT' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/MPI_HDM05/' 'MPI_HDM05' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/MPI_Limits/' 'MPI_Limits' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/MPI_mosh/' 'MPI_mosh' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/SFU/' 'SFU' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/TotalCapture/' 'TotalCapture' './experiments'
bash './MoConVQ/Script/tracking_directory.sh' './amass_ds/Transitions/' 'Transitions' './experiments'
bash './MoConVQ/Script/.sh' './amass_ds/DanceDB/' 'DanceDB' './experiments'

python './Script/recenter_bvh.py' './experiments/accad'
python './Script/recenter_bvh.py' './experiments/BMLmovi'
python './Script/recenter_bvh.py' './experiments/BMLrub'
python './Script/recenter_bvh.py' './experiments/CMU'
python './Script/recenter_bvh.py' './experiments/EKUT'
python './Script/recenter_bvh.py' './experiments/Eyes'
python './Script/recenter_bvh.py' './experiments/KIT'
python './Script/recenter_bvh.py' './experiments/MPI_HDM05'
python './Script/recenter_bvh.py' './experiments/MPI_Limits'
python './Script/recenter_bvh.py' './experiments/MPI_mosh'
python './Script/recenter_bvh.py' './experiments/SFU'
python './Script/recenter_bvh.py' './experiments/TotalCapture'
python './Script/recenter_bvh.py' './experiments/Transitions'
python './Script/recenter_bvh.py' './experiments/DanceDB'

python './Script/evaluate.py' './amass_ds/accad' './experiments/accad' './accad.json' './accad.csv'
python './Script/evaluate.py' './amass_ds/DanceDB' './experiments/DanceDB' './DanceDB.json' './DanceDB.csv'
python './Script/evaluate.py' './amass_ds/BMLmovi' './experiments/BMLmovi' './BMLmovi.json' './BMLmovi.csv'
python './Script/evaluate.py' './amass_ds/Eyes' './experiments/Eyes' './Eyes.json' './Eyes.csv'
python './Script/evaluate.py' './amass_ds/BMLrub' './experiments/BMLrub' './BMLrub.json' './BMLrub.csv'
python './Script/evaluate.py' './amass_ds/CMU' './experiments/CMU' './CMU.json' './CMU.csv'
python './Script/evaluate.py' './amass_ds/EKUT' './experiments/EKUT' './EKUT.json' './EKUT.csv'
python './Script/evaluate.py' './amass_ds/KIT' './experiments/KIT' './KIT.json' './KIT.csv'
python './Script/evaluate.py' './amass_ds/MPI_HDM05' './experiments/MPI_HDM05' './MPI_HDM05.json' './MPI_HDM05.csv'
python './Script/evaluate.py' './amass_ds/MPI_Limits' './experiments/MPI_Limits' './MPI_Limits.json' './MPI_Limits.csv'
python './Script/evaluate.py' './amass_ds/MPI_mosh' './experiments/MPI_mosh' './MPI_mosh.json' './MPI_mosh.csv'
python './Script/evaluate.py' './amass_ds/SFU' './experiments/SFU' './SFU.json' './SFU.csv'
python './Script/evaluate.py' './amass_ds/TotalCapture' './experiments/TotalCapture' './TotalCapture.json' './TotalCapture.csv'
python './Script/evaluate.py' './amass_ds/Transitions' './experiments/Transitions' './Transitions.json' './Transitions.csv'
