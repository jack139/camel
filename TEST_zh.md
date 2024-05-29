# Local test



## 使用 FastChat



### 安装

```bash
sudo pip3.9 install "fschat[model_worker,webui]"
sudo pip3.9 install pydantic==1.10.13
sudo pip3.9 install colorama tenacity
sudo pip3.9 install transformers_stream_generator # for Qwen-7B-Chat
sudo pip3.9 install openai==1.30.3 # for camel
sudo pip3.9 install qdrant-client==1.6.4 # vector DB
sudo pip3.9 install "unstructured[unstructured_inference]"
sudo pip3.9 install unstructured unstructured_inference pdf2image pdfminer.six pikepdf pypdf pillow_heif
sudo pip3.9 install opencv-python==4.8.1.78 opencv-contrib-python==4.8.1.78

sudo apt install tesseract-ocr libtesseract-dev # tesseract, for PDF OCR
sudo pip3.9 install unstructured_pytesseract
```



### 启动服务

```bash
# Launch the controller
python3.9 -m fastchat.serve.controller

# Launch the model worker(s)
python3.9 -m fastchat.serve.model_worker --model-path ./lm_model/Qwen-7B-Chat

# Launch the RESTful API server
python3.9 -m fastchat.serve.openai_api_server --host localhost --port 8000

# Launch the Gradio web server
python3.9 -m fastchat.serve.gradio_web_server
```



## Camel 测试



### 配置 LLM

- 修改脚本 ```test_zh.py```

```python
    main(
        model_type=ModelType.QWEN,
        model_path="../lm_model/Qwen-7B-Chat",
        server_url="http://localhost:8000/v1",
    )
```



### 运行测试

```bash
# agent 测试
OPENAI_API_KEY=EMPTY python3.9 -m examples_zh.role_playing

# RAG 测试
OPENAI_API_KEY=EMPTY python3.9 -m examples_zh.rag datasets_test/
```



### 简单微调提示语

- 修改脚本```camel/prompts/ai_society.py```中关于“<你的解决方案>”的提示语可以对结果输出进行一定影响

```python
("""
...

解决方案：<你的解决方案>

<你的解决方案> 应该非常具体和详细，包括详细的解释、更好的详细实现、解决任务的代码示例，和详细的方案项目、步骤列表等。
对于重复提出的指令和输入，<你的解决方案> 需要有一些变化，不要总是提供一样的描述。
<你的解决方案> 最后必须以 “请说下一个指令” 这句话结束。""")
```
