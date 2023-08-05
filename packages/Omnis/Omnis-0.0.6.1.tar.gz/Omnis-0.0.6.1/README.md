# Omnis
Deep Learning for Everyone

------------------


## You have just found Omnis.

Omnis is an API of deep neural network applications, written in Python and capable of running on top of [Keras](https://github.com/keras-team/keras). It was developed with a focus on enabling fast application of deep learning.

Use Omnis if you need a deep learning library that:

- Is EASY to learn and use.
- Allows for easy and fast prototyping.
- Supports CNN, LSTM, GAN, RL application.(TBA)
- Runs seamlessly on CPU and GPU.

Omnis is compatible with: __Python 2.7-3.6__.

------------------


## Deep Block

Omnis has been developed as a backend library of [Deep Block](https://deepblock.site). Deep Block is a creative learning community where anyone can learn AI technologies with ease. If you want to learn more about AI or Omnis, try [Deep Block](https://deepblock.site).

------------------


## Getting started: Implement a deep learning application with four lines of code!

The core data structure of Omnis is an application which is designed to be easy to use in each field. Each application consists of a [`Keras Functional Model`](https://keras.io/models/model/).

Here is an `Image Classification` example:

```python
from omnis.application.image_processing.image_classification.densenet import DenseNet121
import cv2
import numpy
```

Choose an application:

```python
cnn = DenseNet121()
```

Prepare data:

```python
cnn.prepare_train_data(get_image_from='directory', data_path='101_ObjectCategories')
```

After preparing data, you can train your application(model):

```python
cnn.train(epochs = 30, batch_size = 16)
```

Now you can use the application to classify images:

```python
ant_img = cv2.imread('101_ObjectCategories/ant/image_0013.jpg')
test_data = numpy.expand_dims(ant_img, axis=0)
reshaped_test_data = cnn.reshape_data(test_data)
prediction_result = cnn.predict(reshaped_test_data)

print('predict labels')
print(prediction_result)
```

For a more in-depth tutorial about Omnis, you can check out:

- [Deep Block](https://deepblock.site)

In the [examples folder](https://github.com/mkh48v/omnis/tree/master/example) of the repository, you will find more applications.

------------------


## Installation

Before installing Omnis, please install Keras. We recommend the TensorFlow backend for Keras.

Then, you can install Omnis itself. There are two ways to install Omnis:

- **Install Omnis from PyPI (recommended):**

If you don't use a virtual environment, you can run the command below (not recommended):

```sh
sudo pip install omnis
```

If you are using a virtual environment, you may want to avoid using sudo (conda virtual environment recommended):

```sh
pip install omnis
```

- **Alternatively: install Omnis from the GitHub source:**

First, clone Omnis using `git`:

```sh
git clone https://github.com/mkh48v/omnis.git
```

 Then, `cd` to the Omnis folder and run the install command:
```sh
cd omnis
sudo python setup.py install
```

------------------


## Guiding principles

- __Simplicity.__ Omnis pursues a simple architecture. Designing a software with simple architecture not only helps you to understand the code easily but also helps your painful debugging.

- __Easiness.__ Don't worry about complicated algorithms or theories or mathematics. Omnis will handle difficult stuffs for you. Just learn how to use deep neural networks and USE THIS!

- __Modularity.__ No spaghetti code!

------------------


## Why this name, Omnis?

Omnis means _EVERY_ in Latin. The goal of Omnis is to make deep learning technologies easier so that _EVERY_ one can use deep learning technologies without headache.

------------------
