# Philly COVID Stats
I've been following Philly's COVID stats for awhile, but don't know of a place that combines the [COVID Response Levels](https://www.phila.gov/2022-02-16-philadelphia-establishes-covid-response-levels-to-guide-mandate-enforcement/) with the public data.
To see what that looked like (and to learn streamlit/plotly), I decided to build that myself.

This repo contains a streamlit app that visualizes the Philly COVID statistic relevant to the response levels, and updates its data daily.

## Usage
To run this repo, install the dependencies with 
```bash 
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Alternatively, navigate to the cloud version at https://share.streamlit.io/ben-heil/philly-covid-stats/main.
