import subprocess
import json
import csv

# Function to retrieve EC2 instance information
def get_ec2_instance_info():
    instances = []
    next_token = None

    while True:
        command = [
            'aws', 'ec2', 'describe-instances',
            '--output', 'json'
        ]

        if next_token:
            command.extend(['--starting-token', next_token])

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            output = json.loads(result.stdout)

            for reservation in output['Reservations']:
                for instance in reservation['Instances']:
                    print(instance['InstanceId'])

                    instance_data = [
                        instance.get('InstanceId', ""),
                        instance.get('InstanceType', ""),
                        instance['State'].get('Name', ""),
                        instance.get('LaunchTime', ""),
                        instance.get('PrivateIpAddress', ""),
                        instance.get('PublicIpAddress', ""),
                        instance.get('SubnetId', ""),
                        instance.get('VpcId', ""),
                        ','.join( [ sg.get('GroupName', '') for sg in instance.get('SecurityGroups', []) ])
                    ]
                    instances.append(instance_data)

            next_token = output.get('NextToken')

            if not next_token:
                break
        else:
            print("Error:", result.stderr)
            break

    return instances

# Function to write EC2 instance information to a CSV file
def write_to_csv(instances, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Instance Id', 'Instance Type', 'State', 'Launch Time', 'Private IP', 'Public IP', 'Subnet Id', 'VPC Id', 'Instance Profile', 'Security Groups'])
        writer.writerows(instances)

# Main function
def main():
    instances = get_ec2_instance_info()
    write_to_csv(instances, 'ec2_instances.csv')
    print("EC2 instance information saved to ec2_instances.csv")

if __name__ == "__main__":
    main()
