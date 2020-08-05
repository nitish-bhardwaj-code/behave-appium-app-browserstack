from appium import webdriver
from browserstack.local import Local
import os, json

config_file_path = os.path.join(os.path.dirname(__file__), '..', "config.json")
print("Path to the config file = %s" % (config_file_path))
with open(config_file_path) as config_file:
    CONFIG = json.load(config_file)

TASK_ID = int(os.environ['TASK_ID']) if 'TASK_ID' in os.environ else 0

BROWSERSTACK_USERNAME = os.environ['BROWSERSTACK_USERNAME'] if 'BROWSERSTACK_USERNAME' in os.environ else CONFIG['username']
BROWSERSTACK_ACCESS_KEY = os.environ['BROWSERSTACK_ACCESS_KEY'] if 'BROWSERSTACK_ACCESS_KEY' in os.environ else CONFIG['access_key']

def before_feature(context, feature):
    desired_capabilities = CONFIG['capabilities']
    desired_capabilities['device'] = CONFIG['environments'][TASK_ID]['device']
    context.browser = webdriver.Remote(
        desired_capabilities=dict(desired_capabilities),
        command_executor="http://%s:%s@%s/wd/hub" % (BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, CONFIG['server'])
    )

def after_feature(context, feature):
    context.browser.quit()
