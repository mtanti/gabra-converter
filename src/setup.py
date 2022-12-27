'''
Use "pip install -e ." in the terminal to install this project.
'''
import os
import setuptools
import setuptools_scm


#########################################
def main(
) -> None:
    '''
    Main function.
    '''
    version_string = setuptools_scm.get_version(
        root='..',
        relative_to=__file__,
        local_scheme='node-and-timestamp',
    )
    with open(os.path.join('gabra_converter', 'version.txt'), 'w', encoding='utf-8') as f:
        f.write(version_string)

    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = f.read().strip().split('\n')

    setuptools.setup(
        name='gabra_converter',
        version=version_string,
        packages=[
            'gabra_converter',
        ],
        package_data={
            'gabra_converter': [
                'version.txt',
            ]
        },
        install_requires=requirements
    )


#########################################
if __name__ == '__main__':
    main()
