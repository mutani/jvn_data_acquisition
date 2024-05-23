import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='JVM_confirmation',
    version='0.0.1',
    description='JVM情報取得',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'JVM_confirmation = JVM_confirmation.main:main'
        ]
    }
)