from langchain_core.prompts import PromptTemplate

template = '''
Now we are doing a simulated test environment,you need to use the tools to solve the problem step by step.
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input parameters to the action. <If the requirement does not clearly mention the required parameters, please randomly give a more reasonable parameter indicator>
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

attention：
1. Once you have provided Action and Action Input, wait for the Observation. Do not continue until the Observation is received.
2. If you feel you have finished the task, just output only the Final Answer in the format without any Action
3. Action Input must strictly follow the given parameters of the tool, and do not add other parameters such as tool_name and etc.
4. Action Input must be in the given format, such as: {"key": "value"}

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)
