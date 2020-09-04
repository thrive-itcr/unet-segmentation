# rt106-algorithm-sdk

[![CircleCI](https://circleci.com/gh/rt106/rt106-algorithm-sdk.svg?style=svg)](https://circleci.com/gh/rt106/rt106-algorithm-sdk)

_Copyright (c) General Electric Company, 2017.  All rights reserved._


**Software Development Kit for adding new algorithms to Rt 106**

This git project contains code and guidelines to simplify adding new algorithms to Rt 106.
The goal is to avoid duplicated code and unnecessary effort.  Therefore, all integration code that is the same
for all integrated algorithms is organized into a "generic adaptor."  The adaptor code that is necessarily different
for each integrated algorithm is kept to a minimum and is organized into an "application-specific adaptor."

The steps to add a new algorithm are:
* Add needed code for calling your algorithm to the application-specific adaptor.
* Create a Dockerfile for building your algorithm along with its adaptor (generic and application-specific parts).
* Base your algorithm's Docker image on the rt106/rt106-algorithm-sdk image.
* Modify the Docker Compose file that launches the entire system to include your algorithm.

More details on all these steps are below.

## Prerequisite knowledge.

The adaptor code is implemented in Python, and the overall architecture of Rt 106 builds on Docker.
Therefore, the user needs to be familiar with both Python and Docker to use this SDK.

A beginning reference on Docker is available here:  [https://www.docker.com/what-docker]

A Python reference is available here:  [https://www.python.org/doc/]

Of course, there are numerous other references available for both Docker and Python.

## To build the algorithm sdk image.

You can build the rt106-algorithm-sdk image using
```
docker build -t rt106/rt106-algorithm-sdk .
```
Depending on your environment, you may need to specify proxy information, so that you would use a command like this:

```
docker build -t rt106/rt106-algorithm-sdk --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy --build-arg no_proxy=$no_proxy .
```

## Algorithm template example

The rt106-algorithm-sdk also provides an example of a packaged algorithm. Launching the rt106-algorithm-sdk directly,
as opposed to just using it as a base image, registers an algorithm with a rt106 system called "algorithm-template" to which
the rt106-frontend will build a UI, send inputs, and receive outputs and status.

## To integrate a new algorithm.

Below are the detailed instructions for integrating a new algorithm into Rt 106 using the SDK.

### Set up your project.

Create a directory that contains your algorithm source files, and also copies of several files from this project:  
* Dockerfile
* entrypoint.sh
* rt106SpecificAdaptorCode.py
* rt106SpecificAdaptorDefinitions.json

As a best practice, you likely want this directory to be managed by GitHub or alternate version control system.

### Modify rt106SpecificAdaptorDefinitions.json

This is where you need to modify a text file that contains a JSON description of the algorithm inputs and outputs. Set values for the elements
described below.

* name: unique name for your analytic, with no white space
* version: version of your analytic, such as 'v1_0_0'
* queue: name of your analytic's request queue, convention is to concatenate the version onto the name of the analytic.
* parameters: description of the input parameters fot the analytic.
* results: description of the outputs that result from running the analytic.
* result_display: description of how you would like you output values or images displayed.
* api: for the short-term, it is not used and can be set to {}
* doc: description of the analytic, both a short description and a detailed description.
* classification: a hierarchical description of your type of algorithm.

This is where you need to modify a small amount of code to call your algorithm, including marshalling inputs and outputs
and reporting status.  Set values for the variables below.

In rt106SpecificAdaptorCode.py, fill in the code needed to get and organize your inputs, call your analytic, receive the outputs,
store the outputs, and send the needed data back to the calling process.  Of course your code should check for
any possible error conditions.

The *context* variable contains the algorithms inputs and parameters in a JSON structure described above.  For example, the *context* variable may contain something like: *{'seriesName':'MySeries'}*
These values need to be marshalled to the inputs of your algorithm as appropriate.

You need to set a value to *myStatus.*

### Dockerfile

The Dockerfile included with the SDK sets up a Python programming environment along with the adaptor itself.  You need to extend this
Dockerfile as required to assemble your algorithm.  You also need to take care that the adaptor can locate your algorithm within the
container.  The path to the algorithm executable likely needs to be included within rt106SpecificAdaptor.py.

### Docker Compose

Your docker-compose.yml file needs to be extended to include a case for your new algorithm.

Required fields include:
* image - name of your Docker image
* ports - include "7106" as the internal port used by the adaptor.  Don't provide an externally-mapped port.  Docker will assign an external port that Registrator can find.
* environment - SERVICE_NAME needs to be set to the name of your new analytic service.  SERVICE_TAGS must be set to 'analytic'.
