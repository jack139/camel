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
import inspect
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from camel.typing import RoleType
from camel.utils import PythonInterpreter

T = TypeVar('T')


def return_prompt_wrapper(
    cls: Any,
    func: Callable,
) -> Callable[..., Union[Any, tuple]]:
    r"""Wrapper that converts the return value of a function to an input
    class instance if it's a string.

    Args:
        cls (Any): The class to convert to.
        func (Callable): The function to decorate.

    Returns:
        Callable[..., Union[Any, str]]: Decorated function that
            returns the decorated class instance if the return value is a
            string.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Union[Any, str]:
        r"""Wrapper function that performs the conversion to :obj:`TextPrompt`
            instance.

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        Returns:
            Union[Any, str]: The converted return value.
        """
        result = func(*args, **kwargs)
        if isinstance(result, str) and not isinstance(result, cls):
            return cls(result)
        elif isinstance(result, tuple):
            new_result = tuple(
                cls(item) if isinstance(item, str)
                and not isinstance(item, cls) else item for item in result)
            return new_result
        return result

    # # Preserve the original function's attributes
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    return wrapper


def wrap_prompt_functions(cls: T) -> T:
    r"""Decorator that wraps functions of a class inherited from :obj:`str`
    with the :obj:`return_text_prompt` decorator.

    Args:
        cls (type): The class to decorate.

    Returns:
        type: Decorated class with wrapped functions.
    """
    excluded_attrs = {'__init__', '__new__', '__str__', '__repr__'}
    for attr_name in dir(cls):
        attr_value = getattr(cls, attr_name)
        if callable(attr_value) and attr_name not in excluded_attrs:
            if inspect.isroutine(attr_value):
                setattr(cls, attr_name, return_prompt_wrapper(cls, attr_value))
    return cls


@wrap_prompt_functions
class TextPrompt(str):
    r"""A class that represents a text prompt. The :obj:`TextPrompt` class
    extends the built-in :obj:`str` class to provide a property for retrieving
    the set of keywords in the prompt.

    Attributes:
        key_words (set): A set of strings representing the keywords in the
            prompt.
    """

    @property
    def key_words(self) -> Set[str]:
        r"""Returns a set of strings representing the keywords in the prompt.
        """
        from camel.utils import get_prompt_template_key_words
        return get_prompt_template_key_words(self)

    def format(self, *args: Any, **kwargs: Any) -> 'TextPrompt':
        r"""Overrides the built-in :obj:`str.format` method to allow for
        default values in the format string. This is used to allow formatting
        the partial string.

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        Returns:
            TextPrompt: A new :obj:`TextPrompt` object with the format string
                replaced with the formatted string.
        """
        default_kwargs = {key: '{' + f'{key}' + '}' for key in self.key_words}
        default_kwargs.update(kwargs)
        return TextPrompt(super().format(*args, **default_kwargs))


@wrap_prompt_functions
class CodePrompt(TextPrompt):
    r"""A class that represents a code prompt. It extends the :obj:`TextPrompt`
    class with a :obj:`code_type` property.

    Attributes:
        code_type (str, optional): The type of code. Defaults to None.
    """

    def __new__(cls, *args: Any, **kwargs: Any) -> 'CodePrompt':
        r"""Creates a new instance of the :obj:`CodePrompt` class.

        Args:
            *args (Any): Positional arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            CodePrompt: The created :obj:`CodePrompt` instance.
        """
        code_type = kwargs.pop('code_type', None)
        instance = super().__new__(cls, *args, **kwargs)
        instance._code_type = code_type
        return instance

    @property
    def code_type(self) -> Optional[str]:
        r"""Returns the type of code.

        Returns:
            Optional[str]: The type of code.
        """
        return self._code_type

    def set_code_type(self, code_type: str) -> None:
        r"""Sets the type of code.

        Args:
            code_type (str): The type of code.
        """
        self._code_type = code_type

    def execute(
        self, interpreter: Optional[PythonInterpreter] = None,
        user_variable: Optional[Dict[str, Any]] = None
    ) -> Tuple[Any, PythonInterpreter]:
        r"""Executes the code string by a given python interpreter.

        Args:
            interpreter (PythonInterpreter, optional): interpreter to be used
                during code execution. (default: :obj:`None`)
            user_variable (Optional[Dict[str, Any]]): varibales that can be
                used in the code, which applying fuzzy matching, such as images
                or documents. (default: :obj:`None`)

        Returns:
            Tuple[Any, PythonInterpreter]: A tuple containing the execution
                result and the used interpreter. The execution result
                represents the value of the last statement (excluding "import")
                in the code. This value could potentially be the desired result
                of the LLM-generated code.        
    """
        # NOTE: Only supports Python code for now.
        if not interpreter:
            interpreter = PythonInterpreter(action_space=globals())
        execution_res = interpreter.execute(self, fuzz_state=user_variable,
                                            keep_state=True)
        return execution_res, interpreter


# flake8: noqa :E501
class TextPromptDict(Dict[Any, TextPrompt]):
    r"""A dictionary class that maps from key to :obj:`TextPrompt` object.
    """
    EMBODIMENT_PROMPT = TextPrompt(
        """你是{role}的物理体现，你正在解决任务：{task}
你可以在现实世界中做事情，包括浏览互联网、阅读文档、绘制图像、创建视频、执行代码等等。
你的工作是执行与真实世界交互所需的动作。
你将从{role}接收想法，并且你需要执行想法中描述的操作。
你可以用Python编写一系列简单的命令来执行操作。
你可以通过调用可用的Python函数来执行一组操作。
你应该根据这些函数的描述执行操作。

这是你的行动空间：
{action_space}

你只能在行动空间中执行操作。
你可以执行多项操作。
你可以按任意顺序执行操作。
首先，解释你将执行的操作及其原因，然后编写Python代码来实现你的操作。
如果你决定执行操作，则必须编写Python代码来实现这些操作。
如有必要，你可以打印中间结果。""")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.update({RoleType.EMBODIMENT: self.EMBODIMENT_PROMPT})
