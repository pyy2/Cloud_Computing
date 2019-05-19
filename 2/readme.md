# Objective

### Learn how to create containers for a set of microservices and orchestrate and manage them using kubernetes

## Overview

This assignment, you will

1. Build and run a microservice based application, called Sentiment Analyzer, on your computer.
2. Build container images for each service of the microservice application.
3. Deploy a microservice based application into a Kubernetes Managed Cluster.

The detailed instruction is in the URL below

https://medium.freecodecamp.org/learn-kubernetes-in-under-3-hours-a-detailed-guide-to-orchestrating-containers-114ff420e882 

### What to submit

One zip file which contains the files in each step in its own directory. There are 4 steps, so there should be 4 directories, ie. 1,2,3,4, each with files asked in the description below.

1. Proof that the application can be run on your local machine.

    The terminal output what you have done to set it up
    The screen capture of the Web UI as a result of input "I love Cloud Computing"

2. Proof that you can build and upload docker images for the services, ie. sa-frontend, sa-webapp, sa-logic to docker hub.

    Submit a screen capture showing your images in the docker hub, ie. 
    Docker Images on docker hub

3. Proof that you can run these docker images manually to provide the same functionality like 1)

    Submit the terminal output what you have done for this step, including the output of the command 'docker ps -q'
    Submit the screen capture of the Web UI as a result of  input "Docker container is awesome"

4. Proof that you can orchestrate these containers in a kubernetes deployment shown below, ie. 


Submit the terminal output what you have done for this step, including the commands below after the deployment
1. kubectl get pods --output=wide
2. kubectl get service --output=wide
3. kubectl get deployment --output=wide

Submit screen capture of the web UI as a result of input "Kubernetes is not easy to understand"
