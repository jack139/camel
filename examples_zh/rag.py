# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
import os
import sys
from pathlib import Path
from typing import Dict, List
import readline # 解决input中文时问题，例如删除时回显不正确

from camel.configs import ChatGPTConfig, OpenSourceConfig
from camel.agents import ChatAgent
from camel.embeddings import OpenAIEmbedding
from camel.memories import ChatHistoryMemory, ScoreBasedContextCreator
from camel.memories.rag import RAGmemory
from camel.messages import BaseMessage
from camel.storages import QdrantStorage
from camel.types import ModelType, RoleType, EmbeddingModelType, VectorDistance
from camel.utils import OpenSourceTokenCounter


def get_result_files(folder_path, debug=False) -> List[Dict]:
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


def agent_rag(paths: List[str]) -> None:
    files = []
    for path in paths:
        files += Path(path).rglob("*.pdf")
    print(f"Load file: {files}")

    model_type = ModelType.QWEN
    model_path = "../lm_model/Qwen1.5-7B-Chat"
    server_url = "http://localhost:8000/v1"

    context_creator = ScoreBasedContextCreator(
        OpenSourceTokenCounter(model_type, model_path), # for QWen
        model_type.token_limit,
    )
    embedding = OpenAIEmbedding(
        model_type=EmbeddingModelType.QWEN_7B,
        server_url=server_url,
    )
    memory = RAGmemory(
        context_creator,
        ChatHistoryMemory(context_creator),
        QdrantStorage(
            embedding.get_output_dim(),
            path="./ragdb",
            create_collection=True,
            collection="handbook",
            distance=VectorDistance.COSINE,
        ),
        embedding=embedding,
        files=files,
    )
    #print(memory.vector_storage._get_collection_info("handbook"))
    content = """您是一个有用的助手，可以根据给定的上下文回答用户的问题。
您可以使用的唯一信息是给定的上下文。除了给定的内容之外，您不应提供任何其他信息。
如果您认为给定的上下文不足以回答问题，您可以指示用户提供更多信息。
请不要在您的回答中提及“上下文”一词。它应该对用户隐藏。"""
    system_message = BaseMessage("General assistant", RoleType.ASSISTANT,
                                 meta_dict=None, content=content)

    # agent settings
    agent_kwargs = dict(
        model_type=model_type,
        model_config=OpenSourceConfig(
            model_path=model_path,
            server_url=server_url,
            api_params=ChatGPTConfig(temperature=0.5, frequency_penalty=0.3),
        )
    )

    agent = ChatAgent(
        system_message=system_message,
        memory=memory,
        **(agent_kwargs),
    )
    print(
        "你好。我是RAG助手。我可以根据预制的手册回答任何问题。"
    )
    for _ in range(50):
        question = input("请输入您的问题：")
        user_msg = BaseMessage("User", RoleType.USER, meta_dict=None,
                               content=question)
        response = agent.step(user_msg)
        print(response.msg.content)


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        paths = ["./"]

    agent_rag(paths)
