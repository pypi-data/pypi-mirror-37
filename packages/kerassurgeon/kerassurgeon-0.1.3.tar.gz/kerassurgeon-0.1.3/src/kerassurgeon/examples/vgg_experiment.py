import keras
import tensorflow as tf
import os
import sklearn.metrics as metrics
import numpy as np
from keras.datasets import cifar100
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras import optimizers
from keras.layers.core import Lambda
from keras import backend as K
from keras import regularizers
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, \
    LearningRateScheduler, TensorBoard
from kerassurgeon.operations import delete_layer, insert_layer, \
    delete_channels, replace_layer
from kerassurgeon import Surgeon
from operator import itemgetter, attrgetter
from keras.utils import np_utils

# GPU setting
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.4)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
tf.keras.backend.set_session(sess)

# training parameters
batch_size = 128
maxepoches = 300
learning_rate = 0.1
lr_decay = 1e-6
lr_drop = 20

# VGG model
model = Sequential()
weight_decay = 0.0005

model.add(Conv2D(64, (3, 3), padding='same', input_shape=[32, 32, 3],
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))

model.add(Conv2D(64, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(128, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(256, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(256, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(512, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(512, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(512, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(512, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(512, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(512, (3, 3), padding='same',
                 kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(512, kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(Dropout(0.5))
model.add(Dense(100))
model.add(Activation('softmax'))
print("Model created")

# optimization details
sgd = optimizers.SGD(lr=learning_rate, decay=lr_decay, momentum=0.9,
                     nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd,
              metrics=['accuracy'])
print("Model compile")
model.summary()

# delete channel 0 in every conv layer
# will run error while delete conv layer 36(conv2d_10)
layer_index_bias = 0
for layer_index in [36]:  # [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48,
                    # 54]:  # conv layer index
    print('layer_index:', layer_index)
    delete_layer_index = layer_index + layer_index_bias
    layer = model.layers[delete_layer_index]
    channel = [0]  # delete index 0 channel
    model = delete_channels(model, layer, channel, copy=True)
    layer_index_bias = 1
    print('')

# The data, shuffled and split between train and test sets:
(x_train, y_train), (x_test, y_test) = cifar100.load_data(label_mode='fine')
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

y_test_arr = y_test

x_train /= 255.
x_test /= 255.

y_train = keras.utils.to_categorical(y_train, 100)
y_test = keras.utils.to_categorical(y_test, 100)

# data augmentation
datagen = ImageDataGenerator(
    featurewise_center=False,  # set input mean to 0 over the dataset
    samplewise_center=False,  # set each sample mean to 0
    featurewise_std_normalization=False,  # divide inputs by std of the dataset
    samplewise_std_normalization=False,  # divide each input by its std
    zca_whitening=False,  # apply ZCA whitening
    rotation_range=15,
    # randomly rotate images in the range (degrees, 0 to 180)
    width_shift_range=0.1,
    # randomly shift images horizontally (fraction of total width)
    height_shift_range=0.1,
    # randomly shift images vertically (fraction of total height)
    horizontal_flip=True,  # randomly flip images
    vertical_flip=False)  # randomly flip images
# (std, mean, and principal components if ZCA whitening is applied).
datagen.fit(x_train)


# learning rate
def lr_scheduler(epoch):
    return learning_rate * (0.5 ** (epoch // lr_drop))


reduce_lr = LearningRateScheduler(lr_scheduler)

# checkpoint
model_checkpoint = ModelCheckpoint("cifar100vgg.h5", monitor="val_acc",
                                   save_best_only=True,
                                   save_weights_only=False, verbose=1)

# Tensorboard
tbCallBack = TensorBoard(log_dir='./Graph-C100-VGG', histogram_freq=0,
                         write_graph=True, write_images=True)

# training process in a for loop with learning rate drop every 25 epoches.
historytemp = model.fit_generator(
    datagen.flow(x_train, y_train, batch_size=batch_size),
    steps_per_epoch=x_train.shape[0] // batch_size,
    epochs=maxepoches,
    validation_data=(x_test, y_test),
    callbacks=[reduce_lr, model_checkpoint, tbCallBack], verbose=1)

# acc after training
yPreds = model.predict(x_test, verbose=1)
yPred = np.argmax(yPreds, axis=1)
yTrue = y_test_arr

accuracy = metrics.accuracy_score(yTrue, yPred) * 100
error = 100 - accuracy
print("Accuracy: ", accuracy)
print("Error: ", error)
