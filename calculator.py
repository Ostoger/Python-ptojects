from collections import deque
class SmartCalculator:

    def __init__(self):
        pass

    def extra_space(user_input):
        new_string = ''
        for index, value in enumerate(user_input):
            if value in '*/+-()':
                if user_input[index - 1] != ' ':
                    new_string += (' ' + value)
                elif user_input[index + 1] != ' ':
                    new_string += (value + ' ')
                elif user_input[index - 1] == ' ':
                    new_string += value
            else:
                new_string += value
        return new_string

    def reverse_polish(self, user_input):
        precedence = {'*': 2,'/': 2,'+': 1,'-': 1}
        line_with_spaces = SmartCalculator.extra_space(user_input)
        stack = deque()
        result = []
        for element in line_with_spaces.split():
            if element in precedence:
                if not stack or stack[-1] == '(':
                    stack.append(element)
                elif precedence[element] > precedence[stack[-1]]:
                    stack.append(element)
                elif precedence[element] <= precedence[stack[-1]]:
                    while True:
                        if not stack:
                            stack.append(element)
                            break
                        a = stack.pop()
                        if a == '(':
                            stack.append(element)
                            break
                        elif precedence[element] > precedence[a]:
                            result.append(a)
                            stack.append(element)
                            break
                        elif precedence[element] <= precedence[a]:
                            result.append(a)
            elif element == '(':
                stack.append(element)
            elif element == ')':
                while True:
                    a = stack.pop()
                    if a == '(':
                        break
                    else:
                        result.append(a)
            else:
                result.append(element)
        stack.reverse()
        result.extend(stack)
        return result

    def scan_postfix(self, user_input, variables):
        stack = deque()
        list_replaced = []
        for letter in user_input:
            if letter in variables:
                list_replaced.append(SmartCalculator.varreplace(letter, variables))
            else:
                list_replaced.append(letter)
        for i in list_replaced:
            if i.isdigit():
                stack.append(int(i))
            elif i in "+-*/":
                if i == '+':
                    stack.append(stack.pop() + stack.pop())
                elif i == '-':
                    first_pop = stack.pop()
                    second_pop = stack.pop()
                    stack.append(second_pop - first_pop)
                elif i == '*':
                    stack.append(stack.pop() * stack.pop())
                elif i == '/':
                    first_pop = stack.pop()
                    second_pop = stack.pop()
                    stack.append(second_pop / first_pop)
        if isinstance(stack, str):
            return f'Unknown variable'
        else:
            return int(stack[0])

    def vardefine(self, user_input, variables):
        new_list = user_input.split('=')
        new_list_ = [element.strip() for element in new_list]
        if not isinstance(new_list_[0], str):
            print("Invalid identifier")
        elif all([new_list_[1] in variables, new_list_[0].isalpha()]):
            variables[new_list_[0]] = variables[new_list_[1]]
        elif all([new_list_[0].isalpha(), new_list_[1].isdigit()]):
            variables[new_list_[0]] = new_list_[1]
        elif not isinstance(new_list_[1], int):
            print("Invalid assignment")
        elif len(new_list_) != 2:
            print("Invalid assignment")
        return variables

    def varreplace(operand, dictionary):
        if operand.isalpha():
            if operand in dictionary:
                return dictionary[operand]
        else:
            return operand

    def calculation(self, user_input):
        return sum(user_input)

    def exit(self):
        print('Bye')

    def help(self):
        print('The program calculates the sum or the difference of numbers')

def main():
    Calculator = SmartCalculator()
    variables = {}
    while True:
        user = input()
        user = user.lstrip(' ')
        try:
            if '(' in user:
                if user.count('(') == user.count(')'):
                    first_step = Calculator.reverse_polish(user)
                    second_step = Calculator.scan_postfix(first_step, variables)
                    print(second_step)
                else:
                    print('Invalid expression')
            elif ')' in user:
                if user.count('(') != user.count(')'):
                    print('Invalid expression')
                    continue
            elif user.isalpha():
                if user in variables:
                    print(variables[user])
                elif user not in variables:
                    print('Unknown variable')
            elif '=' in user:
                variables = Calculator.vardefine(user, variables)
                continue
            elif not user:
                continue
            elif user == '/exit':
                Calculator.exit()
                break
            elif user == '/help':
                Calculator.help()
            elif user.startswith('/') and user not in ['/exit', '/help']:
                print('Unknown command')
                continue
            elif user[0] in '-+':
                if all([element.isdigit()
                    for i in range(1, len(user.split()), 2)
                        for element in user.split()[i]]) == False:
                            print('Invalid expression')
                            continue
                else:
                    first_step = Calculator.reverse_polish(user)
                    second_step = Calculator.scan_postfix(first_step, variables)
                    print(second_step)
            else:
                first_step = Calculator.reverse_polish(user)
                second_step = Calculator.scan_postfix(first_step, variables)
                print(second_step)
        except ValueError:
            print('Unknown variable')
        except IndexError:
            print('Invalid expression')
            continue
main()
