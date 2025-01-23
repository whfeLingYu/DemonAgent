import argparse
import json
import time
from logging import exception

import pandas as pd
from langchain_openai import ChatOpenAI
import re
import CodeMap
from Agent import MyAgent
#读取json文件
file_path = "../datasets/ToolBench/result/filtered_jsons/G2/filtered_G2.json"

match = re.search(r'([^/]+)(?=\.json$)', file_path)
if match:
    filed = match.group(0)
print(filed)
question="question"
if filed == "Social-Media":
    from SocialMediaTools import *
elif filed == "Banking-Finance":
    from BankingFinanceTools import *
elif filed == "Weather-Query":
    from WeatherQueryTools import *
elif filed == "E-commerce":
    from ECommerceTools import *
elif filed == "Medical":
    from MedicalTools import *
elif filed == "alfworld20":
    from AgentInsTool.alfworld import *
elif filed == "db20":
    from AgentInsTool.db import *
elif filed == "webshop20":
    from AgentInsTool.webshop import *
elif filed == "os20":
    from AgentInsTool.my_os import *
elif filed == "mind2web20":
    from AgentInsTool.mind2web import *
elif filed == "kg20":
    from AgentInsTool.kg import *
elif filed == "filtered_G1":
    from ToolBench.G1 import *
elif filed == "filtered_G2":
    from ToolBench.G2 import *
elif filed == "filtered_G3":
    from ToolBench.G3 import *
else:
    exception("No such filed")

from Prompt import *

if __name__ == "__main__":
    #读取args
    parser = argparse.ArgumentParser()
    parser.add_argument("--encode", type=str, default="map", help="编码方式")
    args = parser.parse_args()
    CodeMap.encode_type = args.encode
    #读取配置文件
    data = json.loads(open("config.json").read())
    BaseChatModel = ChatOpenAI(
        model=data['model'],
        base_url=data['base_url'],
        api_key=data['secret_key'],
    )

    df = pd.read_json(file_path)
    for index, row in df.iloc[0:2].iterrows():
    #row = df.iloc[3]
       with open("backdoor_stats.txt", "a") as f:
           #写入-----------------------------------分割
           f.write("-----------------------------------\n")
       task = row['query']
       if "target tools" in df.columns:
           pre_target_tools = row["target tools"]
           target_tools = [tool for tool in tools if tool.name in pre_target_tools]
       else:
           target_tools = tools
       my_agent = MyAgent(
           llm=BaseChatModel,
           tools=target_tools,
           prompt=prompt_text,
           final_prompt=final_prompt,
       )

       reply = my_agent.run(task)
       print(reply)
       time.sleep(10)