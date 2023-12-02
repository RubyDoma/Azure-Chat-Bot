# Activate Virtual Environment (create one if missing: python -m venv venv)

source venv/Scripts/activate

## Install requirements

pip install -r requirements.txt

### Use MFA to log in to Sandbox, then run create_resources.bat:

bash create_resources.bat

This script will:

1. Log in to Azure
2. Set subscription to use (the subscription used for this Bot)
3. Export variable names of Resource Group, Storage Account and Container
4. Create a Resource Group in the Subscription
5. Create a Storage Account
6. Get the Access Key from the newly created Storage Account
7. Export the Access Key value (used to authorize access to data in the storage account)
8. Create a Container
9. Assign Owner role to Service Principal (AtlassianServicePrincipal) for the newly created Resource Group
10. Create a GitHub secret with the new access key

#### Deploy code manually via CLI (optional)

1. Create a zip file with folders and files needed
2. Run this command to deploy code to Azure app:

az webapp deployment source config-zip --resource-group "AtlassianRG" --name "atlassian-chat" --src "C:\Users\rdomanico\OneDrive - KPMG\Desktop\EPA PROJECT\Ruby-Domanico-EPA\echo_bot.zip"

##### Testing

The files <file_name1>.py and <file_name2>.py containing the unit tests created. These tests will check <...>.

To run the tests from a terminal (outside of any IDE) please use the following command:

- pytest <file_name>.py
