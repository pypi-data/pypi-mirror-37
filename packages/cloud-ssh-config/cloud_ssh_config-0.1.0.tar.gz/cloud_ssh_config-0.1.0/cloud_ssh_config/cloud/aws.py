import boto3


class cloud:
    def get_hosts(self):
        client = boto3.client('ec2')
        instances = client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        '*'
                    ]
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ],
            MaxResults=100,
        )
        del client

        hosts = {}
        for host in instances['Reservations']:
            if 'PublicIpAddress' in host['Instances'][0]:
                for tag in host['Instances'][0]['Tags']:
                    if tag['Key'] == 'Name':
                        hosts.update(
                            {tag['Value']: host['Instances'][0]['PublicIpAddress']}
                            )
        return hosts
