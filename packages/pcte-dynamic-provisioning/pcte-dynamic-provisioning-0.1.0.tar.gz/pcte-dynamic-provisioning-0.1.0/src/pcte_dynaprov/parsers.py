# STDLIB Imports
import csv
import json
import queue
import ipaddress
import configparser
from uuid import uuid4

# 3rd Party Imports
import yaml

# Local Imports
from pcte_dynaprov import parselog


class ParseBase:
    def __init__(self):
        self.output_filename = None
        self.direct_to_vmare = False
        self.direct_to_lxc = False
        self.direct_to_lxd = False
        self.direct_to_k8s = False
        self.direct_to_docker = False
        self.simspace_yaml__meta_type = 'PCTE/Environment'
        self.simspace_yaml_meta_version = '1.0'
        self.simspace_yaml_meta_name = 'PCTE Grey'
        self.ipaddresses = queue.Queue()

    def load_usable_ipaddresses(self, config):
        if config is not None:
            for i in config['config']['networking']:
                for ii in list(ipaddress.ip_network(i['subnet']).hosts()):
                    if ii == ipaddress.ip_address(i['gateway']):
                        pass
                    else:
                        self.ipaddresses.put(ii)

    def _get_usable_ip_address(self):
        r = str(self.ipaddresses.get())
        return r

    def simspace_out(self, config):
        if config is not None:
            nets = []
            for i in config['config']['networking']:
                self.netName = i['name']
                self.netSubnet = i['subnet']
                self.netDefaultGateway = i['gateway']
                self.netUuid = str(uuid4())
                nets.append(
                    {
                        'defaultGateway': self.netDefaultGateway,
                        'key': self.netUuid,
                        'name': self.netName,
                        'subnet': self.netSubnet,
                    }
                )
            vms = []
            for i in config['config']['services']:
                iface = []
                for ii in range(0, len(i['vNIC'])):
                    if i['vNIC'][ii]['ipv4Address'] == 'auto':
                        self.netIpaddr = self._get_usable_ip_address()
                    else:
                        self.netIpaddr = i['vNIC'][ii]['ipv4Address']
                    iface.append(
                        {
                            'ip': self.netIpaddr,
                            'subnet': self.netUuid
                        }
                    )
                svc = []
                vmSpec = {
                    'cpuCount': i['vCPU']['count'],
                    'description': i['name'],
                    'interfaces': iface,
                    'memoryMb': i['vRAM'],
                    'name': i['name'],
                    'template': i['vmTemplate'],
                    'services': [{'name': i['name']}]
                }
                vms.append(vmSpec)

            spec = {
                'fileType': self.simspace_yaml__meta_type,
                'fileVersion': self.simspace_yaml_meta_version,
                'name': self.simspace_yaml_meta_name,
                'topology': {
                    'vms': vms,
                    'subnets': nets,
                    'users': []
                }
            }

            y = yaml.dump(spec, default_flow_style=False)
            self.output_filename.write(y)

        else:
            parselog.error(f'[ERROR] - No configuration loaded')
            pass


class CSVParser(ParseBase):
    def __init__(self, data=None, outfile_name=None):
        super().__init__()
        self.data = data
        self.outfile_name = outfile_name
        if self.data is not None:
            self.load_usable_ipaddresses(self._parse())
            self.simspace_out(self._parse())

    def _parse(self):
        parselog.info('Starting CSV parser')
        try:
                c = csv.DictReader(self.data)
                return c
        except Exception as e:
            parselog.error(f'Exception occurred while parsing the CSV data ... {e}')


class INIParser(ParseBase):
    def __init__(self, data=None, outfile_name=None):
        super().__init__()
        self.data = data
        self.outfile_name = outfile_name
        if self.data is not None:
            self.load_usable_ipaddresses(self._parse())
            self.simspace_out(self._parse())

    def _parse(self):
        parselog.info('Starting INI parser')
        try:
            config = configparser.ConfigParser()
            c = config.read(self.data)
            return c
        except Exception as e:
            parselog.error(f'Exception occurred while parsing the INI data ... {e}')


class JSONParser(ParseBase):
    def __init__(self, data=None, outfile_name=None):
        super().__init__()
        self.data = data
        self.outfile_name = outfile_name
        if self.data is not None:
            self.load_usable_ipaddresses(self._parse())
            self.simspace_out(self._parse())

    def _parse(self):
        parselog.info('Starting JSON parser')
        try:
            c = json.loads(self.data)
            return c
        except Exception as e:
            parselog.error(f'Exception occurred while parsing the INI data ... {e}')


class YAMLParser(ParseBase):
    def __init__(self, data=None, outfile_name=None):
        super().__init__()
        self.data = data
        self.output_filename = outfile_name
        if self.data is not None:
            self.load_usable_ipaddresses(self._parse())
            self.simspace_out(self._parse())

    def _parse(self):
        parselog.info('Starting YAML parser')
        try:
            c = yaml.load(self.data)
            return c
        except Exception as e:
            parselog.error(f'Exception occurred while parsing the YAML data ... {e}')

