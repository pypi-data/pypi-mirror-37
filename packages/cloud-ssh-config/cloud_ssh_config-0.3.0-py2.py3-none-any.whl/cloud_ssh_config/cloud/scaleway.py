from scaleway.apis import ComputeAPI


class cloud:
    def __init__(self, token, region='ams1'):
        self.region = region
        self.token = token

    def get_hosts(self):
        api = ComputeAPI(region=self.region, auth_token=self.token)
        servers = api.query().servers.get()

        hosts = {}
        for host in servers['servers']:
            if host['state'] == 'running':
                hosts.update(
                    {host['hostname']: host['public_ip']['address']}
                )
        return hosts
