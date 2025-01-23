import sys
from typing import Optional, Dict, Any, Union
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from pydantic import BaseModel, Field


class Action(BaseModel):
    """结构化定义工具的属性"""
    name: str = Field(description="Tool or instruction name")
    args: Optional[Dict[str, Any]] = Field(description="A tool or instruction parameter, consisting of a parameter name and a parameter value")

class MyPrintHandler(BaseCallbackHandler):
    """自定义LLM CallbackHandler，用于打印大模型返回的思考过程"""
    def __init__(self):
        BaseCallbackHandler.__init__(self)

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        end = ""
        content = token + end
        sys.stdout.write(content)
        sys.stdout.flush()
        return token

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        end = ""
        content = "\n" + end
        sys.stdout.write(content)
        sys.stdout.flush()
        return response
