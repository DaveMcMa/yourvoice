This folder includes all the files required to import the application into your HPE Private Cloud AI system.

Instructions on use: Import a new framework via AI Essentials and use yourvoice_helm.tgz as your helm chart. Make sure you add your Chatterbox endpoint & token into the values yaml before deploying (this is done during deployment phase via the AI Essentials UI, but can also be changed via the UI if necessary)

All other files in this repo are not necessary to get the app running but were necessary to get to the final state. Quick rundown of files and what their purpose was:

Dockerfile: Required to package the frontend GUI as a docker image and upload to my repository
app.py: This is the gradio/python code that the docker image runs, essentially the front end code
icon.png: This is the icon I use in AI Essentials when deploying the helm chart
logo.png: This logo is packaged into the docker image / app.py so the frontend has the required logo built in & available
requirements.txt
helmchart (folder): This folder is the helm chart (unzipped) for deploying the UI 
