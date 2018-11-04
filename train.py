import subprocess
import shutil
import os


def run():
    selection = int(input('What are you training (-1 is all)?'))

    print("Moving positives...")
    move_positives(selection)

    print("Moving negatives...")
    move_negatives(selection)

    print("Generating info file...")
    generate_info_file()

    print("Generating vector file...")
    generate_vec_file()

    print("Generating background directory...")
    generate_background_directory()

    print("Starting Training")
    train_cascade()

    return True


def copy_directory(src, dst, num):
    if not os.path.exists(dst):
        os.makedirs(dst)
    else:
        return
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        shutil.copy(full_file_name, dst)
        os.rename(os.path.join(dst, file_name), os.path.join(dst, str(num) + '_' + file_name))
    return True


def move_positives(selected):
    if selected == -1:
        for i in range(10):
            copy_directory(os.path.join(os.getcwd(), 'setup/markup/' + str(i) + '/'),
                           os.path.join(os.getcwd(), 'training/info/'),
                           i)
    elif -1 < selected < 10:
        copy_directory(os.path.join(os.getcwd(), 'setup/markup/' + str(selected) + '/'),
                       os.path.join(os.getcwd(), 'training/info/'),
                       selected)
    else:
        print("Something went terribly wrong")

    return True


def move_negatives(selected):
    if selected == -1:
        copy_directory(os.path.join(os.getcwd(), 'setup/backgrounds/'),
                       os.path.join(os.getcwd(), 'training/bg/'),
                       selected)
    elif -1 < selected < 10:
        for i in range(10):
            if not i == selected:
                copy_directory(os.path.join(os.getcwd(), 'setup/markup/' + str(i)),
                               os.path.join(os.getcwd(), 'training/bg/'),
                               i)
    else:
        print("Something went terribly wrong")
    return True


def generate_info_file():
    positive_directory = 'training/info'
    info_file_path = 'training/info/info.lst'
    list_of_positives = [
                        file
                        for file in os.listdir(os.path.join(os.getcwd(), positive_directory))
                        ]
    with open(os.path.join(os.getcwd(), info_file_path), 'w') as file:
        for filename in list_of_positives:
            if filename[-3::] == 'jpg':
                n, index, x, y, w, h = filename.split('_')
                h = h[0:-4]
                file.write(filename + ' ' +
                           '1' + ' ' +
                           str(int(x)) + ' ' +
                           str(int(y)) + ' ' +
                           str(int(w)) + ' ' +
                           str(int(h)) + '\n')
    file.close()
    return True


# opencv_createsamples -info info/info.lst -num 41 -w 20 -h 40 -vec positives.vec
def generate_vec_file():
    num_neg = len(os.listdir('./training/info')) - 10
    subprocess.call(['opencv_createsamples',
                    '-info', 'info/info.lst',
                    '-num', str(num_neg),
                    '-w', '18',
                    '-h', '31',
                    '-vec', 'positives.vec'
                    ],
                   cwd='./training',
                   )


# creates BD file for sample creation and training
def generate_background_directory():
    negative_directory = 'training/bg'
    bg_path = 'training/bg.txt'
    list_of_negatives = [
        os.path.join(os.getcwd(), negative_directory, file)
        for file in os.listdir(os.path.join(os.getcwd(), negative_directory))
        if file[-3::] == 'jpg'
    ]
    with open(os.path.join(os.getcwd(), bg_path), 'w') as file:
        for filePath in list_of_negatives:
            file.write(filePath + os.linesep)
    file.close()
    return True


# opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 41 -numNeg 41 -numStages 20 -w 20 -h 40
def train_cascade():
    if not os.path.exists('./training/data'):
        os.mkdir('./training/data')
    num_pos = len(os.listdir('./training/info')) - 250
    num_neg = len(os.listdir('./training/bg')) - 10

    num_pics = int(min(num_pos/2, num_neg))

    subprocess.call(['opencv_traincascade',
                    '-data', 'data',
                    '-vec', 'positives.vec',
                    '-bg', 'bg.txt',
                    '-numPos', str(num_pics*2),
                    '-numNeg', str(num_pics),
                    '-numStages', '20',
                    '-w', '18',
                    '-h', '31'],
                   cwd='./training')
    return True


if __name__ == '__main__':
    print(os.getcwd())
    run()
