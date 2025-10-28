
# Web-based Generative Poster 

This Streamlit app turns your generative posters into a **web app**.

## How to run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to deploy to Streamlit Cloud
1. Push this folder to a GitHub repo (e.g., `generative-poster-streamlit`).
2. On https://streamlit.io/cloud, click **New app** → connect your repo.
3. Set **Main file path** to `app.py`, keep default Python version.
4. Deploy. Done! Your web URL will look like `https://<your-app-name>.streamlit.app/`

## CSV Palette
- Use the built-in `palette.csv` (20 colors) or upload your own from the UI.
- CSV schema:
```
name,r,g,b
ocean,0.1,0.3,0.8
...
```
