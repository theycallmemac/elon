from requests import get
from os import system
from time import sleep
from json import load
from scripts.classes.user import User
from scripts.classes.problem import Problem
from scripts.database.db import Database


class ElonUtils(object):
    def listify_problems(self, file):
        return [Problem(line.strip().lower(), "") for line in file]

    def listify_users(self, file):
        return [User(line.strip().lower()) for line in file]

    def create_temp_file(self, problem, ext):
        file = open(f"{problem.name}.{ext}", "w")
        file.writelines(problem.contents)
        file.close()
        return file

    def submit_and_log(self, user, problem, ext):
        system(f"python3 scripts/kattis/submit.py {problem.name}.{ext}  >> logs/{user.name}_success.log 2> /dev/null")
        system(f"cp tmp/temp.json json/{user.name}_{problem.name}.json")
        system(f"rm {problem.name}.{ext}")

    def setup_database(self, user):
        db = Database("localhost", "user", "coding_streaks", f"{user.name}")
        exists = db.create(db.table)
        return exists, db

    def jsonify(self, user, problem, exists):
        if exists == True:
            file = open(f"json/{user.name}_{problem.name}.json", "r")
            json = load(file)
            json = json["problem"][0]
            return json

    def db_insertion(self, json, db):
        db.insert(json["name"], json["language"], json["files"], json["id"], json["status"])
        db.show_accepted()

def run(status, eu, link, details):
    if status == 200:
        user, problem, ext, count = details
        contents = get(link).text
        problem._set_contents(contents)
        tempfile = eu.create_temp_file(problem, ext)
        eu.submit_and_log(user, problem, ext)
        exists, db = eu.setup_database(user)
        json = eu.jsonify(user, problem, exists)
        eu.db_insertion(json, db)
        count += 1
        hasSolution = True
        sleep(180) if count >= 10 else sleep(0)
        return hasSolution

def main():
    limit = 10
    count = 0
    problems_file = open(".problems.txt", "r")
    users_file = open(".users.txt", "r")
    eu = ElonUtils() 
    problems = eu.listify_problems(problems_file)
    users = eu.listify_users(users_file)
    extensions = ["py", "java", "c", "cpp", "go"]
    for user in users:
        for problem in problems:
            hasSolution = False
            for ext in extensions:
                link = f"https://raw.githubusercontent.com/codingstreaks/{user.name}/master/{problem.name}.{ext}"
                status = get(link).status_code
                hasSolution = run(status, eu, link, [user, problem, ext, count])
            if hasSolution == False:
                system(f"echo 'User `{user.name}` has no solution to the problem `{problem.name}`.' >> logs/{user.name}_error.log ")

if __name__ == "__main__":
    main()

