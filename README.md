# Organic Data Science Dockerized wiki

## 1. Make sure your git credentials are set
    git config --global credential.https://github.com.username [github_user_id]

## 2. Pull recursive
    git clone --recursive https://github.com/KnowledgeCaptureAndDiscovery/ods-docker

## 3. Creating the Docker Image

1. In the same directory as this readme file run the following:
    
    ```
    docker build -f docker/enigma/Dockerfile -t kcapd/ods-enigma .
    ```
    
2. Get the id of the image that was just created for use in the next step:

    ```
    > docker images
    REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
    kcapd/ods-enigma       latest              8e5888362ff4        12 minutes ago      1.27GB
    ``` 
    
    
3. To test the docker image, run the following command. The wiki will be available at http://localhost:8080/wiki

    ``` 
    > docker run -it -p8080:8080 kcapd/ods-enigma
    ```
