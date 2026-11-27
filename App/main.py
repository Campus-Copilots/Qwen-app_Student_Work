import gradio as gr
import os
from dotenv import load_dotenv

from skills import generate_weather_html
from llm_client import generate_reply

# 加载环境变量
load_dotenv()
MY_API_KEY = os.getenv("DASHSCOPE_API_KEY")


# 中间件：把 UI 的输入转给 llm_client
def chat_interface(message, history, model_choice):
    # 这里使用了 yield from，这样 llm_client 里的流式输出可以直接传递给前端
    yield from generate_reply(message, history, model_choice, MY_API_KEY)


# ==========================================
# UI 布局部分
# ==========================================
with gr.Blocks(title="Qwen 多模型助手") as demo:
    # 侧边栏设置
    with gr.Sidebar(label="设置", open=False):
        gr.Markdown("### ⚙️ 助手配置")
        model_dropdown = gr.Dropdown(
            choices=["qwen-flash", "qwen-plus"], #这里可以添/删除加模型
            value="qwen-flash", #确定首选模型
            label="选择大模型"
        )
        gr.Markdown("> 💡 *如果遇到 429 错误，请在此切换模型。*")

    # 顶部标题栏与天气组件
    with gr.Row(elem_classes="flex items-center justify-between"):  # 让整体居中对齐
        with gr.Column(scale=8):  # 左侧标题占大头
            gr.Markdown("# 🎓 大学生 AI 私人助手")
        with gr.Column(scale=2, elem_classes="flex justify-end"):  # 右侧天气占小头，且靠右
            # 调用 skills.py 里的函数生成更小巧的天气组件
            weather_component = gr.HTML(value=generate_weather_html("青岛"))

    # 聊天界面
    chatbot = gr.ChatInterface(
        fn=chat_interface,  # 注意这里用的是上面定义的中间件
        additional_inputs=[model_dropdown],
        title=None,
        examples=[
            ["今天适合出门探险吗？", "qwen-flash"],   #这里可以添加示例和对应的模型
            ["周末图书馆开门吗？", "qwen-flash"]
        ]
    )

if __name__ == "__main__":
    # 以后只要运行 python main.py 就可以了
    demo.launch(share=False)