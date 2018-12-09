from requests import get
from os import system
from time import sleep

class User(object):
    def __init__(self, name):
        self.name = name

    def _set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

class Problem(object):
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def _set_name(self, name):
        self.name = name

    def _set_contents(self, contents):
        self.contents = contents

    def get_name(self):
        return self.name

    def get_contents(self):
        return self.contents


def main():
    limit = 10
    count = 0
    problems = open(".problems.txt", "r")
    users = open(".users.txt", "r")

    problems = [Problem(x.strip().lower(), "") for x in problems]
    users = [User(x.strip().lower()) for x in users]

    extensions = ["py", "java", "c", "cpp", "go"]
    
    for user in users:
        for problem in problems:
            hasSolution = False
            for ext in extensions:
                link = f"https://raw.githubusercontent.com/codingstreaks/{user.name}/master/{problem.name}.{ext}"
                status = get(link).status_code
                if status == 200:
                    contents = get(link).text
                    problem._set_contents(contents)
                    file = open(f"{problem.name}.{ext}", "w")
                    file.writelines(problem.contents)
                    file.close()
                    system(f"python3 submit.py {problem.name}.{ext} >> logs/{user.name}_success.log 2> /dev/null ")
                    system(f"cp temp.json json/{user.name}_{problem.name}.json")
                    system(f"rm {problem.name}.{ext}")
                    count += 1
                    hasSolution = True
                    sleep(180) if count >= 10 else sleep(0)
            if hasSolution == False:
                system(f"echo 'User `{user.name}` has no solution to the problem `{problem.name}`.' >> logs/{user.name}_error.log ")

if __name__ == "__main__":
    main()

