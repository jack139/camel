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
from typing import Any

from camel.prompts import TextPrompt, TextPromptDict
from camel.typing import RoleType


# flake8: noqa
class SolutionExtractionPromptTemplateDict(TextPromptDict):
    r"""A dictionary containing :obj:`TextPrompt` used in the `SolutionExtraction`
    task.

    Attributes:
        ASSISTANT_PROMPT (TextPrompt): A system prompt for the AI assistant
            that outlines the rules of the conversation and provides
            instructions for completing tasks.
    """
    ASSISTANT_PROMPT = TextPrompt(
        """你是一位经验丰富的提取解决方案的智能体。
你的任务是通过查看用户和具有特定专业知识的助理之间的对话来提取全部且完整的解决方案。
你应该纯粹根据谈话内容向我提供一个最终的、详细的解决方案。
你应该将解决方案呈现为你的解决方案。
使用现在时，就好像你是提出解决方案的人一样。
你不应错过任何必要的细节或示例。
保留整个对话过程中提供的所有解释和代码。
请记住，你的任务不是总结，而是提取完整的解决方案。""")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.update({
            RoleType.ASSISTANT: self.ASSISTANT_PROMPT,
        })
