from setuptools import setup

setup(
    name='dodo_deploy_commands',
    version='0.1.1',
    description='Deployment related Dodo Commands',
    url='https://github.com/mnieber/dodo_deploy_commands',
    download_url='https://github.com/mnieber/dodo_deploy_commands/tarball/0.1.1',
    author='Maarten Nieber',
    author_email='hallomaarten@yahoo.com',
    license='MIT',
    packages=['dodo_deploy_commands', ],
    package_data={
        'drop-in': [
            '*.yaml',
            '*.md',
            'deploy-tools/docker/Dockerfile',
            'ssh-agent/docker/Dockerfile',
        ]
    },
    entry_points={},
    install_requires=[],
    zip_safe=False)
