import os

profile_path = os.path.expanduser("~/.local/share/profile")

def check_profile() -> str:
    '''
    File contains 'work' or 'private'
    '''
    with(open(profile_path, 'r')) as f:
        content = f.read()
        f.close()
        return content