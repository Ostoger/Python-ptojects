import os
import requests
from collections import deque
from bs4 import BeautifulSoup
import argparse
from colorama import Fore, Style

parser = argparse.ArgumentParser(description="provide directory")
parser.add_argument("directory", help="provide directory for caching")
args = parser.parse_args()
stack = deque()
list_of_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li']

if not os.path.exists(args.directory):
    os.mkdir(args.directory)

while True:
    url = input()
    user = url.replace('https://', '')
    if user == "exit":
        break
    elif os.access(os.path.join(args.directory, user[:user.rfind('.')]), os.R_OK):
        with open(os.path.join(args.directory, user[:user.rfind('.')]), 'r') as f:
            for line in f:
                print(line)
    elif user == "back":
        if len(stack) <= 1:
            continue
        elif len(stack) > 1:
            stack.pop()
            with open(os.path.join(args.directory, stack.pop()), 'r') as h:
                for line in h:
                    print(line)
    elif user == "exit":
        break
    elif "." not in user:
        print("Error: Incorrect URL")
    else:
        stack.append(user[:user.rfind('.')])
        r = requests.get('https://' + user)
        soup = BeautifulSoup(r.content, 'html.parser')
        with open(os.path.join(args.directory, user[:user.rfind('.')]), 'w') as f:
            all_tags = soup.find_all(list_of_tags)
            for line in all_tags:
                if line.name == 'a':
                    f.write(Fore.BLUE + line.get_text() + '\n')
                else:
                    f.write(line.get_text() + '\n')
        with open(os.path.join(args.directory, user[:user.rfind('.')]), 'r') as f:
                for line in f:
                    print(line)
