import streamlit as st
import requests
from datetime import datetime

# 假设您已经有了API_KEY
API_KEY = "74559e2ae3ff7c8da2c4fe6c70609ee7"
# 定义一个包含县名称和其对应的经纬度的字典
prefectures = {
    "北海道": {"lat": 43.0642, "lon": 141.3469},
    "青森県": {"lat": 40.8244, "lon": 140.7400},
    # 添加所有其他县的数据...
}

# 让用户从下拉列表中选择一个县
selected_prefecture = st.selectbox("県を選択してください", list(prefectures.keys()))
# 获取用户选定的县的经纬度
lat = prefectures[selected_prefecture]["lat"]
lon = prefectures[selected_prefecture]["lon"]

# 获取7天的天气数据
response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely&appid={API_KEY}&units=metric"
)
weather_data = response.json()

# 自定义 CSS 样式
card_style = """
<style>
.weather-card {
    border-radius: 10px;
    background-color: #ADD8E6; /* 浅蓝色背景 */
    padding: 10px;
    margin: 5px;
    text-align: center;
    display: inline-block;
    width: 100px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* 添加阴影以增加深度感 */
}
.weather-icon {
    width: 50px;
    height: 50px;
}
.weather-button {
    display: block;
    margin: 10px auto;
    padding: 5px 10px;
    background-color: #f2f2f2; /* 按钮的浅灰色背景 */
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>
"""

# 在Streamlit中显示标题和自定义样式
st.markdown(card_style, unsafe_allow_html=True)
st.title(f"{selected_prefecture}の7日間の天気予報")

# 使用Streamlit列来布局天气卡片
cols = st.columns(7)  # 为一周的7天创建7个列
for i, day in enumerate(weather_data['daily'][:7]):  # 限制为7天
    date = datetime.fromtimestamp(day['dt']).strftime('%m/%d')
    weather_description = day['weather'][0]['main']
    icon_code = day['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
    temp_min = day['temp']['min']
    temp_max = day['temp']['max']
    
    with cols[i]:
        # 为天气卡片使用 `st.markdown()` 来应用样式
        st.markdown(f"""
        <div class='weather-card'>
            <strong>{date}</strong><br>
            <img src='{icon_url}' class='weather-icon'><br>
            {weather_description}<br>
            {temp_min}~{temp_max} °C
            <button class='weather-button'>服装推薦を表示</button>
        </div>
        """, unsafe_allow_html=True)
