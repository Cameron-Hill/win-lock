import yaml
from win_lock.log_manager import get_logger
logger = get_logger(__name__)

def get_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
