# HolySheet
Word crawler for ancient documents.

<div align="center">

<div>
<img src="demoImages/Gut-24.png" width="350px" float="left"/>

<img src="demoImages/binarizedColumn.png" width="152px" float="right"/> 
</div>

Original <b>Genesis</b> image and binarization 

<img src="demoImages/binarizedRow.png"/>

<b>Line</b> segmentation

<img src="demoImages/binarizedWord.png"/>

<b>Word</b> segmentation

</div>

This software provides for binarization and word segmentation of ancient document,
like Genesis (from Holy Bible). In particular it can:

- **Elaborate .png scans of ancient document with python libraries like openCV**

- **Get word segmentation, using histogram pixel techniques and specific heuristics**

- **Prepare a dataset for Detectron neural network (faster)**

- **Last part want to train a network to find words in new similar documents**

### Requirements

- python packages
    - opencv
    - matplotlib
    - numpy
    - pillow

For the second part (https://github.com/roytseng-tw/Detectron.pytorch) we used PyTorch.

### How To Use