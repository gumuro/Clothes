import streamlit as st
import requests
from datetime import datetime
from joblib import load
import numpy as np
import joblib
import pandas as pd
from PIL import Image
import json

# 定义城市和季节判断函数
cities = {
  "北海道": {"lat": 43.4672, "lon": 142.8278},
  "青森県": {"lat": 40.8244, "lon": 140.7406},
  "岩手県": {"lat": 39.7036, "lon": 141.1527},
  "宮城県": {"lat": 38.2688, "lon": 140.8721},
  "秋田県": {"lat": 39.7186, "lon": 140.1024},
  "山形県": {"lat": 38.2404, "lon": 140.3633},
  "福島県": {"lat": 37.7608, "lon": 140.4748},
  "茨城県": {"lat": 36.3418, "lon": 140.4468},
  "栃木県": {"lat": 36.5657, "lon": 139.8836},
  "群馬県": {"lat": 36.3911, "lon": 139.0608},
  "埼玉県": {"lat": 35.8569, "lon": 139.6489},
  "千葉県": {"lat": 35.6073, "lon": 140.1063},
  "東京都": {"lat": 35.6895, "lon": 139.6917},
  "神奈川県": {"lat": 35.4475, "lon": 139.6424},
  "新潟県": {"lat": 37.9026, "lon": 139.0236},
  "富山県": {"lat": 36.6953, "lon": 137.2113},
  "石川県": {"lat": 36.5947, "lon": 136.6256},
  "福井県": {"lat": 36.0652, "lon": 136.2216},
  "山梨県": {"lat": 35.6642, "lon": 138.5683},
  "長野県": {"lat": 36.6513, "lon": 138.1812},
  "岐阜県": {"lat": 35.3912, "lon": 136.7223},
  "静岡県": {"lat": 34.9769, "lon": 138.3831},
  "愛知県": {"lat": 35.1802, "lon": 136.9066},
  "三重県": {"lat": 34.7303, "lon": 136.5086},
  "滋賀県": {"lat": 35.0045, "lon": 135.8686},
  "京都府": {"lat": 35.0211, "lon": 135.7556},
  "大阪府": {"lat": 34.6937, "lon": 135.5023},
  "兵庫県": {"lat": 34.6913, "lon": 135.1830},
  "奈良県": {"lat": 34.6851, "lon": 135.8050},
  "和歌山県": {"lat": 34.2260, "lon": 135.1675},
  "鳥取県": {"lat": 35.5036, "lon": 134.2383},
  "島根県": {"lat": 35.4723, "lon": 133.0505},
  "岡山県": {"lat": 34.6618, "lon": 133.9344},
  "広島県": {"lat": 34.3966, "lon": 132.4596},
  "山口県": {"lat": 34.1861, "lon": 131.4705},
  "徳島県": {"lat": 34.0657, "lon": 134.5593},
  "香川県": {"lat": 34.3401, "lon": 134.0433},
  "愛媛県": {"lat": 33.8416, "lon": 132.7661},
  "高知県": {"lat": 33.5597, "lon": 133.5311},
  "福岡県": {"lat": 33.6064, "lon": 130.4183},
  "佐賀県": {"lat": 33.2494, "lon": 130.2988},
  "長崎県": {"lat": 32.7448, "lon": 129.8737},
  "熊本県": {"lat": 32.7898, "lon": 130.7417},
  "大分県": {"lat": 33.2382, "lon": 131.6126},
  "宮崎県": {"lat": 31.9111, "lon": 131.4239},
  "鹿児島県": {"lat": 31.5602, "lon": 130.5581},
  "沖縄県": {"lat": 26.2124, "lon": 127.6809}
}

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

# 以下のCSSをページ全体に適用
st.markdown("""
<style>
/* 全体の背景色を設定 */
body {
    background-color: #02ad21;
}

header {
    background-color: #02ad21;
    padding: 7px 7px;
    color: white;
    text-align: center;
    position: absolute;
    width: 100%;
}


/* フッター部分のスタイル */
footer {
    background-color: #02ad21;
    padding: 7px 7px;
    color: white;
    text-align: center;
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
}

/* 天気カードのスタイリング */
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

# ヘッダーの追加
st.markdown('<header>オススメ服</header>', unsafe_allow_html=True)
st.write("         ")
st.write("         ")
st.write("         ")
st.markdown('<footer>オススメ服</footer>', unsafe_allow_html=True)



# 选择城市的下拉列表
st.write("都道府県を選択してください")
city_name = st.selectbox("", options=list(cities.keys()))

lat = cities[city_name]["lat"]
lon = cities[city_name]["lon"]

# 获取选中城市的天气数据
credentials_dict = json.loads(st.secrets["OpenWeather_API"])
API_KEY = credentials_dict["api_key"]

city_id = cities[city_name]

def get_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ja"
    response = requests.get(url)
    data = response.json()
    return data

weather_data = get_weather(lat, lon, API_KEY)

# 处理API数据并计算季节
current_date = datetime.now()
season = determine_season(current_date)
daily_forecast = weather_data['daily'][0]
max_tem = daily_forecast['temp']['max']
min_tem = daily_forecast['temp']['min']
mean_tem = (max_tem + min_tem) / 2
average_humidity = daily_forecast['humidity']
average_wind_speed = daily_forecast['wind_speed']
sensible_temperature = daily_forecast['feels_like']['day']

# 加载模型和标签编码器
model_path = 'random_forest_classifier.joblib'
model = load(model_path)
season_encoder = joblib.load('season_encoder.joblib')

# 使用标签编码器转换新的输入数据
season_encoded = season_encoder.transform([season])

# 模型输入数据
input_data = np.array([
    max_tem,
    min_tem,
    mean_tem,
    average_humidity,
    average_wind_speed,
    sensible_temperature,
    season_encoded[0]  # 季節が数値にエンコードされていることを確認
]).reshape(1, -1)


# 获取穿衣建议
clothing_advice_list = model.predict(input_data)[0]

# 创建天气卡片和展示穿衣建议
icon_code = daily_forecast['weather'][0]['icon']
icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
current_time = datetime.now().strftime("%H:%M")
current_weekday = datetime.now().strftime("%A")
current_date = datetime.now().strftime("%Y-%m-%d")

st.markdown(f"""
<div class="weather-card">
    <div>
        <h2>{city_name}</h2>
    </div>
    <div>
        <img src="{icon_url}" alt="weather icon">
    </div>
    <div>
        <p>気温： {daily_forecast['temp']['min']}~{daily_forecast['temp']['max']}°C</p>
        <p>体感気温：{daily_forecast['feels_like']['day']}°C</p>
        <p>風速： {daily_forecast['wind_speed']} m/s</p>
        <p>湿度： {daily_forecast['humidity']}%</p>
    </div>
    <div>
        <p>時間：{current_time}</p>
        <p>曜日：{current_weekday}</p>
        <p>日付：{current_date}</p>
    </div>
</div>
""", unsafe_allow_html=True)



# Excelファイルから服のデータを読み込む
clothes_df = pd.read_excel('clothes.xlsx')
unique_clothing_types = set(clothing_advice_list)

st.write("         ")
st.write("         ")
st.write("         ")
st.write("オススメ服")

# 服の画像を表示する列を作成
cols = st.columns(2)  # 2列を作成

# 服の画像とキャプションを表示
for index, clothing_type in enumerate(unique_clothing_types):
    matched_rows = clothes_df[clothes_df['type'] == clothing_type]
    if not matched_rows.empty:
        # 画像のパスを取得
        image_path = matched_rows.iloc[0]['name']  # 'name'は画像のパスが含まれる列名です
        try:
            # 画像を読み込む
            image = Image.open(image_path)
            # 画像を列に配置
            col_index = index % 2  # 0または1の値を取得
            cols[col_index].image(image, caption=clothing_type, width=150)  # 画像を表示
        except FileNotFoundError:
            st.error(f"ファイルが見つかりません：{image_path}")


# ボタンを追加
if st.button("服のファッショントレンド"):
    # ボタンが押されたときにリンクを開く
    st.markdown("[ファッショントレンドへのリンク](https://public.tableau.com/app/profile/kaku.bokuyou/viz/fuku21/1?publish=yes)")

