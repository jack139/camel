# Local test



## FastChat



### Install

```bash
sudo pip3.9 install "fschat[model_worker,webui]"
sudo pip3.9 install pydantic==1.10.13
sudo pip3.9 install colorama tenacity
sudo pip3.9 install transformers_stream_generator # for Qwen-7B-Chat
```



### Start service

```bash
# Launch the controller
python3.9 -m fastchat.serve.controller

# Launch the model worker(s)
python3.9 -m fastchat.serve.model_worker --model-path ./lm_model/Llama-2-7b-chat-hf

# Launch the RESTful API server
python3.9 -m fastchat.serve.openai_api_server --host localhost --port 8000

# Launch the Gradio web server
python3.9 -m fastchat.serve.gradio_web_server
```



## Camel



### Config

```bash
cp examples/open_source_models/role_playing_with_open_source_model.py .
```

- Edit script ```role_playing_with_open_source_model.py```

```python
    main(
        model_type=ModelType.LLAMA_2,
        model_path="../lm_model/Llama-2-7b-chat-hf",
        server_url="http://localhost:8000/v1",
    )
```



### Run test

```bash
OPENAI_API_KEY=EMPTY python3.9 role_playing_with_open_source_model.py
```
