# Zest.ai Web Development Deliverable #

First, download the latest version of Docker and Docker-Compose from: https://docs.docker.com/compose/

To run both the front-end React app and the Python flask server, execute the following command:

`docker-compose up`

To shut down the applications:

`docker-compose down`

If you make changes to the Dockerfile or any other elements of the build config, you may need to rebuild the containers:

`docker-compose build`

Alternatively, you can both build and launch the containers in one command:

`docker-compose up --build`

More information on how to use docker commands can be found on the Docker website: https://docs.docker.com/compose/reference/overview/ 

Note: this containerization is configured for development only. We still need to write some build files for the production build.

## ZRP Endpoint ##

Picklefiles:
    - need the "zrp_fe_pkl.obj" and "clf_fl.obj" picklefiles in the picklefiles/ directory to run predictions

Required Parameters:
    - first name
    - last name
    - middle name
    - zipcode
    - precinct split
    - gender
    - county code
    - congressional district
    - senate district
    - house district
    - birth date

The goal is to eventually reduce the number of required fields needed to run predictions (perhaps calling a census API that can retrieve the required parameters). 