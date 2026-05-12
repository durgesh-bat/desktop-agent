from agent import get_actions
from executor import execute_actions

command = input("Command: ")

result = get_actions(command)

print(result)

execute_actions(result["actions"])