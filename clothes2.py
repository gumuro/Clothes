import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Meiryo'
import matplotlib.dates as mdates
import streamlit as st
import requests
from datetime import datetime
from joblib import load
import numpy as np
import joblib
import pandas as pd
from PIL import Image

# 定义 API 密钥（建议通过环境变量或安全方式获取）
API_KEY = "74559e2ae3ff7c8da2c4fe6c70609ee7"
def get_weather_by_time(lat, lon, dt):
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Response Data:", data)  # 打印完整的响应数据
        return data
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

# 用于获取一整天的天气预报的函数
def get_daily_forecast(lat, lon, tz_str):
    timezone = pytz.timezone(tz_str)
    today = datetime.now(timezone).date()
    # 确保开始时间是从0点开始的
    start_time = timezone.localize(datetime.combine(today, datetime.min.time())).timestamp()
    # 结束时间为下一天的0点
    end_time = start_time + 86400  # 24小时后的时间戳
    forecasts = []
    for timestamp in range(int(start_time), int(end_time), 3600):  # 每小时获取一次数据
        weather_data = get_weather_by_time(lat, lon, timestamp)
        if weather_data:
            forecasts.append(weather_data)
    return forecasts

# 根据城市名称获取经纬度
def get_lat_lon(city_name):
    city_coords = {
        "北海道": (43.4672, 142.8278),
        "青森県": (40.8244, 140.7406),
        "岩手県": (39.7036, 141.1527),
        "宮城県": (38.2688, 140.8721),
        "秋田県": (39.7186, 140.1024),
        "山形県": (38.2404, 140.3633),
        "福島県": (37.7608, 140.4748),
        "茨城県": (36.3418, 140.4468),
        "栃木県": (36.5657, 139.8836),
        "群馬県": (36.3911, 139.0608),
        "埼玉県": (35.8569, 139.6489),
        "千葉県": (35.6073, 140.1063),
        "東京都": (35.6895, 139.6917),
        "神奈川県": (35.4475, 139.6424),
        "新潟県": (37.9026, 139.0236),
        "富山県": (36.6953, 137.2113),
        "石川県": (36.5947, 136.6256),
        "福井県": (36.0652, 136.2216),
        "山梨県": (35.6642, 138.5683),
        "長野県": (36.6513, 138.1812),
        "岐阜県": (35.3912, 136.7223),
        "静岡県": (34.9769, 138.3831),
        "愛知県": (35.1802, 136.9066),
        "三重県": (34.7303, 136.5086),
        "滋賀県": (35.0045, 135.8686),
        "京都府": (35.0211, 135.7556),
        "大阪府": (34.6937, 135.5023),
        "兵庫県": (34.6913, 135.1830),
        "奈良県": (34.6851, 135.8050),
        "和歌山県": (34.2260, 135.1675),
        "鳥取県": (35.5036, 134.2383),
        "島根県": (35.4723, 133.0505),
        "岡山県": (34.6618, 133.9344),
        "広島県": (34.3966, 132.4596),
        "山口県": (34.1861, 131.4705),
        "徳島県": (34.0657, 134.5593),
        "香川県": (34.3401, 134.0433),
        "愛媛県": (33.8416, 132.7661),
        "高知県": (33.5597, 133.5311),
        "福岡県": (33.6064, 130.4183),
        "佐賀県": (33.2494, 130.2988),
        "長崎県": (32.7448, 129.8737),
        "熊本県": (32.7898, 130.7417),
        "大分県": (33.2382, 131.6126),
        "宮崎県": (31.9111, 131.4239),
        "鹿児島県": (31.5602, 130.5581),
        "沖縄県": (26.2124, 127.6809)
    }
    return city_coords.get(city_name, (None, None))
city_coords = {
        "北海道": (43.4672, 142.8278),
        "青森県": (40.8244, 140.7406),
        "岩手県": (39.7036, 141.1527),
        "宮城県": (38.2688, 140.8721),
        "秋田県": (39.7186, 140.1024),
        "山形県": (38.2404, 140.3633),
        "福島県": (37.7608, 140.4748),
        "茨城県": (36.3418, 140.4468),
        "栃木県": (36.5657, 139.8836),
        "群馬県": (36.3911, 139.0608),
        "埼玉県": (35.8569, 139.6489),
        "千葉県": (35.6073, 140.1063),
        "東京都": (35.6895, 139.6917),
        "神奈川県": (35.4475, 139.6424),
        "新潟県": (37.9026, 139.0236),
        "富山県": (36.6953, 137.2113),
        "石川県": (36.5947, 136.6256),
        "福井県": (36.0652, 136.2216),
        "山梨県": (35.6642, 138.5683),
        "長野県": (36.6513, 138.1812),
        "岐阜県": (35.3912, 136.7223),
        "静岡県": (34.9769, 138.3831),
        "愛知県": (35.1802, 136.9066),
        "三重県": (34.7303, 136.5086),
        "滋賀県": (35.0045, 135.8686),
        "京都府": (35.0211, 135.7556),
        "大阪府": (34.6937, 135.5023),
        "兵庫県": (34.6913, 135.1830),
        "奈良県": (34.6851, 135.8050),
        "和歌山県": (34.2260, 135.1675),
        "鳥取県": (35.5036, 134.2383),
        "島根県": (35.4723, 133.0505),
        "岡山県": (34.6618, 133.9344),
        "広島県": (34.3966, 132.4596),
        "山口県": (34.1861, 131.4705),
        "徳島県": (34.0657, 134.5593),
        "香川県": (34.3401, 134.0433),
        "愛媛県": (33.8416, 132.7661),
        "高知県": (33.5597, 133.5311),
        "福岡県": (33.6064, 130.4183),
        "佐賀県": (33.2494, 130.2988),
        "長崎県": (32.7448, 129.8737),
        "熊本県": (32.7898, 130.7417),
        "大分県": (33.2382, 131.6126),
        "宮崎県": (31.9111, 131.4239),
        "鹿児島県": (31.5602, 130.5581),
        "沖縄県": (26.2124, 127.6809)
}
city_names = list(city_coords.keys())

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

# 初始化布局和样式
st.markdown("""
<style>
.weather-card {
    background-color: #90e0ee;
    color: #333;
    padding: 10px 10px;
    border-radius: 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: sans-serif;
}
.city-select {
    border: none;
    background-color: inherit;
    font-size: 1em;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# 选择城市的下拉列表
st.write("都道府県を選択してください")
city_name = st.selectbox("", options=list(city_coords.keys()), format_func=lambda x: x, key="city")

# 获取选中城市的天气数据
API_KEY = "74559e2ae3ff7c8da2c4fe6c70609ee7"

city_id = list(city_coords.keys())

def get_weather(lat, lon,  API_KEY):
    API_KEY = "74559e2ae3ff7c8da2c4fe6c70609ee7"
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

weather_data = get_weather(city_id, API_KEY)
API_KEY = "74559e2ae3ff7c8da2c4fe6c70609ee7"
# 处理API数据并计算季节
current_date = datetime.now()
season = determine_season(current_date)
max_tem = weather_data['daily']['temp_max']
min_tem = weather_data['daily']['temp_min']
mean_tem = (max_tem + min_tem) / 2
average_humidity = weather_data['daily']['humidity']
average_wind_speed = weather_data['wind']['speed']
sensible_temperature = weather_data['daily']['feels_like']

# 加载模型和标签编码器
model_path = 'C:/1作品/picture_myclothes/random_forest_classifier.joblib'
model = load(model_path)
season_encoder = joblib.load('C:/1作品/picture_myclothes/season_encoder.joblib')

# 使用标签编码器转换新的输入数据
season_encoded = season_encoder.transform([season])

# 模型输入数据
input_data = [
    max_tem,
    min_tem,
    mean_tem,
    average_humidity,
    average_wind_speed,
    sensible_temperature,
    season_encoded[0]  # 季节编码
]


# 获取穿衣建议
clothing_advice_list = model.predict([input_data])[0]

# 创建天气卡片和展示穿衣建议
icon_code = weather_data['weather'][0]['icon']
icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
current_time = datetime.now().strftime("%H:%M %Y-%m-%d %a")

st.markdown(f"""
<div class="weather-card">
    <div>
        <h2>{city_name}</h2>
    </div>
    <div>
        <img src="{icon_url}" alt="weather icon">
    </div>
    <div>
        <p>気温： {weather_data['main']['temp_min']}~{weather_data['main']['temp_max']}°C</p>
        <p>体感気温：{weather_data['main']['feels_like']}°C</p>
        <p>風速： {weather_data['wind']['speed']} m/s</p>
        <p>湿度： {weather_data['main']['humidity']}%</p>
    </div>
    <div>
        <p>{current_time}</p>
    </div>
</div>
""", unsafe_allow_html=True)

#st.write(f"Clothing advice for today: {clothing_advice[0]}")


clothes_df = pd.read_excel('C:/1作品/picture_myclothes/clothes.xlsx')
      
unique_clothing_types = set(clothing_advice_list)

# 设置Streamlit布局
st.write("　　　　　　")
st.write("　　　　　　")
col1, col2 = st.columns([1, 2])  # 左边一列，右边两列宽度

with col1:
    st.write("         ")
    st.write("選択した服")

# 显示每件衣服
for index, clothing_type in enumerate(unique_clothing_types):
    matched_rows = clothes_df[clothes_df['type'] == clothing_type]
    if not matched_rows.empty:
        # 取得图片路径
        image_path = matched_rows.iloc[0]['name']  # 确保这里是正确的列名
        try:
            # 使用Pillow加载图片
            image = Image.open(image_path)

            # 根据衣服数量分配到左边或右边列
            col = col1 if index == 0 else col2

            with col:
                # 直接使用 Streamlit 函数显示图片
                st.image(image, caption=clothing_type, width=150)
        except FileNotFoundError:
            st.error(f"无法找到文件：{image_path}")


