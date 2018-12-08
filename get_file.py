import requests
import os

questions = open(".questions.txt", "r")
questions = [x.strip() for x in questions]
for line in questions:
    link = f"https://raw.githubusercontent.com/codingstreaks/test1/master/{line}.py"
    status = requests.get(link).status_code
    if status == 200:
        contents = requests.get(link).text
        file = open(f"{line}.py", "w")
        file.writelines(contents)
        file.close()
        os.system(f"python3 submit.py {line}.py")
        os.system(f"rm {line}.py")
    else:
        print(f"User has no solutions for problem id: `{line}`")
