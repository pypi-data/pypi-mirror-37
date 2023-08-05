"""A configuration settings module."""

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

APTIVATE_CLI_MYSQL = 'APTIVATE_CLI_MYSQL'
APTIVATE_CLI_SUDO = 'APTIVATE_CLI_SUDO'
APTIVATE_CLI_PASS_DIR = 'APTIVATE_CLI_PASS_DIR'

APTIVATE_CLI_KANBANTOOL_API_TOKEN = 'Internal/Infrastructure/KANBANTOOL_API_TOKEN'  # noqa
KANBANTOOL_OUTREACH_BOARD_ID = 41725
KANBANTOOL_OUTREACH_CONVERSATIONS_STAGE_ID = 336375
KANBANTOOL_BASE_URI = 'https://aptivate.kanbantool.com/api/v3/'
