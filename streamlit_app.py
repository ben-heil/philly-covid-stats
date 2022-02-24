from cProfile import label
import streamlit as st
import pandas as pd
import plotly.express as px

def load_cases_by_date():
    # TODO load from web and use st.cache
    cases_by_date = pd.read_csv('cases_by_date.csv')
    cases_by_date = cases_by_date.drop(['the_geom', 'the_geom_webmercator', 'etl_timestamp'], axis=1)
    cases_by_date = cases_by_date.pivot(index='collection_date', columns='test_result', values='count')
    # Remove NaN date
    cases_by_date = cases_by_date[cases_by_date.index.notnull()]
    # If positive results aren't given, assume the largest possible unlisted value (5)
    # For more info, see https://www.opendataphilly.org/dataset/covid-cases
    cases_by_date.loc[cases_by_date['positive'].isnull(), 'positive'] = 5
    cases_by_date['percent_positive'] = 100 *  cases_by_date['positive'] / (cases_by_date['positive'] + cases_by_date['negative'])
    cases_by_date['positive_avg'] = cases_by_date.positive.rolling(7).mean()
    cases_by_date['percent_positive_avg'] = cases_by_date.percent_positive.rolling(7).mean()
    cases_by_date['date_collected'] = cases_by_date.index
    cases_by_date['date_collected'] = cases_by_date['date_collected'].astype('datetime64')
    return cases_by_date

def load_hosp_by_date():
    hosp_by_date = pd.read_csv('hospitalizations_by_date.csv')
    hosp_by_date = hosp_by_date.drop(['etl_timestamp'], axis=1)

    hosp_by_date = hosp_by_date.pivot(index='date', columns='hospitalized', values='count')
    # Remove NaN date
    hosp_by_date = hosp_by_date[hosp_by_date.index.notnull()]
    hosp_by_date.loc[hosp_by_date['Yes'].isnull(), 'Yes'] = 5
    hosp_by_date['report_date'] = hosp_by_date.index
    hosp_by_date['avg_hospitalizations'] = hosp_by_date.Yes.rolling(7).mean()
    return hosp_by_date

# Notes:
# Values can't fall below 5
# Values are a 7-day rolling window; it's unclear what the city uses
# Hospitalizations are based on confirmed cases, it's unclear whether the city
# uses suspected cases for their metric


cases_df = load_cases_by_date()
plot = px.line(cases_df, x='date_collected', y='positive_avg', title='Positive COVID Tests by Date Collected')

plot.add_hrect(y0=0, y1=100, fillcolor='green', opacity=.2, layer='below')
plot.add_hrect(y0=100, y1=225, fillcolor='yellow', opacity=.2, layer='below')
plot.add_hrect(y0=225, y1=500, fillcolor='orange', opacity=.2, layer='below')
plot.add_hrect(y0=500, y1=4250, fillcolor='red', opacity=.2, layer='below')

st.plotly_chart(plot)

plot = px.line(cases_df, x='date_collected', y='percent_positive_avg', title='Percent Positivity')
plot.add_hrect(y0=0, y1=2, fillcolor='green', opacity=.2, layer='below')
plot.add_hrect(y0=2, y1=5, fillcolor='yellow', opacity=.2, layer='below')
plot.add_hrect(y0=5, y1=10, fillcolor='orange', opacity=.2, layer='below')
plot.add_hrect(y0=10, y1=50, fillcolor='red', opacity=.2, layer='below')

st.plotly_chart(plot)

hosp_by_date = load_hosp_by_date()
plot = px.line(hosp_by_date, x='report_date', y='avg_hospitalizations', title='COVID Hospitalizations')
plot.add_hrect(y0=0, y1=50, fillcolor='green', opacity=.2, layer='below')
plot.add_hrect(y0=50, y1=100, fillcolor='yellow', opacity=.2, layer='below')
plot.add_hrect(y0=100, y1=200, fillcolor='orange', opacity=.2, layer='below')
#plot.add_hrect(y0=500, y1=600, fillcolor='red', opacity=.2, layer='below')

st.plotly_chart(plot)