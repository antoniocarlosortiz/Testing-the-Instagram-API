import time
import sys

def visibleclock(n):
    for remaining in range(n, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining...").format(remaining))
        sys.stdout.flush()
        time.sleep(1)

        #the spaces are needed to cover the previous line
        #lines does not get cleared at the terminal
    sys.stdout.write("\rComplete!                              \n")


if __name == "__main__":
    visibleclock(10)