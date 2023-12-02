az login
az account set --subscription="f4b1e8d1-13bc-4b3a-aa0a-4c6f6459d9fc"
export RESOURCE_GROUP_NAME=AtlassianRG
export STORAGE_ACCOUNT_NAME=atlassiansa
export CONTAINER_NAME=tfstate
az group create --name $RESOURCE_GROUP_NAME --location "UK South"
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)

export ACCOUNT_KEY=$ACCOUNT_KEY

az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"


MSYS_NO_PATHCONV=1 az role assignment create --assignee 605fa8e5-69e7-4511-98b2-ec7e22f52789 --role Owner --scope /subscriptions/f4b1e8d1-13bc-4b3a-aa0a-4c6f6459d9fc/resourceGroups/AtlassianRG

gh secret set ARM_ACCESS_KEY --body $ACCOUNT_KEY

