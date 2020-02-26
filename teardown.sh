#!/bin/sh
for ((num = 1; num <= $1; num++)); do
    echo "Delete user: attendant"$num
    aws iam remove-user-from-group --group-name=AttendantGroup --user-name=attendant$num
    aws iam delete-login-profile --user-name=attendant$num
    aws iam delete-user --user-name=attendant$num
done

echo "Deleting cf stack... Please Ctrl-C if it's taking a long time."
aws cloudformation delete-stack --stack-name workshop-cfn
aws cloudformation wait stack-delete-complete

echo "Now nuking account..."
bin/aws-nuke -c config/nuke-config.yaml --force --no-dry-run
