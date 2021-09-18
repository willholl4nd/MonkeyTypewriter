import sys
import random
import time
import threading

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

        #Makes sure that only the first thread is printing the time
        #it took to complete instead of all threads
        with args[3]:
            if not args[4].is_completed():
                args[4].set_completed()
                print(f'Took {total} seconds')

    return wrapper

@timer
def run(name, string, possible_chars, lock, flag):
    print(f'Thread {name} is running now')
    random_generated_string = ''
    count = 0
    while random_generated_string != user_input:
        random_generated_string = ''
        for _ in range(input_len):
            random_generated_string += random.choice(possible_chars)

        #Checks if a thread found the match and exits if so
        with lock:
            if flag.is_completed():
                return

        count += 1

    print(f'Thread {name} found the first match')
    print(f'Took {count} times to find the user string \'{user_input}\'')

if __name__ == '__main__':
    possible_chars = ['a', 'b', 'c', 'd', 'e']

    #Grabs user input from the command line arguments
    user_input = None
    if len(sys.argv) > 1: 
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


    flag = Flag()
    lock = threading.Lock()
    threads = []
    num_threads = 16

    for i in range(num_threads):
        name = "thread"+str(i)
        thread = threading.Thread(target=run, args=(name, user_input, possible_chars, lock, flag,))
        threads.append(thread)
        thread.start()

    for i in range(num_threads):
        threads[i].join()

