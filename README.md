# UNet-based segmentation algorithm

This repository contains a UNet-based segmentation algorithm and wrapper code to integrate it into the THRIVE framework. 

## Unpack data as instructed in THRIVE


## Set up environment variables

Within your directory that contains the file docker-compose.yml, create a file called .env that contains:

`
LOCAL_DATA_DIR=/your/data/root
Rt106_SERVER_HOST=localhost
`

## Build the UNet cell segmentation algorithm docker image

First, build the rt106 base image. Go to "containers" directory, build the "thrive20/rt106-algorithm-sdk-focal" image by doing:

`
$ docker build -t thrive20/rt106-algorithm-sdk-focal .
`

Second, build the algorithm image. Go to the algorithm directory, e.g., containers/algorithms, build the algorithm image by:

`
$ docker build -t thrive20/unet-cell-segmentation-focal .
`
replace "unet-cell-segmentation-focal" by your own algorithm image name.

Note that you may need to change the "entrypoint.sh" script depending on the python versions you have:
`
/usr/bin/python3 ./rt106GenericAdaptorREST.py & sleep 3
/usr/bin/python2 ./rt106GenericAdaptorAMQP.py --broker rabbitmq --dicom http://datastore:5106
`

Finally, add the following to the docker-compose.yml file:

`  unet-cell-segmentation:
    image: thrive20/unet-cell-segmentation-focal:latest
    ports:
    - 7106
    environment:
      MSG_SYSTEM: amqp
      SERVICE_NAME: unet-cell-segmentation--v1_0_0
      SERVICE_TAGS: analytic
`
Again, replace "unet-cell" with your own algorithm name. 


## Run docker-compose

Run:

`
$ docker-compose up
`

 
## Features of Rt. 106 

* Based on Docker for easy setup and configuration.
* Entirely web-based for easy deployment in cloud or on premise.
* Displays DICOM or TIFF images using the Cornerstone image viewer, along with mask overlays.
* An Algorithm SDK makes it easy to add new algorithms.
* The user interface is easily customizable to create custom applications.
* A file-based datastore is provided having a well-defined REST API so that alternative storage mechanisms can be integrated or developed.
* Algorithm executions are tracked in a database for later reference.
* Initial set of automated quality tests.

--------------------------------


