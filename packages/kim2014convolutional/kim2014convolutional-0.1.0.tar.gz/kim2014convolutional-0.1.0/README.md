# kim2014convolutional

This package provides a simple implementation of the models proposed in
the paper:

    Kim, Y. (2014). Convolutional neural networks for sentence classification. arXiv preprint arXiv:1408.5882.

## Installation
This package depends on the [Keras](https://keras.io/) library. This
means you will need to install a backend library in order to use this
module. Take a look to [Keras installation](https://keras.io/#installation)
to get more information.

After having installed the backend of yout choice, you just need to
install this package using [pip](https://pypi.org/):

    pip install kim2014convolutional

## Usage
This package only provides a single model. To get detailed information
on the parameters the model accepts, take a look to the documentation
included with the module class.

Here is a complete example of instantiation of the `CNN-multichannel`
model proposed in the original paper using two channel of randomly
initialized word embeddings:

```python
import numpy as np
import numpy.random as rng

vocabulary_size = 10000
embedding_size = 300

value = np.sqrt(6/embedding_size)

weights_shape = (vocabulary_size+1, embedding_size)
weights = rng.uniform(low=-value, high=value, size=weights_shape)

channels = [
    {
      'weights': [weights],
      'trainable': False,
      'input_dim': vocabulary_size + 1,
      'output_dim': embedding_size,
      'name': 'random-embedding-1'
    },
    {
      'weights': [weights],
      'trainable': True,
      'input_dim': vocabulary_size + 1,
      'output_dim': embedding_size,
      'name': 'random-embedding-2'
    }
]

windows = [
    {
        'filters': 100,
        'kernel_size': 3,
        'activation': 'relu',
        'name': '3-grams'
    },
    {
        'filters': 100,
        'kernel_size': 4,
        'activation': 'relu',
        'name': '4-grams'
    },
    {
        'filters': 100,
        'kernel_size': 5,
        'activation': 'relu',
        'name': '5-grams'
    }
]

from kim2014convolutional import Model

model = Model(channels=channels,
              windows=windows,
              sentence_length=37,
              num_classes=6,
              dropout_rate=0.5,
              maxnorm_value=3,
              classifier_activation='softmax',
              include_top=True,
              name='CNN-multichannel')

model.summary()
```
