from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D

num_classes = 2
resnet_weights_path = weight_path
my_new_model = Sequential()
my_new_model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_weights_path))
my_new_model.add(Dense(num_classes, activation='softmax'))

my_new_model.layers[0].trainable = False

my_new_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

# Data Augmentation
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

image_size = 224

data_generator_with_aug = ImageDataGenerator(preprocessing_funcion=preprocess_input, horizontal_flip=True, width_shift_range=0.1, height_shift_range=0.1)
data_generator_no_aug = ImageDataGenerator(preprocessing_funcion=preprocess_input)

train_generator = data_generator_with_aug.flow_from_directory(
    directory='directory',
    target_size=(image_size, image_size),
    batch_size=12,
    class_mode='categorical'
)

validation_generator = data_generator_no_aug.flow_from_directory(
    directory='directory',
    target_size=(image_size, image_size),
    class_mode='categorical'
)

my_new_model.fit_generator(
    train_generator,
    epochs=3,
    steps_per_epoch=19,
    validation_data=validation_generator
)

# From Scratch
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D

img_rows, img_cols = 28, 28
num_classes = 10

def prep_data(raw):
    y = raw[:, 0]
    out_y = keras.utils.to_categorical(y, num_classes)

    x = raw[:, 1:]
    num_images = raw.shape[0]
    out_x = x.reshape(num_images, img_rows, img_cols, 1)
    out_x = out_x / 255
    return out_x, out_y

fashin_file = 'file_path.csv'
fashin_data = np.loadtxt(fashion_file, skiprows=1, delimiter=',')
x, y = prep_data(fashion_data)

fashion_model = Sequential()
fashion_model.add(Conv2D(12, activation='relu', kernel_size=3, input_shape=(img_rows, img_cols)))
fashion_model.add(Conv2D(20, activation='relu', kernel_size=3))
fashion_model.add(Conv2D(20, activation='relu', kernel_size=3))
fashion_model.add(Flatten())
fashion_model.add(Dense(100, activation='relu'))
fashion_model.add(Dense(10, activation='softmax'))
fashion_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

fashion_model.fit(x, y, batch_size=100, epochs=4, validation_split=0.2)

fashion_model.add(Conv2D(20, activation='relu', kernel_size=3, strides=2))
fashion_model.add(Dropout(0.5))
