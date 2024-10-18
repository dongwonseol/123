import streamlit as st
import pandas as pd
import datetime
import requests

# Define marathon data
marathons = [
    {"id": 1, "date": "2024-04-16", "name": "서울국제마라톤", "location": "서울", "distance": 42.195},
    {"id": 2, "date": "2024-05-21", "name": "경주국제마라톤", "location": "경주", "distance": 42.195},
    {"id": 3, "date": "2024-09-10", "name": "인천국제마라톤", "location": "인천", "distance": 42.195},
    {"id": 4, "date": "2024-10-15", "name": "춘천마라톤", "location": "춘천", "distance": 42.195},
    {"id": 5, "date": "2024-11-05", "name": "제주국제마라톤", "location": "제주", "distance": 21.0975},
    {"id": 6, "date": "2024-11-19", "name": "광주마라톤", "location": "광주", "distance": 10}
]

# Cache weather to avoid multiple API requests
weather_cache = {}

# Function to get weather
def get_weather(location):
    if location in weather_cache:
        return weather_cache[location]
    
    # Replace 'YOUR_API_KEY' with an actual API key for OpenWeatherMap
    api_key = "YOUR_API_KEY"
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location},KR&appid={api_key}&units=metric")
        data = response.json()
        weather_cache[location] = data
        return data
    except Exception as e:
        st.error(f"날씨 정보를 가져오는데 실패했습니다: {e}")
        return None

# Filter marathons based on search criteria
def filter_marathons(search_term, month, distance):
    filtered = []
    for marathon in marathons:
        if (search_term.lower() in marathon["name"].lower() or search_term.lower() in marathon["location"].lower()) and \
           (month == "" or datetime.datetime.strptime(marathon["date"], "%Y-%m-%d").month == int(month)) and \
           (distance == "" or float(distance) == marathon["distance"]):
            filtered.append(marathon)
    return filtered

# UI Design using Streamlit
st.title("한국 마라톤 일정 관리")

# Search Section
st.subheader("마라톤 검색")
search_term = st.text_input("마라톤 검색")
month = st.selectbox("월 선택", [""] + [str(i) for i in range(1, 13)])
distance = st.selectbox("거리 선택", ["", "42.195", "21.0975", "10", "5"])

# Filter and display the marathons
filtered_marathons = filter_marathons(search_term, month, distance)

if st.button("검색"):
    st.write(f"총 마라톤 수: {len(filtered_marathons)}")

    # Display filtered marathons
    if filtered_marathons:
        marathon_table = []
        for marathon in filtered_marathons:
            weather = get_weather(marathon["location"])
            weather_info = f"{weather['main']['temp']}°C, {weather['weather'][0]['description']}" if weather else "날씨 정보 없음"
            marathon_table.append([
                marathon["date"],
                marathon["name"],
                marathon["location"],
                f"{marathon['distance']} km",
                weather_info
            ])
        
        df = pd.DataFrame(marathon_table, columns=["날짜", "대회명", "지역", "거리", "날씨"])
        st.table(df)

# Statistics
st.subheader("통계")
total_marathons = len(marathons)
selected_marathons = len(filtered_marathons)
total_distance = sum(marathon["distance"] for marathon in marathons)

st.write(f"총 마라톤 수: {total_marathons}")
st.write(f"선택된 마라톤: {selected_marathons}")
st.write(f"총 거리 (km): {total_distance}")

# Display Calendar (Basic Calendar Layout)
st.subheader("달력 보기")

today = datetime.date.today()

def draw_calendar(date):
    st.write(f"{date.year}년 {date.month}월")
    days_in_month = (datetime.date(date.year, date.month + 1, 1) - datetime.timedelta(days=1)).day
    month_grid = []
    
    for day in range(1, days_in_month + 1):
        day_str = f"{date.year}-{str(date.month).zfill(2)}-{str(day).zfill(2)}"
        marathons_on_day = [marathon["name"] for marathon in marathons if marathon["date"] == day_str]
        month_grid.append(f"{day}: {', '.join(marathons_on_day)}" if marathons_on_day else str(day))
    
    st.write("\n".join(month_grid))

draw_calendar(today)

st.write("이전 달 또는 다음 달 버튼을 구현하려면 버튼과 상태관리가 필요합니다.")
