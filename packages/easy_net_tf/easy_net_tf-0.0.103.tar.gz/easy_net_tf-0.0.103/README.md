## easy_net_tf

A tensorflow-based network utility lib.

### features
- Tensorflow based
- python3

### install	
`pip install easy_net_tf`

### dependence
`tensorflow`, `numpy`, `cv2`

### content

#### nn (nerual network)
- fully connect net: `from easy_net_tf.nn.fully_connect_net import FullyConnectNet`
- mobilenet: `from easy_net_tf.nn.mobile_net_v2 import MobileNetV2`
- cnn: `from easy_net_tf.nn.cnn import CNN`

#### utility
- accuracy:	`from easy_net_tf.utility.accuracy import UtilityAccuracy`
- file:	`from easy_net_tf.utility.file import UtilityFile`
- variable:	`from easy_net_tf.utility.variable import UtilityVariable`
- anchor: `from easy_net_tf.utility.anchor import UtilityAnchor`
- bounding: `from easy_net_tf.utility.bounding import UtilityBounding`
- loss: `from easy_net_tf.utility.bounding import UtilityLoss`
- image: `from easy_net_tf.utility.image import UtilityImage`
- slide_window: `from easy_net_tf.utility.slide_window import UtilitySlideWindow`

### license
MIT