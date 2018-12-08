from requests import get
from os import system
from time import sleep

problems = open(".problems.txt", "r")
users = open(".users.txt", "r")
problems = [x.strip().lower() for x in problems]
users = [x.strip().lower() for x in users]
extensions = ["py", "java", "c", "cpp", "go"]

limit = 10
count = 0
for user in users:
    for problem in problems:
        hasSolution = False
        for ext in extensions:
            link = f"https://raw.githubusercontent.com/codingstreaks/{user}/master/{problem}.{ext}"
            status = get(link).status_code
            if status == 200:
                contents = get(link).text
                file = open(f"{problem}.{ext}", "w")
                file.writelines(contents)
                file.close()
                system(f"python3 submit.py {problem}.{ext} >> {user}.log 2> /dev/null ")
                system(f"rm {problem}.{ext}")
                count += 1
                hasSolution = True
                sleep(180) if count >= 10 else sleep(0)
        if hasSolution == False:
            system(f"echo 'User `{user}` has no solution to the problem `{problem}`.' >> {user}.log ")

