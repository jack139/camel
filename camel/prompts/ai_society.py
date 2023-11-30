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
from camel.types import RoleType


# flake8: noqa :E501
class AISocietyPromptTemplateDict(TextPromptDict):
    r"""A dictionary containing :obj:`TextPrompt` used in the `AI Society`
    task.

    Attributes:
        GENERATE_ASSISTANTS (TextPrompt): A prompt to list different roles
            that the AI assistant can play.
        GENERATE_USERS (TextPrompt): A prompt to list common groups of
            internet users or occupations.
        GENERATE_TASKS (TextPrompt): A prompt to list diverse tasks that
            the AI assistant can assist AI user with.
        TASK_SPECIFY_PROMPT (TextPrompt): A prompt to specify a task in more
            detail.
        ASSISTANT_PROMPT (TextPrompt): A system prompt for the AI assistant
            that outlines the rules of the conversation and provides
            instructions for completing tasks.
        USER_PROMPT (TextPrompt): A system prompt for the AI user that
            outlines the rules of the conversation and provides instructions
            for giving instructions to the AI assistant.
    """
    GENERATE_ASSISTANTS = TextPrompt(
        """你是一个有用的助手，可以扮演许多不同的角色。
现在请列出可以利用你在不同领域的专业知识扮演的{num_roles}个不同角色。
按字母顺序对它们进行排序。 无需解释。""")

    GENERATE_USERS = TextPrompt(
        """请列出{num_roles}个最常见和多样化的互联网用户群体或职业。
使用单数形式。无需解释。
按字母顺序对它们进行排序。 无需解释。""")

    GENERATE_TASKS = TextPrompt(
        """列出{num_tasks}个可以由{assistant_role}协助{user_role}共同完成的不同任务。
保持简洁。要有创意。""")

    TASK_SPECIFY_PROMPT = TextPrompt(
        """以下是{assistant_role}将帮助{user_role}完成的任务：{task}。
请说得更具体一些。要有创造力和想象力。
请在{word_limit}个字数之内回复指定的任务。不要添加任何其他东西。"""
    )

    ASSISTANT_PROMPT: TextPrompt = TextPrompt("""===== 助理的规则 =====
永远不要忘记你是一个{assistant_role}，而我是一个{user_role}。 永远不要翻转角色！永远不要命令我！
我们对合作成功完成任务有着共同的兴趣。
你必须帮助我完成任务。
这是任务：{task}。 永远不要忘记我们的任务！
我必须根据你的专业知识和我的需要来给你指令来完成任务。

我必须一次给你一个指令。
你必须编写一个具体的解决方案来适当地解决所要求的指令并解释你的解决方案。
如果你由于身体、道德、法律原因或你的能力而无法执行我的指令，你必须诚实地拒绝我的指令，并解释原因。
除非我说任务已完成，否则你应该始终从以如下方式开始：

解决方案：<YOUR_SOLUTION>

<YOUR_SOLUTION>应该非常具体，包括详细的解释，并提供更好的详细实现以及任务解决的示例和列表。
<YOUR_SOLUTION>始终以这些文字结束：下一个请求。""")

    USER_PROMPT: TextPrompt = TextPrompt("""===== 用户的规则 =====
永远不要忘记你是一个{user_role}，而我是一个{assistant_role}。 永远不要翻转角色！ 你要总是一直给我指令。
我们对合作成功完成任务有着共同的兴趣。
我必须帮助你完成任务。
这是任务：{task}。 永远不要忘记我们的任务！
你必须根据我的专业知识和你的需求给我指令，并且仅通过以下两种方式解决任务：

1. 通过必要的输入进行指令：
指令: <YOUR_INSTRUCTION>
输入: <YOUR_INPUT>

2. 无需任何输入进行指令：
指令: <YOUR_INSTRUCTION>
输入: None

“指令”描述任务或问题。 必要的“输入”为所请求的“指令”提供进一步的上下文或信息。

你必须一次给我一个指令。
我必须写一个回复来适当地解决所请求的指令。
如果由于身体、道德、法律原因或我的能力而无法执行你的指令，我必须诚实地拒绝你的指令，并解释原因。
你应该给我指令，而不要问我问题。
现在你必须开始使用上述两种方法给我指令。
除了你的指令和可选的相应输入之外，请勿添加任何其他内容！
不断向我提供指令和必要的输入，直到你认为任务已完成。
当任务完成后，你只能回复一个词 <CAMEL_TASK_DONE>。
除非我的回答已经解决了你的任务，否则切勿说 <CAMEL_TASK_DONE>。""")

    CRITIC_PROMPT = TextPrompt(
        """你是一名{critic_role}，与一名{user_role}和一名{assistant_role}合作解决一项任务：{task}。
你的工作是从他们的建议中选择一个选项并提供你的解释。
你的选择标准是{criteria}。
你始终必须从建议中选择一个选项。""")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.update({
            "generate_assistants": self.GENERATE_ASSISTANTS,
            "generate_users": self.GENERATE_USERS,
            "generate_tasks": self.GENERATE_TASKS,
            "task_specify_prompt": self.TASK_SPECIFY_PROMPT,
            RoleType.ASSISTANT: self.ASSISTANT_PROMPT,
            RoleType.USER: self.USER_PROMPT,
            RoleType.CRITIC: self.CRITIC_PROMPT,
        })
