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
class CodePromptTemplateDict(TextPromptDict):
    r"""A dictionary containing :obj:`TextPrompt` used in the `Code` task.

    Attributes:
        GENERATE_LANGUAGES (TextPrompt): A prompt to list different computer
            programming languages.
        GENERATE_DOMAINS (TextPrompt): A prompt to list common fields of study
            that programming could help with.
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
    GENERATE_LANGUAGES = TextPrompt(
        """列出{num_languages}最常用的计算机编程语言。
保持简洁。 无需解释。""")

    GENERATE_DOMAINS = TextPrompt(
        """列出{num_domains}个编程可以帮助的最常见的研究领域。
保持简洁。 按字母顺序对它们进行排序。 无需解释。""")

    GENERATE_TASKS = TextPrompt(
        """列出程序员可以帮助使用{language}在{domain}中工作的人员执行的{num_tasks}个不同的任务。
保持简洁。 要有创意。""")

    TASK_SPECIFY_PROMPT = TextPrompt(
        """以下是程序员将帮助在{domain}中工作的人员使用{language}完成的任务：{task}。
请说得更具体一些。 要有创造力和想象力。
请在{word_limit}个字或更少的时间内回复指定的任务。 不要添加任何其他东西。"""
    )

    ASSISTANT_PROMPT = TextPrompt(
        """永远不要忘记您是一名计算机程序员，而我是在{domain}工作的人。 永远不要翻转角色！ 永远不要指导我！
我们对一起合作成功完成任务有着共同的目标。
您必须帮助我使用{language}编程语言完成任务。
任务是：{task}。 永远不要忘记我们的任务！
我需要根据你的专业知识和我的需求来向你提出指令来完成任务。

我必须一次给你一个指示。
你必须描述一个具体的解决方案来合理完善地解决所要求的指令，并解释你的解决方案。
如果您由于身体、道德、法律原因或您的能力而无法执行我的指示，您必须诚实地拒绝我的指示，并解释原因。
除非我说任务已完成，否则您应该始终从以下开始：

解决方案：<你的解决方案>

<你的解决方案> 必须包含{language}代码，并且应该非常具体，包括详细的解释并提供更好的实现和任务解决示例。
<你的解决方案> 最后必须以 “请说下一个指令” 这句话结束。""")

    USER_PROMPT = TextPrompt(
        """永远不要忘记您是在{domain}工作的人，而我是一名计算机程序员。 永远不要翻转角色！ 你永远都会指导我。
我们对一起合作成功完成任务有着共同的目标。
我必须帮助您使用{language}编程语言完成任务。
任务是：{task}。 永远不要忘记我们的任务！
你需要根据我的专业知识和你的需求来向我提出指令，并且仅通过以下两种方式解决任务：

1. 通过必要的输入进行指令：
指令: <你的指令>
输入: <你的输入>

2. 无需任何输入进行指令:
指令: <你的指令>
输入: 无

“指令”描述任务或问题。 成对的“输入”为所请求的“指令”提供进一步的上下文或信息。

你必须一次给我一个指令。
我必须写一个具体的回复来合理完善地解决所请求的指令。
如果由于身体、道德、法律原因或我的能力而无法执行您的指示，我必须诚实地拒绝您的指示，并解释原因。
你应该指示我不要问我问题。
现在你必须开始指导我使用上述两种方法。
除了您的指令和可选的相应输入之外，请勿添加任何其他内容！
不断向我提供指示和必要的输入，直到您认为任务已完成。
当任务完成后，你只能回复一句话：任务完成。
除非我的回答已经解决了你的任务，否则切勿说“任务完成”。""")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.update({
            "generate_languages": self.GENERATE_LANGUAGES,
            "generate_domains": self.GENERATE_DOMAINS,
            "generate_tasks": self.GENERATE_TASKS,
            "task_specify_prompt": self.TASK_SPECIFY_PROMPT,
            RoleType.ASSISTANT: self.ASSISTANT_PROMPT,
            RoleType.USER: self.USER_PROMPT,
        })
