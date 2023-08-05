# Copyright (c) 2018 UniquID

"""Constant definitions."""

# AWS security group ports
AWS_SEC_GROUP_PORTS = ['22', '8070']
# path to static file containing AWS Agent package
AWS_AGENT_URL_PATH = '/static/awsagent/latest.tar.gz'

# error messages for AWS
ERR_AWS_NOT_CONFIGURED = 'AWS CLI tool is not configured. Halting command.'
ERR_AWS_QUERY_ACCOUNT = 'AWS account identifier not retrieved.'
ERR_AWS_REPLY_MISSING_DATA = 'Missing data from reply to AWS CLI command. Missing: '
ERR_AWS_SEC_GROUP_EXISTS = 'AWS Security Group already exists.'
ERR_AWS_SEC_GROUP_NOT_EXISTS = 'AWS Security Group does not exist.'
ERR_AWS_KEYPAIR_FILE_CREATE = 'Error creating AWS EC2 key pair file: '
ERR_AWS_KEYPAIR_FILE_READ = 'Error reading AWS EC2 key pair file: '
ERR_AWS_INVALID_KEYPAIR_NAME = 'Invalid name for EC2 key pair.'
ERR_AWS_CANNOT_FIND_INSTANCE = 'Cannot find EC2 instance: '
ERR_AWS_NO_EC2_IMAGE = 'Cannot find a suitable EC2 image.'
ERR_AWS_SHELL_COMMAND_FAILED = 'Shell command returned an error.'
ERR_AWS_CANNOT_FIND_IOT_ENDPOINT = 'Cannot find AWS IoT Endpoint'
ERR_AWS_LAMBDA_INVOKE_FAILED = 'Failed to invoke the AWS Lambda function.'

# aws deploy dialogs
TXT_AWS_SEC_GROUP_CREATED = 'AWS Security Group created. Id: '
TXT_AWS_PORT_OPENED = 'AWS Security Group inbound TCP port opened: '
TXT_AWS_KEYPAIR_FILE_WRITTEN = 'AWS Key Pair file saved: '
TXT_AWS_EXIT_EARLY = 'User terminated deploy process.'
TXT_AWS_WAIT_INSTANCE_RUNNING = 'Waiting on EC2 instance to start running.'

# amazon aws id of canonical
AWS_ID_CANONICAL = '099720109477'
