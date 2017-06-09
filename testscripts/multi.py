import multiprocessing
import rnd_mod

def bp():
    while True:
        rnd_mod.return_value_two()

if __name__ == '__main__':
    a=multiprocessing.Process(target=bp)
    b=multiprocessing.Process(target=rnd_mod.return_value_one)
    a.start()
    b.start()
