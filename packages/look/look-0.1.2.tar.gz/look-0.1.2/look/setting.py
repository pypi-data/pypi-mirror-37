from pathlib import Path

NUMBER = ['2', '3', '4', '5', '6', '7', '8', '9']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

ALL_CHAR_SET = NUMBER + ALPHABET
ALL_CHAR_SET_LEN = len(ALL_CHAR_SET)
MAX_CAPTCHA = 1

# 图像大小
IMAGE_HEIGHT = 26
IMAGE_WIDTH = 15

# 切图参数
box = {}
box[0] = (9,3,24,30)
box[1] = (24,3,39,30)
box[2] = (39,3,54,30)
box[3] = (54,3,69,30)


dataset = Path('dataset')
SOURCE_TRAIN_PATH = dataset / 'source_train'
SOURCE_TEST_PATH = dataset / 'source_test'
TRAIN_PATH = dataset / 'train'
TEST_PATH = dataset / 'test'
CAPTCHA_PATH = dataset / 'captcha'
DOWNLOAD_Path = dataset / 'download'


# Hyper Parameters
TRAIN_NUM_EPOCHS = 100
# TRAIN_BATCH_SIZE = 64
TRAIN_LEARNING_RATE = 0.001
