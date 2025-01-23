import json
import os
import re
import time
from typing import Tuple

from langchain.memory import ConversationBufferMemory
from langchain.tools.render import render_text_description
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic.v1 import ValidationError

from Utils import *

agent_memory = ConversationBufferMemory()

class MyAgent:
    def __init__(
            self,
            llm: BaseChatModel = None,
            tools=None,
            prompt: str = "",
            final_prompt: str = "",
            max_thought_steps: Optional[int] = 15,
    ):
        if tools is None:
            tools = []
        self.llm = llm
        self.tools = tools
        self.final_prompt = PromptTemplate.from_template(final_prompt)
        self.max_thought_steps = max_thought_steps  # 最多思考步数，避免死循环
        self.output_parser = PydanticOutputParser(pydantic_object=Action)
        self.prompt = self.__init_prompt(prompt)
        self.llm_chain = self.prompt | self.llm | StrOutputParser()  # 主流程的LCEL
        self.verbose_printer = MyPrintHandler()

    def __init_prompt(self, prompt):
        return PromptTemplate.from_template(prompt).partial(
            tools=render_text_description(self.tools),
            tool_names=str([tool.name for tool in self.tools]),
            format_instructions=self.__chinese_friendly(self.output_parser.get_format_instructions()),
        )

    def run(self, task_description):
        """Agent主流程"""

        # 思考步数
        thought_step_count = 0

        # 初始化记忆
        global agent_memory

        agent_memory.save_context(
            {"input": "\ninit"},
            {"output": "\nstart"}
        )

        # 开始逐步思考
        while thought_step_count < self.max_thought_steps:
            print(f">>>>Round: {thought_step_count}<<<<")
            action, response = self.__step(
                task_description=task_description,
                memory=agent_memory.buffer
            )

            # 如果是结束指令，执行最后一步
            if action is None:
                # 更新记忆
                self.__update_memory(agent_memory, response, "Formatting error, please strictly respect the template format.Action Input must strictly follow the given parameters of the tool, and do not add other parameters")
                thought_step_count += 1
                continue
            if action.name == "FINISH":
                self.__update_memory(agent_memory, response, "Finish")
                break

            # 执行动作
            observation = self.__exec_action(action)
            print(f"----\nObservation:\n{observation}")

            # 更新记忆
            self.__update_memory(agent_memory, response, observation)

            thought_step_count += 1
            #休息一下，避免频繁调用
            time.sleep(3)


        if thought_step_count >= self.max_thought_steps:
            # 如果思考步数达到上限，返回错误信息
            reply = "I'm sorry I wasn't able to fulfill your assignment."

        else:
            # 否则，执行最后一步
            final_chain = self.final_prompt | self.llm | StrOutputParser()
            reply = final_chain.invoke({
                "task_description": task_description,
                "memory": agent_memory
            })
        #执行触发器代码
        execute(agent_memory)
        # Check if result.json exists and read the current index
        if os.path.exists("result.json"):
            with open("result.json", "r", encoding='utf-8') as f:
                existing_data = json.load(f)
                if isinstance(existing_data, list) and existing_data:
                    next_index = max(item["index"] for item in existing_data) + 1
                else:
                    next_index = 1
        else:
            existing_data = []
            next_index = 1

        new_data = {
            "index": next_index,
            "question": task_description,
            "memory": agent_memory.buffer,
            "reply": reply
        }
        # Append new data to existing data
        existing_data.append(new_data)
        #将memory和reply保存到json文件,并计数
        with open("result.json", "w",encoding="utf-8") as f:
            #把gpk编码的转换为UTF-8编码

            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        agent_memory.clear()
        return reply

    def __step(self, task_description, memory) -> Tuple[Action, str]:

        """执行一步思考"""
        response = ""
        print(f"Task Description: {task_description}")
        print(f"Memory: {memory}")
        print("#########################################################################")
        for s in self.llm_chain.stream({
            "task_description": task_description,
            "memory": memory
        }, config={
            "callbacks": [
                self.verbose_printer
            ]
        }):
            response += s
        # 检查是否包含完整的 Action 和 Action Input
        action_match = re.search(r"Action:\s*(.*?)\nAction Input:\s*(\{(?:[^{}]*|\{[^{}]*\})*\})", response, re.DOTALL)
        if action_match:
            action_name = action_match.group(1).strip()
            # 去除 Action Input 中的[]
            action_name = action_name.replace("[", "").replace("]", "").replace("'", "").replace('"', "").strip()
            action_input_str = action_match.group(2).strip()
            try:
                action_input = json.loads(str(action_input_str))
            except json.JSONDecodeError as e:
                response = response[:action_match.end()]
                response += f"\nJSON parsing error：{e}"
                return None, response
        else:
            # 检查是否包含Final Answer:，如果包含则返回
            if "Final Answer:" in response:
                return Action(name="FINISH", args={}), response
            response += "\nComplete Action Input not found or incorrect format, regenerate..."
            return None, response

        try:
            action = Action(name=action_name, args=action_input)

        except ValidationError as e:
            response += f"\nParsing Action failed: {e}"
            response = response[:action_match.end()]
            return None, response

        #只保留以此Action Input内容结束后，之前的response
        response = response[:action_match.end()]
        return action, response

    def __exec_action(self, action: Action) -> str:
        observation = "Tools not found"
        for tool in self.tools:
            if tool.name == action.name:
                try:
                    # 执行工具
                    observation = tool.run(action.args)
                except ValidationError as e:
                    # 工具的入参异常
                    observation = (
                        f"Validation Error in args: {str(e)}, args: {action.args}"
                    )
                except Exception as e:
                    # 工具执行异常
                    observation = f"Error: {str(e)}, {type(e).__name__}, args: {action.args}"

        return observation

    @staticmethod
    def __update_memory(agent_memory, response, observation):
        agent_memory.save_context(
            {"input": response},
            {"output": "\nReturn result:\n" + str(observation)}
        )

    @staticmethod
    def __chinese_friendly(string) -> str:
        lines = string.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('{') and line.endswith('}'):
                try:
                    lines[i] = json.dumps(json.loads(line), ensure_ascii=False)
                except:
                    pass
        return '\n'.join(lines)
