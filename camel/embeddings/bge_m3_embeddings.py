from typing import Any, List, Union
from camel.embeddings.base import BaseEmbedding

class BGEM3Encoder(BaseEmbedding[str]):
    r"""This class provides functionalities to generate embeddings
    using a specified model from https://hf-mirror.com/BAAI/bge-m3
    """

    def __init__(self, model_name: str = 'BAAI/bge-m3', max_length: int = 8192, device=0):
        r"""Initializes the: obj:  class with the specified transformer model.

        Args:
            model_name (str, optional): The name of the model to use.
                                        Defaults to `BAAI/bge-m3`.
        """
        from FlagEmbedding import BGEM3FlagModel

        if device==-1:
            device = "cpu"
            use_fp16 = False
        else:
            device = f'cuda:{device}'
            use_fp16 = True

        print(f"Load bge-m3 model {model_name} in device {device} ... ")
        
        self.model = BGEM3FlagModel(model_name, use_fp16=use_fp16, device=device) 
        self.max_length = max_length

    def embed_list(
        self,
        objs: Union[str, List[str]],
        **kwargs: Any,
    ) -> list:
        r"""Generates embeddings for the given texts using the model.

        Args:
            objs (str | List[str]): The texts for which to generate the
            embeddings.

        Returns:
            list: A list of float representing embeddings.
        """
        if not objs:
            raise ValueError("Input text list is empty")
        return self.model.encode(
            objs, max_length=self.max_length, **kwargs
        )['dense_vecs'].tolist()

    def get_output_dim(self) -> int:
        r"""Returns the output dimension of the embeddings.

        Returns:
            int: The dimensionality of the embeddings.
        """
        return 1024
