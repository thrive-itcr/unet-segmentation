# Copyright (c) General Electric Company, 2019.  All rights reserved.
#FROM debian:stretch
FROM ubuntu:20.04

# install dependencies
RUN buildDeps='python3-pip' \
    && set -x \
    && apt-get -y update && apt-get install -y $buildDeps --no-install-recommends \
    && pip3 install --upgrade pip && hash -r \
    && pip3 install --upgrade setuptools \
    && pip3 install flask pika==0.9.14 boto3 requests==2.19 junit-xml pytest-cov

# install SDK
ADD rt106GenericAdaptorSQS.py rt106GenericAdaptorAMQP.py rt106GenericAdaptorREST.py rt106SpecificAdaptorCode.py rt106SpecificAdaptorDefinitions.json entrypoint.sh testGenericAdaptorAPIs.py testGenericAdaptorAMQP.py /rt106/

# configure folder structures
RUN mkdir /rt106/input && mkdir /rt106/output && mkdir /rt106/test

# set permissions
RUN chmod a+x /rt106/entrypoint.sh

# set the working directory
WORKDIR /rt106

# establish the user
# create non-privileged user and group
RUN groupadd -r rt106 && useradd -r -g rt106 rt106 && chown -R rt106:rt106 /rt106
USER rt106:rt106

# configure the default port for an analytic, can be overridden in entrypoint
EXPOSE 7106

# entry point
CMD ["/rt106/entrypoint.sh"]
