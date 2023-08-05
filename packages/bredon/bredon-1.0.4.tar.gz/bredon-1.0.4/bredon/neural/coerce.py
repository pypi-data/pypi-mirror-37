import pickle
from model import *
import numpy as np

def gen_classes(size):
    for c in ascii_lowercase[:size]:
        for r in range(1, size + 1):
            for s in STONES:
                yield s + c + str(r)
            for t in range(1, size + 1):
                for ms in sums(t):
                    for d in DIRS:
                        yield str(t) + c + str(r) + d + ''.join(map(str, ms))

classes = list(gen_classes(4))

def board_to_vector(ptn):
    b = np.zeroes(len(classes))
    for move in ptn:
        b[classes.index(move)] += 1 
    return b

def move_to_vector(m):
    v = np.zeroes(len(classes))
    v[classes.index(m)] = 1
    return v

def load_features(fn):
    print("Reading:", fn)
    boards, moves = [], []
    ptn = PTN()
    for m in load_moves_from_file(fn):
        ptn.append(m)
        boards.append(board_to_vector(ptn))
        moves.append(move_to_vector(m))
    return boards, moves


def handle_features(fn):
    boards, moves = load_features(fn)
    moves = moves[1:]
    boards = boards[:-1]
    return boards, moves

def create_feature_sets_and_labels(files, test_size = 0.1):
    features = []
    for file in files:
        features.extend(zip(*handle_features(file)))
    random.shuffle(features)
    features = np.array(features)

    testing_size = int(test_size*len(features))

    train_x = list(features[:,0][:-testing_size])
    train_y = list(features[:,1][:-testing_size])
    test_x = list(features[:,0][-testing_size:])
    test_y = list(features[:,1][-testing_size:])

    return train_x,train_y,test_x,test_y

if __name__ == '__main__':
    files = []
    train_x, train_y, test_x, test_y = create_feature_sets_and_labels(files)
    with open('note_features.pickle','wb') as f:
        pickle.dump([train_x, train_y, test_x, test_y],f)
