import os
import logging
import logging.config
import yaml

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
default_log_path = os.path.join(project_root, 'logs', 'win_logs.log')
default_config_path = os.path.join(project_root, 'configs', 'logging_config.yaml')

key_map = {
    '$ROOT':project_root,
}

def _apply_keywords(dict_):
    for k, v in dict_.items():
        if isinstance(v, dict):
            _apply_keywords(v)
        else:
            for key,val in key_map.items():
                dict_[k] = v.replace(key,val) if isinstance(v, str) else v



def configure_logging(config_path=default_config_path, fall_back_level=logging.DEBUG, env_key='LOG_CONFIG'):
    path = config_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
            _apply_keywords(config)
            logging.config.dictConfig(config)
    else:
        _do_basic(fall_back_level)

def _do_basic(fall_back_level):
    logging.basicConfig(level=fall_back_level)


def get_logger(name):
    configure_logging()
    return logging.getLogger(name)
