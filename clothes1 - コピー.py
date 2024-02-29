import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Meiryo'
import matplotlib.dates as mdates
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
# 获取温度范围的函数
def get_temp_range(daily_forecast, timezone_str):
    tz = pytz.timezone(timezone_str)
    today_start = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = (today_start + timedelta(days=1)) - timedelta(seconds=1)
    today_temps = [data_point['temp']
                   for forecast in daily_forecast
                   for data_point in forecast['data']  # 这里添加一个循环来遍历 'data' 列表
                   if 'dt' in data_point and today_start <= datetime.fromtimestamp(data_point['dt'], tz) < today_end]
    if today_temps:
        min_temp = min(today_temps)
        max_temp = max(today_temps)
        return min_temp, max_temp
    else:
        return None, None
# 假设您的 Excel 文件路径是 'clothes.xlsx'
df_clothes = pd.read_excel('clothes.xlsx')
def get_combined_recommendations(df, current_temp, tolerance=3, num_outfits=3):
    # 分别找出内搭和外套
    inner_clothes = df[(df['type'] == 'inner') &
                       (df['suitable temperature'] >= current_temp - tolerance) &
                       (df['suitable temperature'] <= current_temp + tolerance)]
    outer_clothes = df[(df['type'] == 'outer') &
                       (df['suitable temperature'] >= current_temp - tolerance) &
                       (df['suitable temperature'] <= current_temp + tolerance)]
    # 生成搭配组合，确保不重复
    combined_recommendations = []
    used_pairs = set()
    while len(combined_recommendations) < num_outfits:
        if not inner_clothes.empty and not outer_clothes.empty:
            available_inner = inner_clothes.sample(n=len(inner_clothes), replace=False)
            available_outer = outer_clothes.sample(n=len(outer_clothes), replace=False)
            for inner in available_inner.itertuples():
                for outer in available_outer.itertuples():
                    # 检查这个搭配是否已经选过
                    if (inner.Index, outer.Index) not in used_pairs:
                        used_pairs.add((inner.Index, outer.Index))
                        combined_recommendations.append((inner, outer))
                        break
                if len(combined_recommendations) == num_outfits:
                    break
        else:
            break  # 如果没有足够的衣物进行搭配，则退出循环
    return [(inner._asdict(), outer._asdict()) for inner, outer in combined_recommendations]
# Streamlit 应用界面的主要部分
def main():
    st.title("ファッション推薦システム")
    # 使用Markdown添加格式化文本
    st.markdown("""
        <style>
        .big-font {
            font-size:20px !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">このシステムは、今日の天気に基づいて最適な服装を推薦します。</p>', unsafe_allow_html=True)
    st.write("""
        以下の手順に従ってご利用ください：
        1. **天気情報の確認**：画面に表示される本日の天気予報を確認してください。
        2. **服装推薦**：本日の気温に適した服装が自動的に推薦されます。
        3. **服装のアップロード**：お持ちの服の写真をアップロードし、服の種類や適した温度範囲などの情報を入力することもできます。
        システムは、気温や天気の状況に応じて、快適でスタイリッシュな服装を提案します。
    """)
    city_name = st.selectbox("都道府県を選択してください",city_names)
    lat, lon = get_lat_lon(city_name)
    timezone_str = "Asia/Tokyo"
    if lat and lon:
        # 获取当前天气
        daily_forecast = get_daily_forecast(lat, lon, timezone_str)
        if daily_forecast and 'data' in daily_forecast[-1]:
            # 假设最后一个元素是最接近当前时间的预报
            current_data = daily_forecast[-1]['data'][0]
            current_temp = current_data['temp']
            feels_like = current_data['feels_like']
            weather_description = current_data['weather'][0]['description']
            weather_icon = current_data['weather'][0]['icon']
            st.header("今日の天気情報")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"現在の温度: {current_temp}°C")
                st.write(f"体感温度: {feels_like}°C")
                st.write(f"天気状況: {weather_description}")
            with col2:
                st.image(f"http://openweathermap.org/img/w/{weather_icon}.png")
            # 获取一整天的天气预报
            daily_forecast = get_daily_forecast(lat, lon, timezone_str)
            if daily_forecast:
              # 从daily_forecast的每个元素的'data'键中提取时间和温度
              times = []
              temps = []
              for forecast in daily_forecast:
                     for data_point in forecast['data']:
                            times.append(datetime.fromtimestamp(data_point['dt'], tz=pytz.timezone(timezone_str)))
                            temps.append(data_point['temp'])
              if times and temps:
                # 绘制温度变化图表
                plt.figure(figsize=(10, 4))
                plt.plot(times, temps, marker='o')
                plt.title("今日の温度変化")
                plt.xlabel("時間")
                plt.ylabel("温度 (°C)")
                plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                plt.gcf().autofmt_xdate()
                st.pyplot(plt)
                # 获取推荐搭配
                combined_recommendations = get_combined_recommendations(df_clothes, current_temp)
                # 显示推荐搭配
                if combined_recommendations:
                    set_number = 1
                    for inner, outer in combined_recommendations:
                            st.markdown(f"## セット{set_number}：")
                            col1, col2 = st.columns(2)
                            with col1:
                                   st.image(inner['name'], caption=inner['material'], width=300)
                            with col2:
                                   st.image(outer['name'], caption=outer['material'], width=300)
                            set_number += 1
              else:
                    st.error("現在の天気情報の取得に失敗しました。")
            else:
                st.error("天気予報の取得に失敗しました。")
        else:
            st.error("現在の天気情報の取得に失敗しました。")
    else:
        st.error("指定された都市の位置情報が見つかりませんでした。")
    # 上传衣物图片并输入信息
    st.header("服装のアップロード")
    uploaded_file = st.file_uploader("写真を選択してください", type=['jpg', 'png'])
    if uploaded_file is not None:
        # 这里添加处理上传文件的代码
        # ...
        # 输入衣物信息
        st.text_input("服装タイプを入力してください")
        st.text_input("素材を入力してください")
        st.slider("適した温度範囲", min_value=-20, max_value=40, value=(20, 30))
        if st.button("アップロード"):
            st.write("服装がアップロードされました。")
if __name__ == "__main__":
    main()