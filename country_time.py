import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import numpy as np

st.title("국가별 현재 시간")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def get_time_in_timezone(timezone):
    tz = ZoneInfo(timezone)
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def get_current_times():
    timezones = {
        "한국": "Asia/Seoul",
        "미국(뉴욕)": "America/New_York",
        "일본": "Asia/Tokyo",
        "중국(베이징)": "Asia/Shanghai"
    }
    
    data = {
        '국가': [],
        '시간': []
    }
    
    for region, tz in timezones.items():
        current_time = get_time_in_timezone(tz)
        data['국가'].append(region)
        data['시간'].append(current_time)

    return pd.DataFrame(data)


placeholder = st.empty()

while True:
    current_times_df = get_current_times()
    placeholder.write(current_times_df)
    time.sleep(1)

st.title('Uber pickups in NYC')

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
