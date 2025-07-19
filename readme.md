This is a working bento packaging & deployment example for the chatterbox text-to-speech model (https://huggingface.co/ResembleAI/chatterbox) on top of HPE Private Cloud AI. This repo includes a working bento (chatterbox.bento) which you can upload to your Private Cloud S3 (with the upload_bento notebook - make sure to use whatever bucket names you want instead of what I've chosen)

Once you've uploaded the model to your S3 bucket of choice, follow these instructions to add as a packaged model to HPE MLIS: 

1: Add the S3 storage as a registry to MLIS. For endpoint it should look something like this (verify on your AI Essentials UI) : http://local-s3-service.ezdata-system.svc.cluster.local:30000. To retrieve the access and secret key you can open a boto3 client to the S3 endpoint (no credentials necessary) and run the following code from your jupyter notebook: 

creds = boto3.Session().get_credentials()
print(f"Access Key: {creds.access_key}")
print(f"Secret Key: {creds.secret_key}")
print(f"Token: {creds.token}")

Or verify these credentials via the Upload_bento notebook example. Don't forget to specify a bucketname. 

2: Create your packaged model within MLIS. Select your newly created S3 registry, bento archive format, and pass the following as the url: s3://[yourbucketnamehere]/chatterbox.bento [or whatever you called your bento if you renamed it or created your own]. For resource allocation I have tested using 1-6 CPU, 20GB memory and 1GPU. CPU inferencing should also work but a lot slower (this is a pretty powerful model that even lets you set expressions).

3: Create a deployment of your packaged model on MLIS (fixed-1 for example) and ensure you generate an access token. 

4: Wait for successful deployment of the model and then run tests using the MLIS_inference notebook (ensure you replace my example API and token with your own)

5: The model should return an audio file with the requested text generated as audio. 

This repo also includes a frontend for interacting with the model in the "frontend" folder - simply follow the instructions from that folder to get a frontend deployed in your HPE PCAI AI Essentials environment which can be assessed from the UI to interact with the model.

<img width="3014" height="1476" alt="image" src="https://github.com/user-attachments/assets/37276158-5253-486a-8c2e-c5dc9791b008" />

If you are interested in how this model was packaged as a bento, please check the bento_build_files directory.
