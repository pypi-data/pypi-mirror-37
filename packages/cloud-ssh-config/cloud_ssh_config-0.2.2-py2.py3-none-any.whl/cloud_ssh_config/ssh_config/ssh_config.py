import six


class config:
    def __init__(self, user='ubuntu', prefix='', key='~/.ssh/id_rsa'):
        self.user = user
        self.prefix = prefix
        self.key = key

    def get_config(self, hosts):
        for host, ip in six.iteritems(hosts):
            print('Host ' + str(self.prefix) + host)
            print('    HostName ' + ip)
            print('    User ' + self.user)
            print('    IdentityFile ' + self.key)
            print('')
        return True
