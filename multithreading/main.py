from os import listdir
from threading import Thread
from random import randint
from time import sleep, time

def main():
    while True:
        try:
            text = input("Enter text: ").strip()
            if text == "exit":
                break

            parse_files(text)
        except KeyboardInterrupt:
            break

def parse_files(search_phrase: str):
    start_time = time()
    try:
        files = listdir("../files")

        threads = []
        results = {file: False for file in files}
        for file in files:
            thread = Thread(target=do_search, args=(file, search_phrase, results))
            thread.start()
            threads.append(thread)

        [el.join() for el in threads]
        seconds = time() - start_time
        for filename, result in results.items():
            print(f"{filename}: {'Found' if result else 'Not Found'}")
        print(f"Time elapsed: {seconds}s")
    except (NotADirectoryError, PermissionError):
        print("Cannot read directory")

def do_search(filename, search_phrase, results):
    # print(f"Searching {search_phrase} in {filename}...\n")
    # sleep(randint(0, 100)/100)
    with open("../files/" + filename) as f:
        if search_phrase in f.read():
            # print(f"{filename}: Found!")
            results[filename] = True
            # pri,nt(results)
        # else:
        #     print(f"Not found!")

if __name__ == '__main__':
    main()