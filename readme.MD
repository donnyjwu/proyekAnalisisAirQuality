Setup environment

conda create --name proyekAnalisisAirQuality python=3.9
conda activate proyekAnalisisAirQuality
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel

Run steamlit app
streamlit run dashboard/dashboard.py
