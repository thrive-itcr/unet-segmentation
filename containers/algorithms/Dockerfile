FROM thrive20/rt106-algorithm-sdk-focal:latest

USER root

## start installing dependency

ENV DEBIAN_FRONTEND=noninteractive 

RUN  echo "52.22.146.88 index.docker.io" >> /etc/hosts \
  && apt-get update \
  && apt-get install -y -qq --no-install-recommends \
       curl \
       apt-utils \
       lsb-release \
       apt-transport-https \
       software-properties-common \
       ca-certificates \
  \
  && apt-get install -y -qq \
     iputils-ping \
     build-essential \
     #python-virtualenv \
     #python-dev \
     vim \
     git \
     sudo \
     xterm \
     xauth \
     xorg \
     dbus-x11 \
     xfonts-100dpi \
     xfonts-75dpi \
     xfonts-cyrillic

RUN apt-get install -y docker.io \
  && apt-get -y autoremove \
  && apt-get -y clean \
  && rm -rf /var/lib/apt/lists/* \
  \
  && mkdir /tmp/.X11-unix \
  && chmod 1777 /tmp/.X11-unix \
  && chown root:root /tmp/.X11-unix/

RUN apt-get update \
  && apt-get install -y \
  apt-utils \
  file \
  wget \
  cmake \
  bash-completion \
  python3-software-properties \
  python3 \
  python3-pip \
  python3-dev \
  python3-tk \
  python3-venv \
  python3-numpy \
  sqlite3 \
  libproj-dev \
  libjsoncpp-dev \
  libgeos-dev \
  libproj-dev \
  libxml2-dev \
  libpq-dev \
  libnetcdf-dev \
  libpoppler-dev \
  libcurl4-gnutls-dev \
  libhdf4-alt-dev \
  libhdf5-serial-dev \
  libgeographic-dev \
  libfftw3-dev \
  libtiff5-dev \
  libgmp3-dev \
  libmpfr-dev \
  libxerces-c-dev \
  libmpfr-dev \
  libmuparser-dev \
  libboost-date-time-dev \
  libboost-system-dev \
  libboost-filesystem-dev \
  libgsl-dev \
  libgeos++-dev \
  libpng-dev \
  sudo \
  xvfb \
  && apt-get -y clean \
  && rm -rf /var/lib/apt/lists/*

# Install image processing related packages
RUN pip3 --no-cache-dir install -U scikit-learn \
  && pip3 --no-cache-dir install scikit-image \
  && pip3 --no-cache-dir install opencv-python \
  && pip3 install tifffile python3-pika

RUN pip3 install keras>=2.2.4 \
  && pip3 install tensorflow


## end dependency install


## add python2 dependency

RUN apt-get -y update \
    && apt-get -y install libgtk2.0-0 \
    && apt-get -y install libsm6 \
    && apt-get -y install python2 

RUN curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
RUN python2 get-pip.py

RUN pip2 install --upgrade setuptools \
    && pip2 install flask pika==0.9.14 boto3 requests==2.19 junit-xml pytest-cov \
    && pip2 install numpy opencv-python


## add the adaptor code specialized for this algorithm
ADD rt106SpecificAdaptorCode.py rt106SpecificAdaptorDefinitions.json entrypoint.sh /rt106/

ADD runDAPISeg.py testTissueSeg.py learning_helpers.py CellDIVE_IO.py CellDIVE_Seg.py /rt106/
ADD models /rt106/
ADD models/unet_models/nuc_seg_unet_model_48_sp.json /rt106/models/unet_models/nuc_seg_unet_model_48_sp.json
ADD models/unet_models/nuc_seg_unet_model_48_sp.h5 /rt106/models/unet_models/nuc_seg_unet_model_48_sp.h5

RUN mkdir -p /rt106/input && mkdir -p /rt106/output
RUN chmod a+x /rt106/entrypoint.sh

# set the working directory
WORKDIR /rt106

# set permissions
RUN chown -R rt106:rt106 /rt106

# establish user (created in the base image)
USER rt106:rt106

# entry point
CMD ["/rt106/entrypoint.sh"]
