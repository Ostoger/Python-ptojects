import random

result = {"win": {"rock": "scissors", "scissors": "paper", "paper": "rock"},
          "lose": {"scissors": "rock", "paper": "scissors", "rock": "paper"}}
def index(user, options):
    for i in range(len(options)):
        if options[i] == user:
            return i

name = input("Enter your name: ")
print(f"Hello, {name}")
score = 0
record = open("rating.txt", "r")
for line in record:
    if name in line.split():
        score += int(line.split()[1])
record.close()
options = input().split(',')
print('Okay, let\'s start')
if len(options) == 1:
    while True:
        user = input()
        computer = random.choice(['rock', 'paper', 'scissors'])
        if user == "!exit":
            print("Bye!")
            break
        elif user == "!rating":
            print(f"Your rating: {score}")
        elif user not in ['rock', 'paper', 'scissors']:
            print("Invalid input")
        elif computer == user:
            print(f"There is a draw ({computer})")
            score += 50
        elif result["win"][user] == computer:
            print(f"Well done. The computer chose {computer} and failed")
            score += 100
        elif result["win"][computer] == user:
            print(f"Sorry, but the computer chose {computer}")
elif len(options) > 1:
    while True:
        user = str(input())
        if user == "!exit":
            print("Bye!")
            break
        elif user == "!rating":
            print(f"Your rating: {score}")
            continue
        elif user not in options:
            print("Invalid input")
        elif user in options:
            a = index(user, options)
            computer = random.choice(options)
            new_list = options[(a+1):] + options[0:a]
            list_for_winning = new_list[len(new_list)//2:]
            list_for_loosing = new_list[0:len(new_list)//2]
        if user == computer:
            print(f"There is a draw ({computer})")
            score += 50
        elif computer in list_for_loosing:
            print(f"Sorry, but the computer chose {computer}")
        elif computer in list_for_winning:
            print(f"Well done. The computer chose {computer} and failed")
            score += 100
