from pathlib import Path

PROJECTDIR_PATH = Path(__file__).parent.parent
RESOURCES_PATH = PROJECTDIR_PATH / 'resources'
PROJECTDIR = str(PROJECTDIR_PATH)
TESTSUITESDIR = str(PROJECTDIR_PATH / 'tests')
