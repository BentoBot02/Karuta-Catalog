# CloudClass.py
# By: BentoBot02
# holds the cloud class

import boto3

class Cloud:
    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, bucket, cloudfrontURL, header):
        self.s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.bucket = bucket
        self.cloudfrontURL = cloudfrontURL
        self.header = header

    def getBucket(self):
        return self.bucket

    def getCloudfrontURL(self):
        return self.cloudfrontURL

    def addPrivateFile(self, folder, file):
        self.s3.Object(self.bucket, folder + "/" + file).upload_file(file)

    def addPublicFile(self, folder, file):
        self.s3.Object(self.bucket, folder + "/" + file).upload_file(file, ExtraArgs={'ACL': 'public-read'})

    def removeFile(self, folder, file):
        obj = self.s3.Object(self.bucket, folder + "/" + file)
        obj.delete()
    
    def getFile(self, folder, file):
        self.s3.Object(self.bucket, folder + "/" + file).download_file(file)