#!/bin/sh

echo "Deploying cfn stack..."
aws cloudformation create-stack --stack-name workshop-cfn --template-body file://cfn/groups_and_policies.yml --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait stack-create-complete --stack-name workshop-cfn 

for ((num = 1; num <= $1; num++)); do
	echo "Creating user: attendant"$num
	aws iam create-user --user-name=attendant$num
	aws iam create-login-profile --user-name attendant$num --password $2 --password-reset-required
	aws iam add-user-to-group --user-name attendant$num --group-name AttendantGroup
done
