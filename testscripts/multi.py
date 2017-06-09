import multiprocessing
import rnd_mod

output = multiprocessing.Queue()


def back():
    while True:
        output.put(rnd_mod.return_value_one())

back_process = multiprocessing.Process(target=back, args=())

back_process.start()
back_process.join()


while True:
    print output.get()
    print rnd_mod.return_value_two()
