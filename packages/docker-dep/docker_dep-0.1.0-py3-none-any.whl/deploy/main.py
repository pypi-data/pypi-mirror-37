import os
import json
import subprocess

FILENAME = 'deploy_settings.json'
SETTINGS_KEYS = ('server', 'registry', 'image', 'tag')


def update_settings(settings):
    with open(FILENAME, 'w') as f:
        f.write(json.dumps(settings))


def ask_settings(settings):
    for key in SETTINGS_KEYS:
        if key not in settings or not settings[key]:
            print('{}: '.format(key.capitalize()), end='')
            value = input()
            settings[key] = value
    return settings


def get_settings():
    current_settings = {}
    if os.path.exists(FILENAME):
        with open(FILENAME) as settings:
            try:
                current_settings = json.loads(settings.read())
            except json.decoder.JSONDecodeError:
                pass
    current_settings = ask_settings(current_settings)
    update_settings(current_settings)
    return current_settings


def deploy():
    settings = get_settings()
    server, registry, image, tag = (settings[key] for key in SETTINGS_KEYS)

    def image_name(separator):
        return '{}{}{}'.format(image, separator, tag)

    subprocess.call(['docker', 'build', '-t', image_name(':'), '.'])
    subprocess.call(['docker', 'tag', image_name(':'), '{}/{}'.format(registry, image_name(':'))])
    subprocess.call(['docker', 'push', '{}/{}'.format(registry, image_name(':'))])

    ssh_command = ' && '.join([
        ' '.join(['docker', 'pull', '{}/{}'.format(registry, image_name(':'))]),
        ' '.join(['(docker', 'stop', image_name('_'), '||', 'true)']),
        ' '.join(['(docker', 'rm', image_name('_'), '||', 'true)']),
        'clear',
        ' '.join(['docker', 'run', '-it', '--name', image_name('_'), '{}/{}'.format(registry, image_name(':'))])
    ])
    subprocess.call(['ssh', '-t', 'root@{}'.format(server), ssh_command])
