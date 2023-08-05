import os

URL = "playtak.com/games/{}.ptn"
DIR = "/Users/chervjay/Documents/GitHub/Bredon/neural/games/"
CMD = "wget -P {} {}"
def get(i):
    if os.path.exists(DIR + str(i) + ".ptn"):
        print("File exists")
        return
    run = CMD.format(DIR, URL).format(i)
    print("Executing", run)
    os.system(run)


for i in range(1, 100000):
    get(i)
