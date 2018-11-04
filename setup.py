import random
import os
import cv2
import subprocess

rng_seed = random.randint(1, 2500000)


def run():
    print("Setting up background images...")
    num_images = move_backgrounds('./images/raw', './setup/backgrounds')
    print("Moved " + str(num_images) + " images")

    print("Moving positives...")
    num_images = move_positives('./images/goals', './setup/goals')
    print("Moved " + str(num_images) + " images")

    print("Generating overlaid samples...")
    num_gen = gen_marked_up('./images/goals', './setup/markup')
    print(str(num_gen) + " images generated (each)")

    return True


def move_backgrounds(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    i = 0
    for filename in os.listdir(src):
        if filename[-3::] == 'jpg':
            img = cv2.imread(os.path.join(src, filename))
            img = size_resample_image(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(dest, str(i) + '.jpg'), img)
            i += 1

    return i


def size_resample_image(img):
    (h, w, d) = img.shape

    if w > 210 and h > 210:
        w_start = random.randint(1, w - 201)
        h_start = random.randint(1, h - 201)
        resized = img[h_start:h_start+200, w_start:w_start+200]
    else:
        resized = cv2.resize(img, (200, 200), interpolation=cv2.INTER_LINEAR)

    return resized


def move_positives(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    i = 0
    for filename in os.listdir(src):
        if filename[-3::] == 'jpg':
            img = cv2.imread(os.path.join(src, filename))
            img = cv2.resize(img, (18, 31))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(dest, filename), img)
            i += 1
    return i


def generate_background_directory():
    negative_directory = 'setup/backgrounds'
    bg_path = 'setup/bg.txt'
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


def gen_samples(i):
    num_neg = len(os.listdir(os.path.join(os.getcwd(), 'setup/backgrounds'))) - 10
    print(i)
    subprocess.call(['opencv_createsamples',
                    '-img', 'goals/' + str(i) + '.jpg',
                    '-bg', 'bg.txt',
                    '-info', 'markup/' + str(i) + '/info.lst',
                    '-pngoutput', 'markup/' + str(i),
                    '-bgcolor', '255',
                    '-maxxangle', '0.5',
                    '-maxyangle', '0.5',
                    '-maxzangle', '0.5',
                    '-w', '18',
                    '-h', '31',
                    '-num', str(num_neg),
                    '-rngseed', str(random.randint(1, 2500000))
                    ],
                   cwd='./setup',
                   )
    return num_neg

def gen_marked_up(src, dest):
    generate_background_directory()

    if not os.path.exists(dest):
        os.mkdir(dest)

    for i in range(10):
        temp_dest = os.path.join(dest, str(i))
        if not os.path.exists(temp_dest):
            os.mkdir(temp_dest)
        num_gen = gen_samples(i)

    return num_gen


if __name__ == '__main__':
    run()


