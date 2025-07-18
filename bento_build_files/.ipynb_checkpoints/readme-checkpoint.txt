How to build a bento in HPE Private Cloud AI

First ensure you are building your bentoml package using version bentoml==1.1.11 (as of AI Essentials 1.8 version) and python 3.9 compatible dependencies. 

You then need 3 files to create your bento:

    service.py is your inferencing definition 
    requirements.txt is your list of inferencing dependencies
    bentofile.yaml is your packaging definition

Once you've defined your application with these 3 files, run the following bentoml commands:

- bentoml build (this will give you an image name in local bentoml repo)
- bentoml export <imagename> (this will provide you with a lightweight .bento file that you can use to serve the model from MLIS for example)