import gradio as gr
import os
from dotenv import load_dotenv

# 导入之前写好的函数
from skills import get_weather_data
from llm_client import generate_reply

# 加载环境变量
load_dotenv()
MY_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def chat_interface(message, history, model_choice):
    yield from generate_reply(message, history, model_choice, MY_API_KEY)


# ==========================================
# 专门为侧边栏定制的“竖排”天气卡片
# ==========================================
def render_sidebar_weather(city_name="西安市", city_code="101110101"):
    current_temp, high, low, weather_type = get_weather_data(city_code)

    if current_temp is None:
        return f"<div style='color: red; font-size: 0.9rem; padding: 10px;'>⚠️ {city_name} 天气获取失败</div>"

    temp_clean = str(current_temp).replace("°C", "").replace("℃", "")

    icon = "🌤️"
    if "晴" in weather_type:
        icon = "☀️"
    elif "雨" in weather_type:
        icon = "🌧️"
    elif "阴" in weather_type or "云" in weather_type:
        icon = "☁️"

    # 🌟 竖排布局，完美适应侧边栏宽度
    html = f"""
    <div style="
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 2px 6px rgba(0,0,0,0.08); font-family: Arial, sans-serif;
        width: 100%; box-sizing: border-box; margin-top: 15px; margin-bottom: 15px;
    ">
        <div style="font-size: 3rem; margin-bottom: 5px;">{icon}</div>
        <div style="font-size: 1.1rem; font-weight: bold; color: #333; margin-bottom: 5px;">
            {city_name}
        </div>
        <div style="font-size: 2.2rem; font-weight: bold; color: #007bff; margin-bottom: 5px;">
            {temp_clean}°C
        </div>
        <div style="font-size: 0.9rem; color: #666; text-align: center;">
            {weather_type} | {low} ~ {high}
        </div>
    </div>
    """
    return html


# ==========================================
# UI 布局部分
# ==========================================
with gr.Blocks(title="Qwen 多模型助手") as demo:
    # 🌟 左侧折叠菜单栏
    with gr.Sidebar(label="设置", open=True):  # open=True 让它默认展开，你可以自己改成 False
        gr.Markdown("### ⚙️ 助手配置")

        # 1. 模型选择下拉框
        model_dropdown = gr.Dropdown(
            choices=["qwen-flash", "qwen-plus"],
            value="qwen-flash",
            label="选择大模型"
        )
        gr.Markdown("> 💡 *如果遇到 429 错误，请在此切换模型。*")

        # 🌟 2. 把天气模块塞进侧边栏
        gr.Markdown("### 🌤️ 今日天气")
        weather_component = gr.HTML(value=render_sidebar_weather("西安市", "101110101"))

    # 🌟 右侧主区域（现在只剩标题和聊天框，极其宽敞）
    gr.Markdown("# 🎓 大学生 AI 私人助手")

    # 聊天界面
    chatbot = gr.ChatInterface(
        fn=chat_interface,
        additional_inputs=[model_dropdown],
        title=None,
        examples=[
            ["今天适合出门探险吗？", "qwen-flash"],
            ["周末图书馆开门吗？", "qwen-flash"]
        ]
    )

if __name__ == "__main__":
    demo.launch(share=False)