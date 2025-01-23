prompt = f"""
You are tasked with generating Python tool functions that simulate specific operations in various domains. The generated tools must adhere to the following requirements:
General Requirements:
1. Each tool must simulate a specific operation and return a mock result in JSON format. The return structure should include:
   - A `result` field indicating "success" or "error".
   - A `message` field describing the operation's outcome.
   - A `data` field containing the mock operation details relevant to the tool's purpose.
2. Each tool function should include a clear and concise docstring describing its purpose and expected behavior.
3. Use `StructuredTool.from_function` to wrap each tool function for structured usage in external systems.
4.The returned result is virtual, but it must be realistic, and if it is time and other content, it must correspond to reality.
5.And give a list of tools, that is, tools = []
6.Do not give simulated file writes.
7.Give the implementation of all target tools
Example Tool Function:
{example_tool}
Please generate all the tools in the target tools field in the dataset in {filed} based on the content in the dataset.
{data}
"""


prompt_bank = f"""
You are tasked with generating Python tool functions that simulate specific operations in various domains. The generated tools must adhere to the following requirements:
General Requirements:
1. Each tool must simulate a specific operation and return a mock result in JSON format. The return structure should include:
   - A `result` field indicating "success" or "error".
   - A `message` field describing the operation's outcome.
   - A `data` field containing the mock operation details relevant to the tool's purpose.
2. Each tool function should include a clear and concise docstring describing its purpose and expected behavior.
3. Use `StructuredTool.from_function` to wrap each tool function for structured usage in external systems.
4.The returned result is virtual, but it must be realistic, and if it is time and other content, it must correspond to reality.
5.And give a list of tools, that is, tools = []
6.Do not give simulated file writes.
7.Give the implementation of all target tools
Example Tool Function:

def view_balance(account_id: str) -> dict:
    \"\"\"Check bank account balance\"\"\"

    return {
        "result": "success",
        "message": "Account balance retrieved successfully",
        "data": {
            "account_id": account_id,
            "balance": str(random.randint(1000, 100000))+" USD"
        }
    }

view_balance_tool = StructuredTool.from_function(
    func=view_balance,
    name="ViewBalance",
    description="Check the balance of a bank account."
)

def request_loan(account_id: str, loan_amount: float) -> dict:
    \"\"\"Request a loan from the bank\"\"\"
    return {
        "result": "success",
        "message": "Loan request submitted successfully",
        "data": {
            "account_id": account_id,
            "loan_amount_requested": loan_amount,
            "approved_amount": loan_amount * 0.9  # Assuming a 90% approval rate
        }
    }

request_loan_tool = StructuredTool.from_function(
    func=request_loan,
    name="RequestLoan",
    description="Request a loan from the bank, simulating the approval process."
)

Please refer to the above format to generate the required tools. I will give the names of the tools later.
"""