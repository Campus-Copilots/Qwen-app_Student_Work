# LLM Assistant for University Student with Qwen API

## 🚀 本地部署指南 (How to Run)

如果你想在本地运行此项目，请按照以下步骤操作：

### 1. 克隆仓库
```bash
git clone https://github.com/IceContainor/Qwen-app_Student_Work.git
cd Qwen-app_Student_Work
```

### 2. 安装依赖
建议使用虚拟环境运行。在终端中执行：
```bash
pip install -r requirements.txt
```

### 3. 配置 API Key (重要！)
由于安全原因，本项目未包含真实 API Key。请在 App 目录下新建一个名为 .env 的文件，并填入你自己的阿里云百炼 API Key：
```.env文件
DASHSCOPE_API_KEY=sk-你的真实API_KEY
```

### 4. 启动程序
在终端中运行主程序：
```bash
python App/main.py
```