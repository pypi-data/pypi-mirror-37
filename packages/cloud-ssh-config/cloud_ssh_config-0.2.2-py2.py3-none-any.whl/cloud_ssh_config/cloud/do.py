import digitalocean


class cloud:
    def __init__(self, token):
        self.manager = digitalocean.Manager(token=token)

    def get_hosts(self):
        my_droplets = self.manager.get_all_droplets()

        hosts = {}
        for host in my_droplets:
            if host.ip_address:
                hosts.update(
                    {host.name: host.ip_address}
                    )
        return hosts
