### Clone 

### Create and activate your venv

cd evocloud

python3 -m venv ./venv

source venv/bin/activate

### Install Google Cloud libraries and login

### Put inside the environment.env file the path to your credentials

create the PubSub topics.

### Edit the experiment file

### Upload the function ga_google/main

gcloud functions deploy main --runtime python37 --trigger-topic population-objects






