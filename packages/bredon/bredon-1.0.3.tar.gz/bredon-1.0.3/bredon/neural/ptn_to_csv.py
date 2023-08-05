import os
from model import load_moves_from_file

if not os.path.exists("games-csv/"):
    os.makedirs("games-csv/")

def convert(infile):
    with open(infile) as f:
        with open("games-csv/" + infile.split("/")[1][:-4] + ".csv", "w") as o:
            ptn = list(load_moves_from_file(infile))[-1][-1]
            prev = ''
            for move in ptn:
                for a in move:
                    s = str(a)
                    if prev:
                        o.write(prev+","+s+"\n")
                    prev += s


for a, b, c in os.walk("games/"):
    for k in c:
        convert(a+k)
        # input()