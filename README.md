# Organic Data Science Dockerized wiki

## 1. Pull recursive
    git clone --recursive https://github.com/KnowledgeCaptureAndDiscovery/ods-docker

## 2. Creating the Docker Image

a. In the same directory as this readme file run the following:
    
    ```
    docker build -f docker/enigma/Dockerfile -t kcapd/ods-enigma .
    ```
    
b. Get the id of the image that was just created for use in the next step:

    ```
    > docker images
    REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
    kcapd/ods-enigma       latest              8e5888362ff4        12 minutes ago      1.27GB
    ``` 
    
## 3. Testing the Docker Image  

a. To test the docker image, run the following command. The wiki will be available at http://localhost:8080/wiki

    ``` 
    > docker run -it -p8080:8080 kcapd/ods-enigma
    ```

b. You can bootstrap the ontology for the wiki from http://localhost:8080/wiki/index.php/Special:WTBootstrap. (Note that it could take upto 5 minutes for all the concepts & properties from the ontology to be imported onto the Wiki). Afterwards, when you create any new page, you can choose the category for the page, which creates the appropriate UI for the properties of the page to be filled out.
