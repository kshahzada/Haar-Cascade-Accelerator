import shutil
import os


def run():
    shutil.rmtree('./training')
    os.mkdir('./training')
    os.mkdir('./training/data')
    return True


if __name__ is '__main__':
    run()

