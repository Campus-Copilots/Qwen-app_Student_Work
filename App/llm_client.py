import dashscope
from http import HTTPStatus
from skills import get_weather_text_for_llm

def generate_reply(message, history, model_choice, api_key):
    """核心对话逻辑：负责调用 Qwen 模型并流式返回"""
    try:
        if not api_key:
            yield "【错误】API Key 为空，请检查 .env 文件！"
            return

        dashscope.api_key = api_key

        # 1. 意图识别（简单版：如果问到天气，就去拿天气数据）
        weather_info = ""
        if any(keyword in message for keyword in ["天气", "下雨", "气温", "冷", "热"]):
            weather_info = get_weather_text_for_llm("Colchester")

        # 2. 构建 System Prompt
        system_prompt = "你是一个乐于助人的大学生助手。"
        if weather_info:
            system_prompt += f"\n【实时系统数据】：{weather_info}。请根据这个真实数据回答用户。"

        # 3. 构建 messages
        messages = [{'role': 'system', 'content': system_prompt}]
        for item in history:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                messages.append({'role': 'user', 'content': item[0]})
                messages.append({'role': 'assistant', 'content': item[1]})
        messages.append({'role': 'user', 'content': message})

        # 4. 调用 API
        responses = dashscope.Generation.call(
            model=model_choice,
            messages=messages,
            result_format='message',
            stream=True,
            incremental_output=True
        )

        partial_response = ""
        for response in responses:
            if response.status_code != HTTPStatus.OK:
                yield f"【API报错】状态码: {response.status_code} | 错误码: {response.code} | 错误信息: {response.message}"
                break
            partial_response += response.output.choices[0].message.content
            yield partial_response

    except Exception as e:
        yield f"【代码运行异常】: {str(e)}"