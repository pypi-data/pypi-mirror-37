# Copyright (c) 2018 UniquID

import requests
import shlex
import subprocess
import json
import time
import os
import stat
import time
import urllib.request
import shutil
import tarfile
import zipfile
import glob
from Crypto.PublicKey import RSA # pycrypto
import uniquid.core.constants as cons
import uniquid.core.constants_aws as awscons

# constants
_TAB = cons.TXT_TAB
_OUTPUT_DIR = 'uniquid_aws'
_KEYPAIR_FILE_PREFIX = 'aws_ec2_keypair_'
_KEYPAIR_FILE_SUFFIX = '.pem'
_KEYPAIR_FILE_PERMS = stat.S_IRUSR
_KEYPAIR_NAME = 'uniquid-agent-key'
# filename of downloaded AWS agent
_AWS_AGENT_FILE = 'aws-agent-latest.tar.gz'
# agent name prefix
_AWS_AGENT_PREFIX = 'AWS-IOT-UNIQUID-AUTHORIZER-'
# agent tarfile sub-directory
_AGENT_TAR_SUBDIR = 'aws-agent'

# configuration exported as a JSON file
_aws_virtdev_config = {
    'orgId': '',
    'mqttUrl': '',
    'mqttTopic' : '',
    'registryUrl': '',
    'awsAuthorizerName': 'UniquIDCustomAuth',
    'awsPrivateKey': [],
    'awsTokenKey': 'UniquIDToken',
    'awsAgentName': '',
    'awsEndpointAddress': '',
    'network' : 'ltc-regtest'
}

# network map - maps network type from orchestrator value to enum
_LTC_REGTEST = 'ltc-regtest'
_LTC_TESTNET = 'ltc-testnet'
_LTC_MAINNET = 'ltc-mainnet'
_aws_network_map = {
    _LTC_REGTEST: 'litecoinregtest'.casefold(),
    _LTC_TESTNET: 'litecointest'.casefold(),
    _LTC_MAINNET: 'litecoin.main'.casefold()
}

class Deploy:
    """Implements all commands related to AWS deployment of the Uniquid Agent.
    """

    def __init__(self, in_console, in_login_mgr):
        """Initialise an instance of the class.

            in_console -- CliConsole object.
            in_login_mgr -- LoginManager object.
        """
        assert in_console is not None
        assert in_login_mgr is not None
        self._console = in_console
        self._login_mgr = in_login_mgr

    def deploy(self, in_platform):
        """Deploy Uniquid node and custom authorizer lambda function to
            customer's platform.

            Arguments:
            in_platform -- Customer platform identifier.
        """
        # check that user is logged in
        session_key = self._login_mgr.get_session_key()
        if session_key is None:
            self._console.exception(cons.ERR_LOGGED_OUT)
        # verify that the user supplied a supported platform
        if in_platform not in cons.PLATFORMS:
            self._console.exception(cons.ERR_BAD_PLATFORM)
        # retrieve organization information
        url = 'http://{0}:{1}/api/v1/info'.format(
                                            self._login_mgr.get_api_ip(),
                                            self._login_mgr.get_api_port())
        cookies = dict(JSESSIONID=self._login_mgr.get_session_key())
        response = None
        try:
            response = requests.get(url, cookies=cookies)
        except requests.exceptions.ConnectionError:
            self._console.exception(cons.ERR_NO_RESPONSE)
        if (response.status_code == 200 and
                response.json()):
            # assemble orchestrator info
            orch_info = dict()
            orch_info['orgIp'] = self._login_mgr.get_api_ip()
            orch_info['orgPort'] = self._login_mgr.get_api_port()
        elif response.status_code == 401:
            self._console.exception(cons.ERR_LOGIN_REJECTED)
        elif response.status_code == 500:
            self._console.exception(cons.ERR_SERVER_ERROR)
        else:
            self._console.exception(cons.ERR_UNKNOWN_ERROR)
        # check platform is supported
        if in_platform == 'aws':
            self._aws_deploy(orch_info)
        else:
            self._console.exception(cons.ERR_BAD_PLATFORM)

    def _aws_deploy(self, in_orch_info):
        """Deploy the Agent and Lambda function to AWS EC2.

            Arguments:
            in_orch_info -- Dictionary with Orchestrator IP and port.
        """
        step = 1
        # data retrieved
        aws_access_key = None
        aws_secret_key = None
        aws_region = None
        # query user to proceed
        # TODO test on Windows
        if os.name == 'nt':
            self._console.ok('Warning: Un-tested on Windows - use at your own risk.\n')
        self._console.ok('Starting deployment of Uniquid AWS Agent to your Amazon AWS cloud.')
        self._console.ok('The following tools must be installed and configured: awscli, Node.js (>= v8.0), npm, ssh, scp.')
        if not self._console.confirm("Do you want to start the deployment?",
                                 in_default=False):
            self._console.ok(awscons.TXT_AWS_EXIT_EARLY)
            return
        # check awscli is installed
        step = self._print_step(step, 'Check awscli is installed.')
        version_cmd = 'aws --version'
        arg_list = shlex.split(version_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode != 0:
            self._console.error('awscli must be installed.')
            self._console.exception(cons.ERR_MISSING_DEPENDENCY)
        self._console.ok(_TAB + cons.TXT_PASS)
        # check aws client configured - access_key
        step = self._print_step(step, 'Check AWS CLI tool is configured.')
        aws_access_key = self._aws_configure_get('aws_access_key_id')
        aws_secret_key = self._aws_configure_get('aws_secret_access_key')
        aws_region = self._aws_configure_get('region')
        self._console.ok(_TAB + cons.TXT_PASS)
        # check node.js is installed
        step = self._print_step(step, 'Check node.js is installed.')
        version_cmd = 'node --version'
        arg_list = shlex.split(version_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode != 0:
            self._console.error('node.js must be installed.')
            self._console.exception(cons.ERR_MISSING_DEPENDENCY)
        self._console.ok(_TAB + 'node.js version: ' + result.stdout.decode('utf-8'))
        self._console.ok(_TAB + 'node.js version must be >= 8.0')
        # TODO check version of npm meets criteria
        self._console.ok(_TAB + cons.TXT_PASS)
        # check npm is installed
        step = self._print_step(step, 'Check npm is installed.')
        version_cmd = 'npm --version'
        arg_list = shlex.split(version_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode != 0:
            self._console.error('npm must be installed.')
            self._console.exception(cons.ERR_MISSING_DEPENDENCY)
        self._console.ok(_TAB + 'npm version: ' + result.stdout.decode('utf-8'))
        self._console.ok(_TAB + 'npm version must be >= 6.4')
        # TODO check version of npm meets criteria
        self._console.ok(_TAB + cons.TXT_PASS)
        # get the aws account id
        step = self._print_step(step, 'Retrieve AWS Account Id.')
        aws_account_id = self._aws_get_caller_identity('Account')
        self._console.ok(_TAB + cons.TXT_PASS)
        # create or select a security group
        step = self._print_step(step, 'Configure an AWS Security Group.')
        sec_group_name = None
        sec_group_id = None
        sec_groups = self._aws_list_security_groups()
        self._console.ok(_TAB + 'Existing Security Groups:')
        if len(sec_groups) > 0:
            for group in sec_groups:
                self._console.ok(_TAB + '* ' + group['Name'])
        else:
            self._console.ok(_TAB + 'None')
        # give the user the option to create a new security group
        if self._console.confirm("Do you want to create another AWS Security Group?",
                                 in_default=False):
            sec_group_name = self._console.prompt('Enter the name of the new AWS security group name',
                                             in_type=str,
                                             in_default='uniquid-agent-sg',
                                             in_show_default=True)
            for group in sec_groups:
                if sec_group_name in group:
                    self._console.exception(awscons.ERR_AWS_SEC_GROUP_EXISTS)
            # security group created for default aws vpc
            version_cmd = ('aws ec2 create-security-group --group-name ' +
                           sec_group_name +
                           ' --description ' +
                           '\"Uniquid Agent Security Group\"')
            result = self._run_command(version_cmd)
            sec_group_dict = json.loads(result.stdout.decode('utf-8').strip())
            if 'GroupId' in sec_group_dict:
                sec_group_id = sec_group_dict.get('GroupId')
                self._console.ok(awscons.TXT_AWS_SEC_GROUP_CREATED +
                                 sec_group_id)
            else:
                self._console.exception(awscons.ERR_AWS_REPLY_MISSING_DATA + 'GroupId')
        else:
            sec_group_name = self._console.prompt('Enter the name of the existing AWS security group to use',
                                             in_default='',
                                             in_type=str,
                                             in_show_default=False)
            # verify user entered name of an existing security group
            isMatch = False
            for group in sec_groups:
                if sec_group_name == group['Name']:
                    sec_group_id = group['Id']
                    isMatch = True
            if not isMatch:
                self._console.exception(awscons.ERR_AWS_SEC_GROUP_NOT_EXISTS)
        # open ports for security group
        self._console.ok('Incoming TCP ports must be open for the security group. Port numbers: ' + ', '.join(awscons.AWS_SEC_GROUP_PORTS))
        if self._console.confirm('Do you want to open inbound TCP ports of '
                                 'the Security Group ' + sec_group_name + '?',
                                 in_default=False):
            for portnum in awscons.AWS_SEC_GROUP_PORTS:
                portnum_cmd = ('aws ec2 authorize-security-group-ingress ' +
                               '--group-name ' + sec_group_name +
                               ' --protocol tcp --port ' + portnum +
                               ' --cidr 0.0.0.0/0')
                result = self._run_command(portnum_cmd)
                self._console.ok(awscons.TXT_AWS_PORT_OPENED + portnum)
        self._console.ok(_TAB + cons.TXT_PASS)
        # keypair selection/creation
        step = self._print_step(step, 'AWS Key Pair selection/creation.')
        self._console.ok('A Key Pair is required to secure access to the EC2 instance.')
        keypair_path = None
        keypair_name = None
        key_pairs = self._aws_list_key_pairs()
        self._console.ok(_TAB + 'Existing Key Pairs:')
        if len(key_pairs) > 0:
            for keypair in key_pairs:
                self._console.ok(_TAB + '* ' + keypair)
        else:
            self._console.ok(_TAB + 'None')
        if self._console.confirm('Do you want to create a key-pair '
                                 'for the instance?'):
            keypair_cmd = ('aws ec2 create-key-pair --key-name ' +
                           _KEYPAIR_NAME +
                           ' --query \"KeyMaterial\" --output text')
            result = self._run_command(keypair_cmd)
            keypair_path = self._write_keypair_file(
                                    result.stdout.decode('utf-8').strip())
            keypair_name = _KEYPAIR_NAME
        else:
            keypair_path = self._console.prompt('Enter the path of an existing'
                                                ' key-pair file to use for the'
                                                ' new EC2 instance',
                                                in_default='',
                                                in_type=str,
                                                in_show_default=False)
            if (not os.path.exists(keypair_path) or
                    not os.path.isfile(keypair_path) or
                    not os.access(keypair_path, os.R_OK)):
                self._console.exception(awscons.ERR_AWS_KEYPAIR_FILE_READ)
            keypair_name = self._console.prompt('Enter the name of this key '
                                                'pair',
                                                in_default=_KEYPAIR_NAME,
                                                in_type=str,
                                                in_show_default=True)
        if (keypair_name is None or
                len(keypair_name) == 0):
            self._console.exception(awscons.ERR_AWS_INVALID_KEYPAIR_NAME)
        self._console.ok(_TAB + cons.TXT_PASS)
        # aws ec2 instance creation
        ec2_id = None
        step = self._print_step(step, 'AWS EC2 instance creation.')
        if self._console.confirm('Do you want to create a new AWS EC2 Instance'
                                 ' for the Uniquid Agent?',
                                 in_default=False):
            # find a suitable ec2 image to use
            ami_id = None
            self._console.ok('Retrieving list of EC2 image types from Amazon '
                             'AWS. Please wait....')
            # TODO hardcoded Canonical owner id
            aws_cmd = ('aws ec2 describe-images --filters '
                       '\"Name=architecture,Values=x86_64\" '
                       '\"Name=state,Values=available\" '
                       '\"Name=root-device-type,Values=ebs\" '
                       '\"Name=virtualization-type,Values=hvm\" '
                       '\"Name=owner-id,Values=' + awscons.AWS_ID_CANONICAL + '\"')
            result = self._run_command(aws_cmd)
            result_str = result.stdout.decode('utf-8').strip()
            result_json = json.loads(result_str)
            for image in result_json.get('Images'):
                if ('Description' in image and
                       'Canonical' in image.get('Description','') and
                       'Ubuntu' in image.get('Description','') and
                       '18.04 LTS' in image.get('Description','') and
                       'UNSUPPORTED' not in image.get('Description','UNSUPPORTED') and
                       image.get('Public', False) == True and
                       image.get('ImageType','') == 'machine'):
                    ami_id = image.get('ImageId', '')
            if ami_id is None:
                self._console.exception(cons.ERR_NO_AWS_IMAGE)
            self._console.ok(_TAB + 'AWS EC2 image choosen: ' + ami_id)
            # create the instance using choosen image type
            aws_cmd = ('aws ec2 run-instances --image-id ' + ami_id +
                       ' --security-group-ids ' + sec_group_id +
                       ' --count 1 --instance-type t2.micro --key-name ' +
                       keypair_name + ' --tag-specifications \"ResourceType=' +
                       'instance,Tags=[{Key=name,Value=uniquid-agent-cli}]\"' +
                       ' --query \"Instances[0].InstanceId\"')
            result = self._run_command(aws_cmd)
            ec2_id = result.stdout.decode('utf-8').strip()
        else:
            ec2_id = self._console.prompt('Enter the ID of the AWS EC2 '
                                                'instance to be used',
                                                in_default='',
                                                in_type=str,
                                                in_show_default=False)
        self._console.ok(_TAB + cons.TXT_PASS)
        # retrieve the public ip of the ec2 instance
        step = self._print_step(step, 'Query IP address of EC2 instance.')
        ec2_public_ip = None
        aws_cmd = ('aws ec2 describe-instances --instance-ids ' +
                   ec2_id +
                   ' --query \"Reservations[0].Instances[0].PublicIpAddress\"')
        result = self._run_command(aws_cmd)
        ec2_public_ip = result.stdout.decode('utf-8').strip().replace('\"','')
        if (ec2_public_ip is None or
            len(ec2_public_ip) == 0):
            self._console.exception(awscons.ERR_AWS_CANNOT_FIND_INSTANCE +
                                    ec2_id)
        self._console.ok(_TAB + cons.TXT_PASS)
        # wait for instance to run
        step = self._print_step(step, 'Wait for EC2 Instance to Initialize.')
        status = self._aws_get_instance_status(ec2_id)
        while status != 'running':
            self._console.ok(_TAB + awscons.TXT_AWS_WAIT_INSTANCE_RUNNING)
            time.sleep(30)
            status = self._aws_get_instance_status(ec2_id)
        # connect to ec2 instance
        time.sleep(30) # TODO hardcoded delay so login doesn't fail
        step = self._print_step(step, 'Verify login to AWS EC2 instance.')
        linux_cmd = ('ssh -i ' + keypair_path +
                     ' -o \"StrictHostKeyChecking=accept-new\" ubuntu@' +
                     ec2_public_ip + ' \"uname -a && exit 0\"')
        result = self._run_command(linux_cmd, 2, 30)
        self._console.ok(_TAB + cons.TXT_PASS)
        # install java in ec2 instance
        step = self._print_step(step, 'Provision the AWS EC2 instance.')
        # sudo apt-get install default-jdk
        linux_cmd = ('ssh -i ' + keypair_path + ' ubuntu@' + ec2_public_ip +
                     ' \"sudo apt-get -y update &&' +
                     ' sudo apt-get -y install default-jdk &&' +
                     ' java -version && exit 0\"')
        result = self._run_command(linux_cmd, 2, 30)
        self._console.ok(_TAB + cons.TXT_PASS)
        # download the jar file
        step = self._print_step(step, 'Download the Uniquid Agent.')
        package_url = ('http://' + cons.UNIQUID_STATIC_IP + ':' +
                       cons.UNIQUID_STATIC_PORT +
                       awscons.AWS_AGENT_URL_PATH)
        # create the output directory
        if not os.path.isdir(_OUTPUT_DIR):
            os.makedirs(_OUTPUT_DIR)
        target_path = os.path.join(_OUTPUT_DIR, _AWS_AGENT_FILE)
        with urllib.request.urlopen(package_url) as response, \
                open(target_path, 'wb') as outfile:
            shutil.copyfileobj(response, outfile)
        with tarfile.open(target_path, 'r') as tf:
            tf.extractall(_OUTPUT_DIR)
        self._console.ok(_TAB + cons.TXT_PASS)
        # customize the agent configuration
        step = self._print_step(step, 'Customize the Uniquid AWS Agent.')
        orch_props = self._get_orch_properties()
        if orch_props is None:
            self._console.exception(cons.ERR_ORCH_REQ_FAIL)
        config_path = os.path.join(_OUTPUT_DIR, _AGENT_TAR_SUBDIR,
                                   'appconfig.properties')
        appconfig = ''
        with open(config_path, 'r') as cf:
            appconfig = cf.read()
        appconfig = appconfig.replace('NETWORK_PARAMS', orch_props.get('network', '[Error]'))
        appconfig = appconfig.replace('MQTT_BROKER', orch_props.get('mqttBroker', '[Error]'))
        # TODO topic.announce will change to org.id - depends on agent version
        appconfig = appconfig.replace('TOPIC', self._login_mgr.get_org_id() + '/announce')
        appconfig = appconfig.replace('NODE_NAME', _AWS_AGENT_PREFIX + aws_account_id)
        with open(config_path, 'w') as cf:
            cf.write(appconfig)
        self._console.ok(_TAB + cons.TXT_PASS)
        # upload jar to instance and start
        step = self._print_step(step, 'Upload Uniquid Agent to AWS EC2 instance.')
        upload_cmd = 'scp -i ' + keypair_path + ' ' + config_path + ' ubuntu@' + ec2_public_ip + ':appconfig.properties'
        result = self._run_command(upload_cmd, 2, 30)
        # find untarred jar file
        for f in glob.glob(_OUTPUT_DIR + '/**/awsagent*.jar', recursive=True):
            jar_path = f
        upload_cmd = 'scp -i ' + keypair_path + ' ' + jar_path + ' ubuntu@' + ec2_public_ip + ':awsagent.jar'
        result = self._run_command(upload_cmd, 2, 30)
        upload_cmd = ('ssh -i ' + keypair_path + ' ' +
                      ' ubuntu@' + ec2_public_ip +
                      ' \"nohup java -jar awsagent.jar appconfig.properties < /dev/null > /dev/null 2>&1 &\"')
        result = self._run_command(upload_cmd, 2, 30)
        self._console.ok(_TAB + cons.TXT_PASS)
        # update values in javascript
        step = self._print_step(step, 'Customize the AWS Lambda function.')
        lambda_code = ''
        line_a = 'var aws_account = \'' + aws_account_id + '\';\n'
        line_b = 'var aws_region = \'' + aws_region + '\';\n'
        line_c = 'var uniquid_aws_agent = \'http://' + ec2_public_ip + ':8070/api/v1/checkawscontract\';\n'
        lambda_path = os.path.join(_OUTPUT_DIR, _AGENT_TAR_SUBDIR, 'lambda', 'UniquidLambda.js')
        with open(lambda_path, 'r') as f:
            lambda_code = f.read()
        with open(lambda_path, 'w') as f:
            f.write(line_a)
            f.write(line_b)
            f.write(line_c)
            f.write('\n')
            f.write(lambda_code)
        self._console.ok(_TAB + cons.TXT_PASS)
        # install dependencies
        step = self._print_step(step, 'Install Javascript dependencies.')
        original_dir = os.getcwd()
        node_dir = os.path.join(_OUTPUT_DIR, _AGENT_TAR_SUBDIR)
        os.chdir(node_dir)
        result = self._run_command('npm install request')
        self._console.ok(_TAB + cons.TXT_PASS)
        # zip package
        step = self._print_step(step, 'Zip the Lambda function package.')
        modules_path = 'node_modules'
        # TODO add compression
        with zipfile.ZipFile('UniquidLambda.zip', 'w') as zf:
            zf.write(os.path.join('lambda', 'UniquidLambda.js'), arcname='UniquidLambda.js') # FIXME hardcoded
            zf.write(modules_path)
            for f in glob.glob(modules_path + '/**/*', recursive=True):
                zf.write(f)
        os.chdir(original_dir)
        self._console.ok(_TAB + cons.TXT_PASS)
        # create the AWS IAM Execution Role
        step = self._print_step(step, 'Create an AWS IAM Execution Role.')
        cmd = 'aws iam get-role --role-name UniquidLambdaRole'
        arg_list = shlex.split(cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode == 0:
            self._console.ok(_TAB + 'AWS IAM role UniquidLambdaRole already exists. Skipping Role creation.')
        else:
            cmd = 'aws iam create-role --role-name UniquidLambdaRole --assume-role-policy-document \'{\"Version\": \"2012-10-17\", \"Statement\": [ { \"Action\": \"sts:AssumeRole\", \"Effect\": \"Allow\", \"Principal\": { \"Service\": \"lambda.amazonaws.com\" } } ] }\' --description \"Allows Lambda functions to call AWS services on your behalf.\"'
            result = self._run_command(cmd)
        # TODO check output from command
        result_string = result.stdout.decode('utf-8').strip()
        result_json = json.loads(result_string)
        aws_role_arn = result_json.get('Role').get('Arn')
        self._console.ok(_TAB + cons.TXT_PASS)
        # attach AWS IAM policy
        step = self._print_step(step, 'Attach the AWS IAM policy.')
        cmd = 'aws iam attach-role-policy --role-name UniquidLambdaRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        result = self._run_command(cmd)
        self._console.ok(_TAB + cons.TXT_PASS)
        # upload the lambda function
        step = self._print_step(step, 'Upload the Lambda function package.')
        # give time for new role to propagate through AWS
        time.sleep(20)
        cmd = 'aws lambda create-function --function-name UniquidLambda --runtime nodejs8.10 --role ' + aws_role_arn + ' --handler UniquidLambda.handler --zip-file fileb://' + node_dir + '/UniquidLambda.zip --region ' + aws_region
        result = self._run_command(cmd)
        result_string = result.stdout.decode('utf-8').strip()
        result_json = json.loads(result_string)
        aws_function_arn = result_json.get('FunctionArn')
        self._console.ok(_TAB + cons.TXT_PASS)
        # test lambda invocation
        step = self._print_step(step, 'Test the Lambda function invocation.')
        time.sleep(30)
        cmd = 'aws lambda invoke --invocation-type RequestResponse --function-name UniquidLambda --region ' + aws_region + ' --log-type Tail --payload \'{\"key1\":\"value1\", \"key2\":\"value2\", \"key3\":\"value3\"}\' ' + node_dir + '/lambda-out.txt'
        result = self._run_command(cmd)
        result_string = result.stdout.decode('utf-8').strip()
        result_json = json.loads(result_string)
        if result_json.get('StatusCode') != 200:
            self._console.exception(awscons.ERR_AWS_LAMBDA_INVOKE_FAILED)
        self._console.ok(_TAB + cons.TXT_PASS)
        # generate key pair
        step = self._print_step(step, 'Generate Key pair for IoT Authorizer.')
        rsa_keys = RSA.generate(2048)
        rsa_private_key = rsa_keys.exportKey('PEM').decode('utf-8')
        rsa_public_key = rsa_keys.publickey().exportKey('PEM').decode('utf-8')
        with open('virtual_device_key_pair.pem', 'w') as f:
            f.write(rsa_private_key + '\n')
            f.write(rsa_public_key)
            self._console.ok('Key pair file written: virtual_device_key_pair.pem') # FIXME hardcoded path
        self._console.ok(_TAB + cons.TXT_PASS)
        # create authorizer
        step = self._print_step(step, 'Create the IoT Authorizer.')
        # check if authorizer exists already
        cmd = 'aws iot describe-authorizer --authorizer-name UniquIDCustomAuth'
        arg_list = shlex.split(cmd)
        is_authorizer_exists = True
        while is_authorizer_exists:
            result = subprocess.run(arg_list,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            if result.returncode == 0:
                self._console.ok('Warning: AWS IoT Authorizer UniquIDCustomAuth already exists!')
                self._console.ok('Please delete before proceeding....')
                if self._console.confirm('Is it OK to proceed?'):
                    pass
            else:
                is_authorizer_exists = False
                # no authorizer therefore ok to proceed
        cmd = 'aws iot create-authorizer --authorizer-name UniquIDCustomAuth --authorizer-function-arn ' + aws_function_arn + ' --token-key-name UniquIDToken --token-signing-public-keys FIRST_KEY=\"' + rsa_public_key + '\" --status ACTIVE --region ' + aws_region
        result = self._run_command(cmd)
        result_string = result.stdout.decode('utf-8').strip()
        result_json = json.loads(result_string)
        aws_authorizer_arn = result_json.get('authorizerArn')
        self._console.ok(_TAB + cons.TXT_PASS)
        # update permissions
        step = self._print_step(step, 'Update permissions for IoT Authorizer.')
        cmd = 'aws lambda add-permission --function-name UniquidLambda --principal iot.amazonaws.com --source-arn ' + aws_authorizer_arn + ' --statement-id UniquID-Id-123 --action \"lambda:InvokeFunction\"'
        result = self._run_command(cmd)
        self._console.ok(_TAB + cons.TXT_PASS)
        # retrieve the public endpoint of the ec2 instance
        step = self._print_step(step, 'Query AWS IoT Endpoint.')
        iot_endpoint = None
        aws_cmd = ('aws iot describe-endpoint')
        result = self._run_command(aws_cmd)
        iot_string = result.stdout.decode('utf-8').strip()
        iot_json = json.loads(iot_string)
        iot_endpoint = iot_json.get('endpointAddress')
        if (iot_endpoint is None or
            len(iot_endpoint) == 0):
            self._console.exception(awscons.ERR_AWS_CANNOT_FIND_IOT_ENDPOINT)
        self._console.ok(_TAB + cons.TXT_PASS)
        # generate config file for Onboarding server
        step = self._print_step(step, 'Generate virtual device configuration file.')
        _aws_virtdev_config['orgId'] = self._login_mgr.get_org_id()
        _aws_virtdev_config['mqttUrl'] = orch_props.get('mqttBroker', '[Error]')
        _aws_virtdev_config['mqttTopic'] = self._login_mgr.get_org_id() + '/announce' # FIXME work-around # orch_props.get('mqttTopic', '[Error]')
        _aws_virtdev_config['registryUrl'] = 'http://' + self._login_mgr.get_api_ip() + ':8060' # FIXME work-around # orch_props.get('registryUrl', '[Error]')
        _aws_virtdev_config['awsPrivateKey'] = rsa_private_key.split('\n')
        _aws_virtdev_config['awsAgentName'] = _AWS_AGENT_PREFIX + aws_account_id
        _aws_virtdev_config['awsEndpointAddress'] = iot_endpoint
        # map from orchestrator network type to an agreed identifier
        network_type = orch_props.get('network', '').casefold()
        if _aws_network_map.get(_LTC_REGTEST,'[Error]') in network_type:
            _aws_virtdev_config['network'] = _LTC_REGTEST
        elif _aws_network_map.get(_LTC_TESTNET,'[Error]') in network_type:
            _aws_virtdev_config['network'] = _LTC_TESTNET
        else:
            _aws_virtdev_config['network'] = _LTC_MAINNET
        # save virtual device configuration to file
        with open('virtual_device_cfg.json', 'w') as f:
            f.write(json.dumps(_aws_virtdev_config, indent=2))
            self._console.ok('Configuration file written: virtual_device_cfg.json') # FIXME hardcoded path
        self._console.ok(_TAB + cons.TXT_PASS)
        self._console.ok('Deployment of Uniquid AWS Agent is now complete.')

    def _run_command(self, in_command, in_retries=0, in_sleep=0):
        """Run a shell command.

            Arguments:
            in_command -- Full string with command.
            in_retries -- Permitted number of retries before raising an
            exception for an error.
            in_sleep -- Sleep between retries in seconds.
            Returns:
            subprocess.run() return object.
            Throws:
            ClickException if the initial command and all retries failed.
        """
        assert len(in_command) > 0
        assert in_retries >= 0
        assert in_sleep >= 0
        arg_list = shlex.split(in_command)
        self._console.ok(_TAB + 'Running command: ' + in_command)
        num_tries = 0
        result = None
        while ((result is None or
                    result.returncode != 0) and
                num_tries <= (in_retries + 1)):
            if num_tries > 1:
                self._console.ok(_TAB + 'Command failed. Pausing before retry.....')
                time.sleep(in_sleep)
                self._console.ok(_TAB + 'Retry command: ' + in_command)
            result = subprocess.run(arg_list,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            num_tries = num_tries + 1
        if result.returncode != 0:
            self._console.error(result.stderr.decode('utf-8').strip())
            self._console.exception(awscons.ERR_AWS_SHELL_COMMAND_FAILED)
        return result

    def _aws_configure_get(self, in_param_name):
        """
        Query an aws client configuration parameter.

        Arguments:
        in_param_name -- Parameter name to be queried.
        Returns:
        String with parameter value.
        Throws:
        Exception thrown if parameter does not exist or is empty.
        """
        query_cmd = 'aws configure get ' + in_param_name
        arg_list = shlex.split(query_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if (result.returncode != 0 or
                result.stdout.decode('utf-8').strip() == 0):
            self._console.error(in_param_name +
                                ' must be configured in awscli.')
            self._console.exception(awscons.ERR_AWS_NOT_CONFIGURED)
        return result.stdout.decode('utf-8').strip()

    def _aws_get_caller_identity(self, in_param_name):
        """
        Query an aws client configuration parameter.

        Arguments:
        in_param_name -- Parameter name to be queried.
        Returns:
        String with parameter value.
        Throws:
        Exception thrown if parameter does not exist or is empty.
        """
        query_cmd = ('aws sts get-caller-identity --output text --query "' +
                     in_param_name + '"')
        arg_list = shlex.split(query_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if (result.returncode != 0 or
                result.stdout.decode('utf-8').strip() == 0):
            self._console.exception(awscons.ERR_AWS_NOT_CONFIGURED)
        return result.stdout.decode('utf-8').strip()

    def _aws_get_instance_status(self, in_ec2_id):
        """
        Query the status of an EC2 instance.

        Arguments:
        in_ec2_id -- Id of the EC2 instance.
        Returns:
        String with status.
        """
        retval = None
        query_cmd = ('aws ec2 describe-instance-status --output json --instance-ids ' +
                     in_ec2_id)
        arg_list = shlex.split(query_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if (result.returncode != 0 or
                result.stdout.decode('utf-8').strip() == 0):
            self._console.exception(awscons.ERR_AWS_CANNOT_FIND_INSTANCE +
                                    in_ec2_id)
        json_obj = json.loads(result.stdout.decode('utf-8').strip())
        if ('InstanceStatuses' in json_obj and
            len(json_obj['InstanceStatuses']) == 1):
            retval = json_obj.get('InstanceStatuses')[0].get('InstanceState').get('Name')
        return retval

    def _aws_list_security_groups(self):
        """Return a list with names, ids of all security groups.

            Returns:
            List of dictionary objects."""
        retlist = []
        query_cmd = 'aws ec2 describe-security-groups --output json'
        arg_list = shlex.split(query_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if (result.returncode != 0):
            self._console.error(result.stderr.decode('utf-8').strip())
            self._console.exception(awscons.ERR_AWS_SHELL_COMMAND_FAILED)
        else:
            json_obj = json.loads(result.stdout.decode('utf-8').strip())
            if 'SecurityGroups' in json_obj:
                for obj in json_obj.get('SecurityGroups'):
                    sg_obj = {'name': None, 'id': None}
                    sg_obj['Name'] = obj.get('GroupName')
                    sg_obj['Id'] = obj.get('GroupId')
                    retlist.append(sg_obj)
            else:
                self._console.exception(awscons.ERR_AWS_REPLY_MISSING_DATA)
        return retlist

    def _aws_list_key_pairs(self):
        """Return a list with names of all key pairs.

            Returns:
            List of strings with key pair names."""
        retlist = []
        query_cmd = 'aws ec2 describe-key-pairs --output json'
        arg_list = shlex.split(query_cmd)
        result = subprocess.run(arg_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if (result.returncode != 0):
            self._console.error(result.stderr.decode('utf-8').strip())
            self._console.exception(awscons.ERR_AWS_SHELL_COMMAND_FAILED)
        else:
            json_obj = json.loads(result.stdout.decode('utf-8').strip())
            if 'KeyPairs' in json_obj:
                for obj in json_obj.get('KeyPairs'):
                    if 'KeyName' in obj:
                        retlist.append(obj.get('KeyName'))
            else:
                self._console.exception(awscons.ERR_AWS_REPLY_MISSING_DATA)
        return retlist

    # TODO Can data be retrieved from login manager?
    def _get_orch_properties(self):
        """Retrieve properties from Orchestrator.

        Returns:
        Dictionary object with properties.
        """
        # request info from server
        url = 'http://{0}:{1}/api/v1/properties'.format(self._login_mgr.get_api_ip(),
                                                        self._login_mgr.get_api_port())
        cookies = dict(JSESSIONID=self._login_mgr.get_session_key())
        response = None
        retval = None
        try:
            response = requests.get(url, cookies=cookies)
        except requests.exceptions.ConnectionError:
            self._console.exception(cons.ERR_NO_RESPONSE)
        if (response.status_code == 200 and
                response.json()):
            retval = response.json()
        elif response.status_code == 401:
            self._console.exception(cons.ERR_LOGIN_REJECTED)
        elif response.status_code == 500:
            self._console.exception(cons.ERR_SERVER_ERROR)
        else:
            self._console.exception(cons.ERR_UNKNOWN_ERROR)
        return retval

    def _print_step(self, in_step, in_message):
        """
        Print step number and message. Increment the step number.

        Arguments:
        in_step -- Step number.
        in_message -- Step description.
        Returns:
        Incremented step number.
        """
        self._console.ok('Step ' + str(in_step) + ': ' + in_message)
        return in_step + 1

    def _write_keypair_file(self, in_keypair):
        """Write the AWS keypair to the keypair file.

            Arguments:
            in_keypair -- String with key pair from AWS.
            Returns:
            Full path to key pair file on local filesystem.
        """
        fullpath = self._get_keypair_path()
        fd = self._get_file_handle(fullpath, 'w')
        with fd as outfile:
            outfile.write(in_keypair)
            fd.close()
            os.chmod(fullpath, _KEYPAIR_FILE_PERMS)
            self._console.ok(_TAB + awscons.TXT_AWS_KEYPAIR_FILE_WRITTEN +
                             fullpath)
        return fullpath

    def _get_keypair_path(self):
        """Get the full path of the keypair file used to save the keypair.

            Filename includes a time dependant component therefore every
            call to this method could return a different value.

            Returns:
            String with the full path to the keypair file."""
        datetime_id = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        retval = os.path.join(os.getcwd(),
                              _OUTPUT_DIR,
                              (_KEYPAIR_FILE_PREFIX + datetime_id +
                               _KEYPAIR_FILE_SUFFIX))
        return retval

    def _get_file_handle(self, in_fullpath, in_mode='r'):
        """Get a handle to the temporary file that stores the session key.

            Arguments:
            in_fullpath -- Full path to file.
            in_mode -- 'r' to open in read mode. 'w' to open in write mode.
            Returns:
            A valid file handle or None.
        """
        retval = None
        if not (in_mode is 'r' or in_mode is 'w'):
            self._console.exception('Internal: Incorrect file mode specified.')
        # create output dir if doesn't exist
        dir_path = os.path.dirname(in_fullpath)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # if keypair file already exists, use it.
        try:
            retval = open(in_fullpath, in_mode)
        except OSError:
            retval = None
        except (IOError, OSError):
            self._console.exception(awscons.ERR_AWS_KEYPAIR_FILE_CREATE +
                                    in_fullpath)
        return retval
