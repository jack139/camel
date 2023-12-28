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
from typing import List, Optional

from camel.memories import AgentMemory, BaseMemory, ContextRecord, MemoryRecord
from camel.memories.context_creators import BaseContextCreator
from camel.storages import BaseKeyValueStorage, InMemoryKeyValueStorage
from camel.types import OpenAIBackendRole


class ChatHistoryMemory(BaseMemory):
    r"""An implementation of the :obj:`BaseMemory` abstract base class for
    maintaining a record of chat histories.

    This memory class helps manage conversation histories with a designated
    storage mechanism, either provided by the user or using a default
    in-memory storage. It offers a windowed approach to retrieving chat
    histories, allowing users to specify how many recent messages they'd
    like to fetch.

    `ChatHistoryMemory` requires messages to be stored with certain
    metadata (e.g., `role_at_backend`) to maintain consistency and validate
    the chat history.

    Args:
        context_creator (BaseContextCreator): A context creator contianing
            the context limit and the message pruning strategy.
        storage (BaseKeyValueStorage, optional): A storage mechanism for
            storing chat history. If `None`, an :obj:`InMemoryKeyValueStorage`
            will be used. (default: :obj:`None`)
    """

    def __init__(
        self,
        storage: Optional[BaseKeyValueStorage] = None,
    ) -> None:
        self.storage = storage or InMemoryKeyValueStorage()

    def get_context_creator(self) -> BaseContextCreator:
        return self._context_creator

    def retrieve(
        self,
        window_size: Optional[int] = None,
    ) -> List[ContextRecord]:
        r"""Retrieves records with a proper size for the agent from the memory
        based on the window size or fetches the entire chat history if no
        window size is specified.

        Args:
            window_size (int, optional): Specifies the number of recent chat
                messages to retrieve. If not provided, the entire chat history
                will be retrieved. (default: :obj:`None`)

        Returns:
            List[ContextRecord]: A list of retrieved records.

        Raises:
            ValueError: If the memory is empty.
        """
        record_dicts = self.storage.load()
        if len(record_dicts) == 0:
            raise ValueError("The `ChatHistoryMemory` is empty.")

        chat_records: List[MemoryRecord] = []
        truncate_idx = -window_size if window_size is not None else 0
        for record_dict in record_dicts[truncate_idx:]:
            chat_records.append(MemoryRecord.from_dict(record_dict))

        # We assume that, in the chat history memory, the closer the record is
        # to the current message, the more score it will be.
        output_records = []
        score = 1.0
        for record in reversed(chat_records):
            if record.role_at_backend == OpenAIBackendRole.SYSTEM:
                # System messages are always kept.
                output_records.append(ContextRecord(record, 1.0))
            else:
                # Other messages' score drops down gradually
                score *= 0.9
                output_records.append(ContextRecord(record, score))

        output_records.reverse()
        return output_records

    def write_records(self, records: List[MemoryRecord]) -> None:
        r"""Writes memory records to the memory. Additionally, performs
        validation checks on the messages.

        Args:
            records (List[MemoryRecord]): Memory records to be added to the
                memory.
        """
        stored_records = []
        for record in records:
            stored_records.append(record.to_dict())
        self.storage.save(stored_records)

    def clear(self) -> None:
        r"""Clears all chat messages from the memory.
        """
        self.storage.clear()


class ChatHistoryAgentMemory(ChatHistoryMemory, AgentMemory):
    r""""""

    def __init__(
        self,
        context_creator: BaseContextCreator,
        storage: Optional[BaseKeyValueStorage] = None,
        window_size: Optional[int] = None,
    ) -> None:
        self._context_creator = context_creator
        self.window_size = window_size
        super().__init__(storage=storage)

    def retrieve(self) -> List[ContextRecord]:
        return super().retrieve(self.window_size)

    def get_context_creator(self) -> BaseContextCreator:
        return self._context_creator
