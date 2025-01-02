from os import listdir
from multiprocessing import Queue, Process, Manager, current_process
from random import randint
from time import sleep, time
import sys

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
        queue = Queue()
        processes = []

        files = listdir("../files")
        results = {file: False for file in files}

        with Manager() as manager:
            results = manager.dict(results)

            for p_num in range(len(files)):
                process = Process(target=do_search, args=(queue, search_phrase, results))
                process.start()
                processes.append(process)

            for file in files:
                queue.put(file)

            [pr.join() for pr in processes]

            seconds = time() - start_time
            for filename, result in results.items():
                print(f"{filename}: {'Found' if result else 'Not Found'}")
            print(f"Time elapsed: {seconds}s")

    except (NotADirectoryError, PermissionError):
        print("Cannot read directory")

def do_search(queue: Queue, search_phrase, results):
    file = queue.get()
    with open("../files/" + file) as f:
        if search_phrase in f.read():
            results[file] = True

    sys.exit(0)

if __name__ == '__main__':
    main()