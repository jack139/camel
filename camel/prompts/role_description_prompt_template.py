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

from camel.prompts import AISocietyPromptTemplateDict, TextPrompt
from camel.typing import RoleType


# flake8: noqa :E501
class RoleDescriptionPromptTemplateDict(AISocietyPromptTemplateDict):
    r"""A dictionary containing :obj:`TextPrompt` used in the `role description`
    task.

    Attributes:
        ROLE_DESCRIPTION_PROMPT (TextPrompt): A default prompt to
            describe the role descriptions.
        ASSISTANT_PROMPT (TextPrompt): A system prompt for the AI assistant
            that outlines the rules of the conversation and provides
            instructions for completing tasks.
        USER_PROMPT (TextPrompt): A system prompt for the AI user that
            outlines the rules of the conversation and provides instructions
            for giving instructions to the AI assistant.
    """
    ROLE_DESCRIPTION_PROMPT = TextPrompt("""===== 角色及其描述 =====
{user_role}和{assistant_role}正在协作完成任务：{task}。
{user_role}用来完成任务的能力、特征、职责和工作流程：{user_description}
{assistant_role}的能力、特征、职责和完成任务的工作流程：{assistant_description}
""")

    ASSISTANT_PROMPT = TextPrompt(ROLE_DESCRIPTION_PROMPT +
                                  AISocietyPromptTemplateDict.ASSISTANT_PROMPT)

    USER_PROMPT = TextPrompt(ROLE_DESCRIPTION_PROMPT +
                             AISocietyPromptTemplateDict.USER_PROMPT)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.update({
            "role_description": self.ROLE_DESCRIPTION_PROMPT,
            RoleType.ASSISTANT: self.ASSISTANT_PROMPT,
            RoleType.USER: self.USER_PROMPT,
        })
