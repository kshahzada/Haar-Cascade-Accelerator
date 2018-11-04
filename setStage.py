import subprocess


def run():
    stages = int(input("How many stages to train to?"))
    change_stage(stages)
    return True


def change_stage(stages=13):
    to_retrain = [i for i in range(10)]
    to_retrain += ['general']

    for cascade in to_retrain:
        print("Retraining " + str(cascade) + "...")
        subprocess.call([
            'opencv_traincascade',
            '-data', str(cascade),
            '-vec', 'positives.vec',
            '-bg', 'bg.txt',
            '-numStages', str(stages),
        ],
            cwd='./cascades')
    return True


if __name__ == '__main__':
    run()

