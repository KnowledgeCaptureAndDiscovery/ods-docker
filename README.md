# Organic Data Science Dockerized wiki

## 1. Getting the pre-built Docker Image
    
    docker pull kcapd/ods-enigma

## 2. (Optional) Creating the Docker Image yourself

a. Get the source

    git clone --recursive https://github.com/KnowledgeCaptureAndDiscovery/ods-docker

b. Run the following in the same directory as this readme file:
    
    docker build -f docker/enigma/Dockerfile -t kcapd/ods-enigma .

c. Get the id of the image that was just created for use in the next step:

    > docker images
    REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
    kcapd/ods-enigma       latest              8e5888362ff4        12 minutes ago      1.27GB

    
## 4. Testing the Docker Image  

a. To test the docker image, run the following command. The wiki will be available at http://localhost:8080/wiki. The default admin username/password is admin/admin123.

    > docker run -it -p8080:8080 kcapd/ods-enigma

b. You can view or bootstrap the ontology for the wiki from http://localhost:8080/wiki/index.php/Special:WTBootstrap. (For enigma, it is pre-loaded from https://w3id.org/enigma, and you don't need to import it. Note that it could take upto 5 minutes for all the concepts & properties from the ontology to be imported onto the Wiki). 

c. When you create any new page, you can choose the category for the page, which creates the appropriate UI for the properties of the page to be filled out.
