import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def uploadMetars(filename):
    try:
        print("Starting uploadMetars function...")

        # Retrieve the connection string for use with the application. The storage
        # connection string is stored in an environment variable on the machine
        # running the application called AZURE_STORAGE_CONNECTION_STRING. If the environment variable is
        # created after the application is launched in a console or with Visual Studio,
        # the shell or application needs to be closed and reloaded to take the
        # environment variable into account.
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a blob client using the local file name as the name for the blob
        remote_file_name = 'AviationWeather\\' + filename
        blob_client = blob_service_client.get_blob_client(container='$web', blob= remote_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + filename)

        # Upload the created file
        with open(file=filename, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    except Exception as ex:
        print('Exception:')
        print(ex)

def main():
    uploadMetars('metars.json')

if __name__ == "__main__":
  
    # calling main function
    main()