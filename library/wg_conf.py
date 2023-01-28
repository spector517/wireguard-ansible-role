DOCUMENTATION = r'''
---
module: wg_conf

short_description: Load  WireGuard configuration

version_added: "1.0.0"

description: |
    This module allow to load the WireGuard config from .conf files to a YAML-object,

options:
    
    conf_path:
        description: Path to the WireGuard config file (.conf)
        required: true
        type: str

author:
    - Alexander Borunov (@spector517)
'''

EXAMPLES = r'''
- name: Load wg0.conf
  spector517.wireguard.wg_conf:
    conf_path: /etc/wireguard/wg0.conf
'''

RETURN = r'''
message:
    description: Return YAML-object of WireGuard configuration
    type: str
    returned: always
    sample:
        wg_config:
            interface:
                Address: wg.server.url
                PrivateKey: yAnz5TF+lXXJte14tji3zlMNq+hd2rYUIgJBgB3fBmk=
            peers:
                - PublicKey: xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp8Dg=
                  AllowedIPs: 10.9.0.2/32
                - PublicKey: TrMvSoP4jYQlY6RIzBgbssQqY3vxI2Pi+y71lOWWXX0=
                  AllowedIPs: 10.9.0.3/32
'''


from re import findall
from re import sub
from os.path import expanduser

from ansible.module_utils.basic import AnsibleModule


class WGConfig:

    __slots__ = ['interface', 'peers']

    def __init__(self, interface: dict = {}, peers: list[dict] = []) -> None:
        self.interface = interface
        self.peers = peers


    def read_string(self, config_string: str) -> None:
        config_string = sub(r'(#|;).+', '', config_string)
        for match in findall(r'\[.+\]\s*\n[^\[\]]+', config_string):
            lines = match.split('\n')
            section = lines[0].strip()[1:-1]
            peer = {}
            for line in match.split('\n')[1:]:
                if not line:
                    continue
                key, value = line.split('=', 1)
                if section == 'Interface':
                    self.interface.update({key.strip(): value.strip()})
                elif section == 'Peer':
                    peer.update({key.strip(): value.strip()})
            if peer:
                self.peers.append(peer)


def load(filepath: str) -> dict:
    with open(filepath, 'rt', encoding='utf-8') as fd:
        string_config = fd.read()
    config = WGConfig()
    config.read_string(string_config)
    result = {'interface': config.interface}
    if config.peers:
        result.update({'peers': config.peers})
    return result


# def main1():
#     test = load('library/test.conf')
#     print(test)


def main() -> None:
    module_args = {
        'conf_path': {'type': str,'required': True},
    }
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    try:
        path = expanduser(module.params['conf_path'])
        module.exit_json(changed=False, wg_config=load(path))
    except Exception as ex:
        module.fail_json(changed=False, msg=str(ex))


if __name__ == '__main__':
    main()
    # main1()
