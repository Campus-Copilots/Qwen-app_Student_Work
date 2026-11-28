import requests

# 1. 基础获取天气函数（接收地区代码）
def get_weather_data(city_code="101110101"):
    try:
        url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
        res = requests.get(url, timeout=5)
        data = res.json()

        today_info = data['data']['forecast'][0]
        current_temp = data['data']['wendu']
        high = today_info['high'].replace('高温 ', '')
        low = today_info['low'].replace('低温 ', '')
        weather_type = today_info['type']

        return current_temp, high, low, weather_type
    except Exception as e:
        print("天气接口报错:", e)
        return None, None, None, None


# 2. 生成漂亮的 HTML 卡片（用于顶部展示）
def get_beautiful_weather_html(city_name, current_temp, high, low, weather_type):
    icon = "🌤️"
    if "晴" in weather_type: icon = "☀️"
    elif "雨" in weather_type: icon = "🌧️"
    elif "阴" in weather_type or "云" in weather_type: icon = "☁️"

    temp_clean = str(current_temp).replace("°C", "").replace("℃", "")

    # 🌟 完美版 HTML 卡片
    html = f"""
    <div style="
        display: flex; align-items: center; justify-content: space-between;
        background: #f8f9fa; padding: 12px 18px; border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); font-family: Arial, sans-serif;
        width: 100%; box-sizing: border-box; border: 1px solid #e5e7eb;
    ">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 2.2rem;">{icon}</span>
            <div style="display: flex; flex-direction: column; gap: 2px;">
                <!-- 给下拉菜单留出空间，文字先隐藏，由真正的下拉框盖上来 -->
                <div style="font-size: 1.1rem; font-weight: bold; color: transparent;">
                    {city_name} ▼
                </div>
                <div style="font-size: 0.85rem; color: #666;">
                    {weather_type} | {low} ~ {high}
                </div>
            </div>
        </div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #007bff;">
            {temp_clean}°C
        </div>
    </div>
    """
    return html

# 3. 给大模型提供纯文本天气数据
def get_weather_text_for_llm(city_name="西安市", city_code="101110101"):
    current_temp, high, low, weather_type = get_weather_data(city_code)
    if current_temp is None:
        return ""
    return f"当前{city_name}的天气是：{weather_type}，气温 {current_temp}°C，最高温 {high}，最低温 {low}。"