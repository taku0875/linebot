import streamlit as st
import requests
from datetime import datetime
import pandas as pd




# 都市コードのリスト
city_code_list = {
    "北海道": "016010",
    "仙台": "040010",
    "東京": "130010",
    "大阪": "270000",
    "博多": "400010",
    "南の果て": "474020",
}

# タイトルと地域選択の表示
st.title("あなたのお住いの天気は？")
st.write("お住まいの地域を選択してください")
selected_city = st.selectbox("地域を選択してください。", city_code_list.keys())

# 選択された地域のコード
city_code = city_code_list[selected_city]
current_city_code = st.empty()
current_city_code.write("選択している地域: " + selected_city)

# 天気APIのURL
url = "https://weather.tsukumijima.net/api/forecast/city/" + city_code

# APIから天気情報を取得
response = requests.get(url)

# ステータスコードが200であることを確認
if response.status_code == 200:
    weather_json = response.json()
    now_hour = datetime.now().hour

    # 'forecasts'キーが存在するか確認
    if 'forecasts' in weather_json:
        chance_of_rain = weather_json['forecasts'][0].get('chanceOfRain', {})

        # 時間帯による降水確率の取得
        if 0 <= now_hour < 6:
            weather_now = chance_of_rain.get('T00_06', 'データなし')
        elif 6 <= now_hour < 12:
            weather_now = chance_of_rain.get('T06_12', 'データなし')
        elif 12 <= now_hour < 18:
            weather_now = chance_of_rain.get('T12_18', 'データなし')
        else:
            weather_now = chance_of_rain.get('T18_24', 'データなし')

        # 現在の降水確率表示
        weather_now_text = "只今の降水確率: " + weather_now
        st.write(weather_now_text)

        # 明日と明後日の降水確率を表示
        df1 = pd.DataFrame(weather_json['forecasts'][0].get('chanceOfRain', {}), index=["今日"])
        df2 = pd.DataFrame(weather_json['forecasts'][1].get('chanceOfRain', {}), index=["明日"])
        df3 = pd.DataFrame(weather_json['forecasts'][2].get('chanceOfRain', {}), index=["明後日"])

        # DataFrameを結合して表示
        df = pd.concat([df1, df2, df3])
        st.dataframe(df)
    else:
        st.error("天気予報情報が見つかりませんでした。")
else:
    st.error("天気情報の取得に失敗しました。APIステータスコード: " + str(response.status_code))

if st.button('🌟 天気をリフレッシュ 🌟'):
    st.experimental_rerun()