pl-imageconvert
================================

.. image:: https://badge.fury.io/py/imageconvert.svg
    :target: https://badge.fury.io/py/imageconvert

.. image:: https://travis-ci.org/FNNDSC/imageconvert.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/imageconvert

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-imageconvert

.. contents:: Table of Contents


Abstract
--------

An app to which acts as a Python wrapper around Linux CLI "convert" which works as an entrypoint around the Linux image processing 'ImageMagick'.


Synopsis
--------

.. code::

    python imageconvert.py                                           \
        [-i|--inputFile <inputFile>]                                 \
        [-o|--outputFile <outputFile>]                               \
        [-a|--args <convertArgsToPass>]                              \
        [-x|--man]                                                   \
        [-y|--synopsis]                                              \
        [--version]                                                  \
        [-v|--verbosity <level>]                                     \
        <inputdir>                                                   \
        <outputdir>                                                  

Description
-----------

``pl-imageconvert`` is a ChrisApp plugin which acts as a wrapper around the ``magick convert`` Linux CLI program that is useful for convert input images to the desired format and saves them in an output directory specified by the user.

This utility requires you to pass an ``inputDir``, ``inputFile``, ``outputDir``, ``outputFile``, and all the other optional CLI arguments that the ``convert`` accepts as a string to the ``args`` argument of ``pyimgconvert``. 

If running this application directly, i.e. outside of its docker container, please make sure that the `imagemagick` application is installed in the host system. On Ubuntu, this is typically:


.. code::
                    
    sudo apt install imagemagick

and also make sure that you are in an appropriate python virtual
environment with necessary requirements already installed 
(see the ``requirements.txt`` file).

Please note, however, that running this application from its
docker container is the preferred method and the one documented
here.

Arguments
---------

.. code::

        [-i|--inputFile <inputFile>]
        Input file within the inputDir that needs to be converted  

        [-a|--args <convertArgsToPass>]
        Arguments that are upposed to be passed to the "magick convert"

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--version]
        If specified, print the version number and exit.

        [-v|--verbosity <level>]
        Set the app verbosity level. 


Run
----

While ``pl-imageconvert`` is meant to be run as a containerized docker image, typcially within ChRIS, it is quite possible to run the dockerized plugin directly from the command line as well. The following instructions are meant to be a psuedo- ``jupyter-notebook`` inspired style where if you follow along and copy/paste into a terminal you should be able to run all the examples.

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

- Pull any one sample image from this link: https://www.fieggen.com/software/jpgextra_sample.htm

- Save this image in your ``devel`` directory with the name "image.jpg".

Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

- Make sure your current working directory is ``devel``. At this juncture it should contain ``image.jpg``.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

- Pull the ``fnndsc/pl-imageconvert`` image using the following command.

.. code:: bash

    docker pull fnndsc/pl-imageconvert


Examples
--------

Copy and modify the different commands below as needed

..  code:: bash

    docker run --rm                                                   \
        -v ${DEVEL}/:/incoming -v ${DEVEL}/results/:/outgoing          \
        fnndsc/pl-imageconvert imageconvert.py                         \
        -i image.jpg                                                   \
        -o image.png                                                   \
        --args "ARGS: -colorspace RGB -resize 40% "                    \                                                \
        /incoming /outgoing


Debug
------

Finally, let's conclude with some quick notes on debugging this plugin. The debugging process is predicated on the idea of mapping a source code directory into an already existing container, thus "shadowing" or "masking" the existing code and overlaying current work directly within the container.

In this manner, one can debug the plugin without needing to continually rebuild the docker image.

So, assuming the same env variables as above, and assuming that you are in the source repo base directory of the plugin code:

.. code:: bash

    git clone https://github.com/FNNDSC/pl-imageconvert.git
    cd pl-imageconvert
    docker run --rm -ti                                                 \
           -v $(pwd)/imageconvert:/usr/src/imageconvert                   \
           -v ${DEVEL}/:/incoming                                         \
           -v ${DEVEL}/results/:/outgoing                                 \
           fnndsc/pl-imageconvert imageconvert.py                         \
           -i image.jpg                                                   \
           -o image.png                                                   \
           --args "ARGS: -colorspace RGB -resize 40% "                    \
           /incoming /outgoing

Of course, adapt the above as needed.


