# pip install boto3
# pip install cft-deploy
# python create_accounts.py test C:\\Users\\infoalchemy2\\Documents\\make_workshop_env-master\\cfn\\groups_and_policies.yml 10
# Username: attendantN
# Password: 1CanDoThis!
import boto3
import time
import sys


def make_accounts(attendees_number):
    # Create IAM client
    iam = boto3.client('iam')
    attach_group = boto3.client('iam')

    # Specify the number of users (should be - 1; attendant numbers start at 1)
    var = int(attendees_number)
    
    # Loop through the 
    for i in range(0, var):
        username = "attendant" + str(i)

        # Create user
        response = iam.create_user(UserName=username)
        
        # Attach created user to group
        final = attach_group.add_user_to_group(GroupName="AttendantGroup", UserName=username)
        
        # Create login profile (password can be reset)
        login_profile = iam.create_login_profile(
            UserName=username,
            Password="1CanDoThis!",
            PasswordResetRequired=True
        )
        print("Creating: {}".format(username))
    return True

def check_cf_status(stack_name):
    cloudformation = boto3.client('cloudformation')

    is_cf_running = True

    while is_cf_running:
        stack = cloudformation.describe_stacks(StackName=stack_name)
        time.sleep(3)
        status = stack['Stacks'][0]['StackStatus']
        print(status)

        if status == 'CREATE_COMPLETE':
            is_cf_running = False
            print("Stack Creation Complete...")
            time.sleep(5)
            return True
            break
        else:
            return False

def create_cf_stack(stack_name, template_file):
    
    cf = boto3.client('cloudformation')
    
    with open(template_file, 'r') as cf_file:
        cft_template = cf_file.read()
        
        response = cf.create_stack(
            StackName=stack_name,
            TemplateBody=cft_template,
            Capabilities=['CAPABILITY_NAMED_IAM']
        )
    
    status = cf.describe_stack_events(
        StackName=stack_name
    )
    
    events = status['StackEvents']
    
    check_cf_status(stack_name)
    
    return True
    
# Pass Arguments:
#  RUN 
    #   python create_accounts.py --stack_name --template_file --n
## stack_name = specify the desired name of the stack
## template_file = specify the path of the .yml file
## attendees = specify the number of attendees to be created

def main(stack_name, template_file, attendees):

    try:
        hasCreated = create_cf_stack(stack_name, template_file)
        if hasCreated:
            make_accounts(attendees)
    except Exception as e:
        print(e)
    else:
        print("Couldn't create stack..")
        
if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        print("This function requires 3 arguments to be passed. Kindly check.")
        print("Please input arguments for: Stack Name, Location of .yml file, Number of Attendees.")
        time.sleep(5)