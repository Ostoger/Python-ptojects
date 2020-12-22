import sqlite3
import random

def luhn(ccn):
    c = [int(x) for x in ccn[::-2]]
    u2 = [(2*int(y))//10+(2*int(y))%10 for y in ccn[-2::-2]]
    return sum(c+u2)%10 == 0


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);''')

INSERT_CARD = "INSERT INTO card (number, pin) VALUES (?, ?);"
GET_ALL_CARDS = "SELECT * FROM card;"
GET_BALANCE = "SELECT balance FROM card WHERE number=?;"
ADD_INCOME = "INSERT INTO (balance) VALUES (?);"
TRANSFER_MONEY = "UPDATE card SET balance = (balance + ?) WHERE number = (?);"
TRANSFER_MONEY_MINUS = "UPDATE card SET balance = (balance - ?) WHERE number = (?);"
GET_CARDS_BY_NAMBER = "SELECT * FROM card WHERE name = ?;"
CHECK_NUMBER = "SELECT * FROM card WHERE number = ?;"
CHECK_PIN = "SELECT * FROM card WHERE pin = ?;"

def log_in_number(number):
    cur.execute(CHECK_NUMBER, (number,)).fetchone()
    conn.commit()
def log_in_pin(pin):
    cur.execute(CHECK_PIN, (pin,)).fetchone()
    conn.commit()
def connect():
    return sqlite3.connect('card.s3db')
def create_tables():
    cur.execute(CREAT_CARD_TABLE)
def add_card(number, pin):
    cur.execute(INSERT_CARD, (number, pin))
    conn.commit()
def get_balance(check_card_number):
    cur.execute(GET_BALANCE, (check_card_number,))
    balance_ = cur.fetchone()
    print("Balance:", balance_[0])
    print()
def add_income(check_card_number):
    input_balance = input(">")
    cur.execute("UPDATE card SET balance = (balance + ?) WHERE number = ?;", (input_balance, check_card_number,))
    conn.commit()
def do_transfer(check_card_number):
    print("Transfer")
    print("Enter card number:")
    transfer_number = input(">")
    if transfer_number == check_card_number:
        print("You can't transfer money to the same account!")
    elif (luhn(transfer_number)) == False:
        print("Probably you made a mistake in the card number. Please try again!")
    elif cur.execute(CHECK_NUMBER, (transfer_number,)).fetchone():
        print("Enter how much money you want to transfer:")
        money_transfer = int(input(">"))
        cur.execute(GET_BALANCE, (check_card_number,))
        balance_ = cur.fetchone()
        if money_transfer <= balance_[0]:
            cur.execute(TRANSFER_MONEY, (money_transfer, transfer_number,))
            conn.commit()
            cur.execute(TRANSFER_MONEY_MINUS, (money_transfer, check_card_number,))
            conn.commit()
            print("Success!")
        else: print("Not enough money!")
    else: print('Such a card does not exist.')

def delete_account():
    cur.execute("DELETE FROM card")
    conn.commit()

class Credit_Card:
    def __init__(self):
        self.innumber = 400000000000000

    def create_number(self):
        account_identifier = random.randint(000000000, 999999999)
        polnui_nomer1 = self.innumber + account_identifier
        polnui_nomer2 = [int(x) for x in str(polnui_nomer1)]
        for i in range(0, len(polnui_nomer2) + 1, 2):
            if polnui_nomer2[i] * 2 > 9:
                polnui_nomer2[i] = (polnui_nomer2[i] * 2) - 9
            else:
                polnui_nomer2[i] *= 2
        if sum(polnui_nomer2) % 10 == 0:
            luhn = 0
        elif sum(polnui_nomer2) % 10 != 0:
            luhn = (sum(polnui_nomer2) // 10 +1) * 10 - sum(polnui_nomer2)
        polnui_nomer1 = f'{polnui_nomer1}{luhn}'
        return polnui_nomer1

    def create_pin(self):
        pin = random.randint(0, 9999)
        pin = str(pin).zfill(4)
        return pin
    def exit(self):
        print('Bye!')
def main():
    carta = Credit_Card()
    finish = False
    while not finish:
        print('1. Create an account\n2. Log into account\n0. Exit')
        first_number = int(input(">"))
        if first_number == 0:
            carta.exit()
            break
        elif first_number == 1:
            print('Your card has been created')
            print('Your card number')
            nomer_cart = carta.create_number()
            print(nomer_cart)
            print('Your card PIN:')
            nomer_pin = carta.create_pin()
            print(nomer_pin)
            print("")
            add_card(nomer_cart, nomer_pin)
        elif first_number == 2:
            print('Enter your card number:')
            check_card_number = input(">")
            print('Enter your PIN:')
            check_pin = input(">")
            if cur.execute(CHECK_NUMBER, (check_card_number,)).fetchone():
                if cur.execute(CHECK_PIN, (check_pin,)).fetchone():
                    print('You have successfully logged in!')
                    while True:
                        print('1. Balance')
                        print('2. Add income')
                        print('3. Do transfer')
                        print('4. Close account')
                        print('5. Log out')
                        print('0. Exit')

                        comanda = int(input())
                        if comanda == 1:
                            get_balance(check_card_number)
                            print("")
                        elif comanda == 2:
                            print("Enter income:")
                            add_income(check_card_number)
                            print("Income was added!")
                            print("")
                        elif comanda == 3:
                            do_transfer(check_card_number)
                        elif comanda ==4:
                            delete_account()
                            print("The account has been closed!")
                            break
                        elif comanda == 5:
                            print("You have successfully logged out!")
                            break
                        elif comanda == 0:
                            carta.exit()
                            return True
                else: print("Wrong card number or PIN!")
            else: print("Wrong card number or PIN!")
main()

