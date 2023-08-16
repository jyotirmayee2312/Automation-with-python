## Automating EC2 Instance Provisioning on AWS Using Python, Boto3, and Terraform (On Ubuntu)

Hey there, fellow techie! Have you ever wished for a magical way to create an EC2 instance on AWS without the manual labor? Well, you're in luck! We're about to embark on a journey of automation using the dynamic trio: Python, Boto3, and Terraform. And guess what? We're doing this on Ubuntu. So, buckle up and let's dive right in.

### What You Need

First things first, make sure your Ubuntu setup is ready for this adventure:

1. **AWS Account:** If you don't already have one, head over to AWS and create an account. You'll need access keys to communicate with AWS programmatically.
2. **Python and Boto3:** Lucky for us, Python comes pre-installed on Ubuntu. But we need to get Boto3, the AWS SDK for Python. Open your terminal and type:
   ```bash
   pip3 install boto3
   ```
3. **Terraform:** Ubuntu makes it easy-peasy to get Terraform too. Open that trusty terminal and enter:
   ```bash
   sudo apt-get update
   sudo apt-get install terraform
   ```

### Step 1: Setting Up AWS Credentials

Before we start, let's ensure AWS recognizes us. Here's what you do:

1. Create an IAM user on AWS with programmatic access and the necessary EC2 permissions.
2. Open your terminal and set your AWS credentials as environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=<your-access-key-id>
   export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
   export AWS_DEFAULT_REGION=<desired-region>
   ```
   
### Step 2: EC2 Instance Blueprint with Terraform

Alright, let's lay the groundwork using Terraform. Create a file named `ec2_instance.tf` and let's work some Terraform magic:

```hcl
provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "ec2_instance" {
  ami           = "ami-0da59f1af71ea4ad2"
  instance_type = "t2.micro"
  key_name      = "aws_login"
}
```

### Step 3: Python Script to Rule Them All

Now, let's bring in Python and Boto3 to orchestrate this symphony of automation. Create a file named `provision_ec2.py` and paste in this enchanting script:

```python
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
```

### Step 4: Let the Magic Begin!

It's showtime! Here's how you set your magic spell into motion:

1. Open your terminal on Ubuntu and navigate to the directory containing your `provision_ec2.py` script and the `ec2_instance.tf` file.
2. Summon the spirits of automation by typing:
   ```bash
   python3 provision_ec2.py
   ```

Voila! Watch as the script dances with Terraform and Boto3 to conjure an EC2 instance right before your eyes. Your AWS-powered creation will come to life, all thanks to your coding prowess!

### In Conclusion

You've just embarked on an enchanting journey into the realm of automation using Python, Boto3, and Terraform—right here on your trusty Ubuntu setup. Remember, the possibilities are endless with this trio, so keep exploring and automating your way to success. Happy coding, magician! 🎩🪄

P.S. Don't forget to give your creation a cool name, like "Automagical EC2 Conjurer." 😉
