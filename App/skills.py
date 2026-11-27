import requests


# 1. 最基础的获取天气数据的函数
def get_weather_data(city_code="101120201"): #在这里可以修改城市代码，后续看看能不能做成定位获取城市代码
    # 101120201 是青岛的代码，你要查别的城市去网上搜对应的代码
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


# 2. 生成紧凑版 HTML 卡片（用于界面右上角）
def generate_weather_html(city="青岛"):
    current_temp, high, low, weather_type = get_weather_data()

    if current_temp is None:
        return f"<div style='color: #ef4444; padding: 5px; font-size: 0.8rem;'>⚠️ 天气获取失败</div>"

    icon = "🌤️"
    if "晴" in weather_type:
        icon = "☀️"
    elif "雨" in weather_type:
        icon = "🌧️"
    elif "阴" in weather_type or "云" in weather_type:
        icon = "☁️"

    html_content = f"""
    <div style="
        display: inline-flex; 
        align-items: center; 
        background: #f8f9fa; 
        border-radius: 8px; 
        padding: 5px 12px; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        font-family: Arial, sans-serif;
    ">
        <div style="font-size: 1.5rem; margin-right: 8px;">{icon}</div>
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <div style="display: flex; align-items: baseline; gap: 6px;">
                <span style="font-size: 0.9rem; font-weight: bold; color: #333;">{city}</span>
                <span style="font-size: 1.1rem; font-weight: bold; color: #007bff;">{current_temp}°C</span>
            </div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 2px;">
                {weather_type} | {low}~{high}
            </div>
        </div>
    </div>
    """
    return html_content


# 3. 给大模型提供纯文本天气数据（聊天对话时用的）
def get_weather_text_for_llm(city="青岛"):
    current_temp, high, low, weather_type = get_weather_data()
    if current_temp is None:
        return ""
    return f"当前{city}的天气是：{weather_type}，气温 {current_temp}°C，最高温 {high}，最低温 {low}。"