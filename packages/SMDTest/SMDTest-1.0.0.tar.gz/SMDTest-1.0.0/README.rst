
SMDTest
======

A simple python wrapper for disparity calculation.

The PSMNet is from: https://github.com/JiaRenChang/PSMNet


The code is Python 2, but Python 3 compatible.

Installation
============

Fast install:

```
for python2: pip install SMDTest

for python3: pip3 install SMDTest
```    


Example:


```
from PSMNet import smd
disparity_img = smd.calculate_disparity(imgL,imgR)
corrected_img = smd.correct_img(imgR,disparity_img)
```

