=====================
SensiML Python CLient
=====================

SensiML python client provides access to SensiML Analytics services for
building machine learning pipelines including data processing, feature
generation and classification for developing smart sensor algorithms optimized
to run on embedded devices.

------------
Installation
------------

    pip install sensiml

    jupyter contrib nbextension install --user

    jupyter nbextension enable bqplot

    jupyter nbextension enable ipywidgets

    jupyter nbextension enable qgrid

or download the Analytic Studio

    https://sensiml.cloud/downloads


----------------------------------
Connect to SensiML Analytic Engine
----------------------------------

    from sensiml import SensiML

    sml = SensiML()

(Note: Connecting to SensiML servers requires and account to log in)


Go to https://sensiml.com/ to learn more about using our platform to build
 machine learning models suitable for performing real-time timeseries
 classification on embedded devices.

