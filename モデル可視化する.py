import streamlit as st
import requests
from datetime import datetime
from joblib import load
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

# 以下是日本47个县的名称和它们的OpenWeatherMap ID，这里只是示例
# 您需要找到每个县的OpenWeatherMap ID并替换下面的数字
prefectures = {
    "Hokkaido": 2128295,
    "Aomori": 2130658,
    "Iwate": 2112518,
    # ...其余的县
    "Okinawa": 1894616
}

# 季节判断函数
def determine_season(date):
    month = date.month
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Winter'

# 加载模型
model_path = 'C:/1作品/picture_myclothes/random_forest_classifier.joblib'
model = load(model_path)
# 加载保存的标签编码器

season_encoder = joblib.load('C:/1作品/picture_myclothes/season_encoder.joblib')

# 下拉列表选择县
prefecture_name = st.selectbox("Choose a prefecture", options=list(prefectures.keys()))

# 获取天气数据
API_KEY = "74559e2ae3ff7c8da2c4fe6c70609ee7"
prefecture_id = prefectures[prefecture_name]

# 获取天气数据的函数
def get_weather(city_id, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

weather_data = get_weather(prefecture_id, API_KEY)

# 处理API数据并计算季节
current_date = datetime.now()
season = determine_season(current_date)
max_tem = weather_data['main']['temp_max']
min_tem = weather_data['main']['temp_min']
mean_tem = (max_tem + min_tem) / 2
average_humidity = weather_data['main']['humidity']
average_wind_speed = weather_data['wind']['speed']
sensible_temperature = weather_data['main']['feels_like']

label_encoders = {
    'season': LabelEncoder()
}

#假设我们已经拟合了label_encoders并保存了它们
# 加载保存的标签编码器

label_encoders['season'].classes_ = np.load('season_encoder.joblib', allow_pickle=True)

# 使用标签编码器转换新的输入数据

season_encoded = season_encoder.transform([season])

# 模型输入数据
input_data = [ # 天气状况编码
    max_tem,
    min_tem,
    mean_tem,
    average_humidity,
    average_wind_speed,
    sensible_temperature,
    season_encoded[0]  # 季节编码
]
# 获取穿衣建议
clothing_advice = model.predict([input_data])

# 展示穿衣建议
st.write(f"Clothing advice for today: {clothing_advice[0]}")
