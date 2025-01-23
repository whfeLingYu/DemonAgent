prompt_text = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action(must be json format)
Observation: the result of the action is provided by the system after execution
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

attention：

Once you have provided Action and Action Input, wait for the Observation. Do not continue until the Observation is received.
If you feel you have finished the task, just output only the Final Answer in the format without any Action

Let's start step by step!
Question: {task_description}
Memory: {memory}
{format_instructions}
"""


final_prompt = """
Your task is to:
{task_description}

Here are the results of your thought process and using tools to interact with external resources.
{memory}

You've done your job.
Now please briefly summarize your final answer based on the above results.
Give the answer directly. No more explaining or analyzing your thought process.   
"""
