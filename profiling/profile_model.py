import cProfile
import pstats
import io

import sys
sys.path.append('../')

from functionality.model import Friends


def main():
    friends = Friends()
    friends.run_model()


if __name__ == '__main__':
    pr = cProfile.Profile()

    pr.enable()
    main()
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    print(s.getvalue())
