"""A configuration settings module."""

from os import environ

ANSIBLE_HOME_DIRECTORY = '.ansible'
ANSIBLE_REQUIREMENTS_FILE = 'requirements.yml'
ANSIBLE_PLAYBOOKS_DIRECTORY = 'playbooks'
ANSIBLE_INVENTORIES_DIRECTORY = 'inventories'
ANSIBLE_PLAYBOOK_FILE = 'deploy.yml'
ANSIBLE_VAULT_FILE = 'bin/open-vault'

ANSIBLE_INVENTORY_FILE = 'inventory'
ANSIBLE_ROLE_PATHS = [
    'external-roles',
]

PROJECT_PLAY_REPOSITORY_URL = 'https://git.coop/aptivate/ansible-plays/{}-play'
PROJECT_APP_REPOSITORY_URL = 'https://git.coop/aptivate/{}'

ROLE_TEMPLATE_URL = 'https://git.coop/aptivate/templates/role'
PLAY_TEMPLATE_URL = 'https://git.coop/aptivate/templates/play'

APTIVATE_CLI_MYSQL_PASS = 'APTIVATE_CLI_MYSQL_PASS'
APTIVATE_CLI_SUDO_PASS = 'APTIVATE_CLI_SUDO_PASS'
APTIVATE_CLI_PASS_DIR = 'APTIVATE_CLI_PASS_DIR'

APTIVATE_CLI_KANBANTOOL_API_TOKEN = 'Internal/Infrastructure/KANBANTOOL_API_TOKEN'  # noqa
KANBANTOOL_OUTREACH_BOARD_ID = 41725
KANBANTOOL_OUTREACH_CONVERSATIONS_STAGE_ID = 336375
KANBANTOOL_BASE_URI = 'https://aptivate.kanbantool.com/api/v3/'

# A variable we can rely on to be exposed in the environment
# https://docs.gitlab.com/ee/ci/variables/#predefined-variables-environment-variables
IS_GITLAB_CI = environ.get('GITLAB_CI', False)
