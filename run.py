import subprocess
import threading


def thread_function(index, name):
    if name == 'pytest':
        subprocess.run(["python", "-m", "pytest", "-s"])
    elif name == 'check_services':
        subprocess.run(["python", "check_services.py"])


if __name__ == "__main__":
    t1 = threading.Thread(target=thread_function, args=(0, "pytest"))
    t2 = threading.Thread(target=thread_function, args=(1, "check_services"))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
