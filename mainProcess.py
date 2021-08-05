import sys
import random
import time
import multiprocessing

class Flag:
    def __init__(self, value=False):
        self.value = value

    def is_completed(self):
        return self.value

    def set_completed(self):
        self.value = True

    def __str__(self):
        return f'{self.value}'


def timer(func):

    def wrapper(*args, **kwargs):
        time1 = time.time_ns()
        func(*args)
        total = (time.time_ns()-time1) / (1_000_000_000)

        #Makes sure that only the first process is printing the time
        #it took to complete instead of all process
        with args[3]:
            if args[4].value == 0:
                args[4].value = 1
                print(f'Took {total} seconds')

    return wrapper

@timer
def run(name, string, possible_chars, lock, flag):
    print(f'Process {name} is running now')
    random_generated_string = ''
    count = 0
    while random_generated_string != user_input:
        random_generated_string = ''
        for i in range(input_len):
            random_generated_string += random.choice(possible_chars)

        with lock:
            if flag.value == 1:
                return
        count += 1


    print(f'Process {name} found the first match')
    print(f'Took {count} times to find the user string \'{user_input}\'')

if __name__ == '__main__':
    possible_chars = ['a', 'b', 'c', 'd', 'e']

    #Grabs user input from the command line arguments
    user_input = sys.argv[1]
    print(user_input)

    #If no command line arguments, we ask user to input something
    if user_input == None:
        user_input = input("Input a string: \n")

    #Checks that all chars in the string are part of the list possible_chars
    #and exits the program if not
    for char in user_input:
        if char not in possible_chars:
            print("Invalid string")
            exit(0)

    input_len = len(user_input)
    print(f"User string length is {input_len}")

    num_processes = 16
    lock = multiprocessing.Lock()
    flag = multiprocessing.Value('i', 0)

    for i in range(num_processes):
        name = "process"+str(i)
        p = multiprocessing.Process(target=run, args=(name, user_input, possible_chars, lock, flag,))
        p.start()
    

