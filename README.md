# Zest.ai Web Development Deliverable #

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