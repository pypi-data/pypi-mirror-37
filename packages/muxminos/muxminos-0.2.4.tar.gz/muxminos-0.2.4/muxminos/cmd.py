import os
import sys
import git
import json
import fire
import yaml
import logging
from os.path import expanduser
from configobj import ConfigObj

log_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=log_format)
logger = logging.getLogger('muxminos')
logger.setLevel(logging.INFO)


def local_config():
    config_dirs = [os.path.join(expanduser("~"), ".config", "xiaomi", "config"), os.path.join(
        expanduser("~"), ".config", "fds", "client.config")]
    for config_dir in config_dirs:
        if not os.path.exists(config_dir):
            if not (logger is None):
                logger.debug(
                    "local config not exist [" + str(config_dir) + "]")
        else:
            if not (logger is None):
                logger.debug("use config from [" + str(config_dir) + "]")
            with open(config_dir) as f:
                return json.load(fp=f)
    return {}


class MuxMinos(object):
    def __init__(self):
        self.__config = local_config()
        if 'xiaomi_username' not in self.__config:
            logger.error('''Please setup ~/.config/xiaomi/config file
Put this message into ~/.config/xiaomi/config file, and replace with correct message.
{
...
  "xiaomi_username": "your_name"
...
}
                ''')
            sys.exit(0)
        if 'MINOS1_CONFIG_LOCATION' not in os.environ or 'MINOS2_CONFIG_LOCATION' not in os.environ:
            logger.error('Please setup MINOS1_CONFIG_LOCATION and MINOS2_CONFIG_LOCATION os environment')
            sys.exit(0)
        self.__minos1 = os.environ['MINOS1_CONFIG_LOCATION']
        self.__minos2 = os.environ['MINOS2_CONFIG_LOCATION']
        self.__sub_config_path = 'xiaomi-config/conf/'
        username = self.__config['xiaomi_username']
        self.__relay_commands = username + "@relay.xiaomi.com"
        self.__tmuxinator_config = os.path.join(
            expanduser("~"), '.config', 'tmuxinator')
        if not os.path.exists(self.__tmuxinator_config):
            os.mkdir(self.__tmuxinator_config)

    def u(self):
        self.__git_update_config(self.__minos1)
        self.__git_update_config(self.__minos2)

    def __git_update_config(self, config_path):
        logger.info("Updating git repo for " + config_path)
        repo = git.Repo(config_path)
        o = repo.remotes.origin
        o.pull()
        logger.info("Done")

    def g(self, service='fds'):
        paths = self.__check_and_get_paths(service)
        regions = self.__check_and_get_regions(paths)
        for k, v in regions.items():
            self.__generate_4region(k, v)

    def __check_and_get_paths(self, service):
        configs = [
            self.__get_real_config_path(self.__minos1),
            self.__get_real_config_path(self.__minos2)]
        paths = []
        for path in configs:
            path = os.path.join(path, service)
            if not os.path.exists(path):
                logger.warning(path + "is not exists")
            else:
                paths.append(path)
        return paths

    def __check_and_get_regions(self, paths):
        regions = {}
        for path in paths:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if os.path.splitext(file)[1] == '.cfg':
                        restserver = ConfigObj(os.path.join(path, file)).get('restserver')
                        hosts = []
                        if restserver is not None:
                            for key in restserver:
                                if key.startswith('host'):
                                    hosts.append(restserver[key])
                            regions[os.path.splitext(file)[0]] = hosts
                    elif os.path.splitext(file)[1] == '.yaml':
                        try:
                            with open(os.path.join(path, file)) as f:
                                hosts = yaml.load(f).get('jobs').get('restserver').get('hosts')
                                regions[os.path.splitext(file)[0]] = hosts
                        except Exception as e:
                            logger.warning(e)
                break
        return regions

    def __generate_4region(self, region_name, hostlist):
        logger.info("Generating configuration file for " + region_name)
        y = {
            'name': '',
            'windows': []
        }
        y['name'] = region_name
        index = 0
        win_name = ''
        block = {
            'layout': 'even-vertical',
            'panes': []
        }
        for host in hostlist:

            block['panes'].append(
                {host: ['ssh ' + self.__relay_commands, host, 'cd /home/work/app/nginx/logs/']})
            index = index + 1
            win_name = win_name + ('' if win_name == '' else '-') + host.split('.')[0].split('-')[2]
            if index == 4:
                y['windows'].append({win_name: block})
                block = {
                    'layout': 'even-vertical',
                    'panes': []
                }
                index = 0
                win_name = ''
        y['windows'].append({win_name: block})
        with open(os.path.join(self.__tmuxinator_config, region_name + ".yml"), 'w') as f:
            yaml.dump(y, f, default_flow_style=False)

    def __get_real_config_path(self, p):
        return os.path.join(p, self.__sub_config_path)


def main():
    fire.Fire(MuxMinos)


if __name__ == '__main__':
    main()
