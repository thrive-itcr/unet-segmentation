# Docker files to build the UNet algorithm image

First create a models directory, and copy all UNet model files there

Then, run the following command:

`
$ docker build -t thrive20/unet-cell-segmentation-focal .
`

You may replace "unet-cell-segmentation-focal" by your own algorithm image name.

