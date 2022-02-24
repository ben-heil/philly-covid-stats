import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


# Cache the result based on the current day to keep the Philly OpenData API from getting queried needlessly
@st.cache(persist=True, max_entries=3)
def load_cases_by_date(today: datetime.datetime) -> pd.DataFrame:
    """
    Load the cases_by_date csv data from the philly website and preprocess it

    Arguments
    ---------
    today: The current day's date, for use in cacheing

    Returns
    -------
    cases_by_date: A dataframe containing each day's positive and negative test values, along with
                   some stats calculated from them
    """
    cases_url = 'https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+covid_cases_by_date&filename=covid_cases_by_date&format=csv&skipfields=cartodb_id'
    cases_by_date = pd.read_csv(cases_url)
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
    cases_by_date['ten_days_prior'] = cases_by_date['positive_avg'].shift(10)
    cases_by_date['ten_day_difference'] = cases_by_date['positive_avg'] - cases_by_date['ten_days_prior']
    cases_by_date['ten_day_percent_change'] = 100 * cases_by_date['ten_day_difference'] /  cases_by_date['ten_days_prior']
    return cases_by_date


@st.cache(persist=True, max_entries=3)
def load_hosp_by_date(today: datetime.datetime) -> pd.DataFrame:
    """
    Load the hosp_by_date csv data from the philly website and preprocess it

    Arguments
    ---------
    today: The current day's date, for use in cacheing

    Returns
    -------
    hosp_by_date: A dataframe containing each day's hospitalizations for COVID
    """
    hosp_url = 'https://phl.carto.com/api/v2/sql?filename=covid_hospitalizations_by_date&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator&q=SELECT%20*%20FROM%20covid_hospitalizations_by_date'
    hosp_by_date = pd.read_csv(hosp_url)
    hosp_by_date = hosp_by_date.drop(['etl_timestamp'], axis=1)

    hosp_by_date = hosp_by_date.pivot(index='date', columns='hospitalized', values='count')
    # Remove NaN date
    hosp_by_date = hosp_by_date[hosp_by_date.index.notnull()]
    hosp_by_date.loc[hosp_by_date['Yes'].isnull(), 'Yes'] = 5
    hosp_by_date['report_date'] = hosp_by_date.index
    hosp_by_date['avg_hospitalizations'] = hosp_by_date.Yes.rolling(7).mean()
    return hosp_by_date


def load_text(file_path):
    """A convenience function for reading in the markdown files used for the site's text"""
    with open(file_path) as in_file:
        return in_file.read()

if __name__ == '__main__':
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    st.set_page_config(layout="wide")

    # Set up header
    header_text = load_text('header_text.md')
    st.write(header_text)

    cases_df = load_cases_by_date(today)
    hosp_by_date = load_hosp_by_date(today)

    col1, col2 = st.columns([1, 1])

    # Positive test plot
    labels = {'date_collected': 'Date Collected', 'positive_avg': 'Positive Test Count (Seven-Day Average)'}
    plot = px.line(cases_df, x='date_collected', y='positive_avg',
                labels=labels, title='Positive COVID Tests by Date Collected')
    plot.add_hrect(y0=0, y1=100, fillcolor='green', opacity=.2, layer='below')
    plot.add_hrect(y0=100, y1=225, fillcolor='yellow', opacity=.2, layer='below')
    plot.add_hrect(y0=225, y1=500, fillcolor='orange', opacity=.2, layer='below')
    plot.add_hrect(y0=500, y1=4250, fillcolor='red', opacity=.2, layer='below')
    plot.update_xaxes(type='date', range=[thirty_days_ago, today])
    thirty_day_max = cases_df.iloc[-30:,].positive.max()
    plot.update_yaxes(range=[0, thirty_day_max + 100])
    with col1:
        st.plotly_chart(plot, use_container_width=True)

    # Percent positive plot
    labels = {'date_collected': 'Date Collected',
            'percent_positive_avg': 'Percent of Tests Positive (Seven-Day Average)'}
    plot = px.line(cases_df, x='date_collected', y='percent_positive_avg',
                labels=labels, title='Percent Positivity')
    plot.add_hrect(y0=0, y1=2, fillcolor='green', opacity=.2, layer='below')
    plot.add_hrect(y0=2, y1=5, fillcolor='yellow', opacity=.2, layer='below')
    plot.add_hrect(y0=5, y1=10, fillcolor='orange', opacity=.2, layer='below')
    plot.add_hrect(y0=10, y1=50, fillcolor='red', opacity=.2, layer='below')
    plot.update_xaxes(type='date', range=[thirty_days_ago, today])
    thirty_day_max = cases_df.iloc[-30:,].percent_positive_avg.max()
    plot.update_yaxes(range=[0, thirty_day_max + 5])
    with col2:
        st.plotly_chart(plot, use_container_width=True)

    # Percent change plot
    labels = {'date_collected': 'Date Collected',
            'ten_day_percent_change': 'Percent Change'}
    plot = px.line(cases_df[cases_df['date_collected'] > '2020-04-15'],
                x='date_collected', y='ten_day_percent_change',
                labels=labels, title='Case Percent Change from Ten Days Prior',
                )
    plot.add_hrect(y0=-70, y1=50, fillcolor='green', opacity=.2, layer='below')
    plot.add_hrect(y0=50, y1=300, fillcolor='red', opacity=.2, layer='below')
    plot.update_xaxes(type='date', range=[thirty_days_ago, today])
    thirty_day_max = cases_df.iloc[-30:,].ten_day_percent_change.max()
    with col1:
        st.plotly_chart(plot, use_container_width=True)

    # Hospitalizations plot
    labels = {'report_date': 'Report Date',
            'avg_hospitalizations': 'Hospitalizations for COVID (Seven-Day Average)'}
    plot = px.line(hosp_by_date, x='report_date', y='avg_hospitalizations',
                labels=labels, title='COVID Hospitalizations')
    plot.add_hrect(y0=0, y1=50, fillcolor='green', opacity=.2, layer='below')
    plot.add_hrect(y0=50, y1=100, fillcolor='yellow', opacity=.2, layer='below')
    plot.add_hrect(y0=100, y1=200, fillcolor='orange', opacity=.2, layer='below')
    #plot.add_hrect(y0=500, y1=600, fillcolor='red', opacity=.2, layer='below')
    plot.update_xaxes(type='date', range=[thirty_days_ago, today])
    thirty_day_max = hosp_by_date.iloc[-30:,].avg_hospitalizations.max()
    plot.update_yaxes(range=[0, thirty_day_max + 5])
    with col2:
        st.plotly_chart(plot, use_container_width=True)

    # Set up post-data text
    footer_text = load_text('footer_text.md')
    st.write(footer_text)
