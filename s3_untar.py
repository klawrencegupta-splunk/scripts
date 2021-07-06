#Simple script using BOTO3 to prompt the user for a bucket name/access and secret key and then downloads all .tar.gz/.tgz files to a folder
# and extracts them automatically to a subfolder called "full"
from boto3.session import Session
import os
import tarfile
import sys


bucket_name = input ("Bucket Name :"+'\n')
print(bucket_name)

access_key_id = input ("AWS Access Key :"+'\n')
print(access_key_id)

secret_access_key = input ("AWS Secret Key :"+'\n')
print(secret_access_key)

folder='data'
destination_path='/downloads'
full_data_path='/downloads/full/'
diag_files = []

def sync_s3_folder(access_key_id,secret_access_key,bucket_name,folder,destination_path): 
    session = Session(aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
    s3 = session.resource('s3')
    your_bucket = s3.Bucket('bucket')
    for s3_file in your_bucket.objects.all():
        if folder in s3_file.key:
            file=os.path.join(destination_path,s3_file.key.replace('/','\\'))
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            your_bucket.download_file(s3_file.key,file)

def untar(fname,full_data_path):
    if fname.endswith(".gz"):
       print(fname) 
       tar = tarfile.open(fname, "r:gz")
       tar.extractall(full_data_path)
       tar.close()
    elif fname.endswith(".tar"):
       tar = tarfile.open(fname, "r:")
       tar.extractall(full_data_path)
       tar.close()


#Download anything in the data folder

if __name__ == "__main__":
    sync_s3_folder(access_key_id,secret_access_key,bucket_name,folder,destination_path)
    scandir_iterator = os.scandir(destination_path)
    for item in scandir_iterator :
       if os.path.isfile(item.path):
          print(item.name)
          fname = destination_path+item.name
          untar(fname,full_data_path)
