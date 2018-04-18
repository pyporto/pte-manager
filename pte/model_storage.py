import sh
from pte import settings


git = sh.git.bake(_cwd=settings.MODEL_STORAGE_ROOT)


def commit(message='Update list of events'):
    git.add('--', 'events', 'misc')
    ret = git.status('-s', '--', 'events', 'misc')
    if ret.strip():
        git.commit(message=message)


def push():
    git.push()


def status():
    print(git.status('-s', '--', 'events', 'misc'))
