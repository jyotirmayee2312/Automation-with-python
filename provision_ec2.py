import subprocess
import json
import boto3

def update_terraform_file(instance_type, ami):
    with open("ec2_instance.tf", "r") as file:
        tf_content = file.read()

    data = json.loads(tf_content)

    data["resource"]["aws_instance"]["ec2_instance"]["instance_type"] = instance_type
    data["resource"]["aws_instance"]["ec2_instance"]["ami"] = ami

    with open("ec2_instance.tf", "w") as file:
        json.dump(data, file, indent=2)

session = boto3.Session(
    aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY',
    region_name='us-east-1'
)

ec2_client = session.client('ec2')

response = ec2_client.describe_images(
    Owners=['amazon'],
    Filters=[
        {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*']},
        {'Name': 'state', 'Values': ['available']}
    ]
)

sorted_images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
latest_ami_id = sorted_images[0]['ImageId']

update_terraform_file("t2.micro", latest_ami_id)

subprocess.run(["terraform", "init"])
subprocess.run(["terraform", "apply", "-auto-approve"])

