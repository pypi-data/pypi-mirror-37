from setuptools import setup, find_packages
setup(name='guestbook.lynn',
        version = '1.0.0',
        package = find_packages(),
        include_package_data = True,
        install_requires = ['Flask',],

entry_points="""
[console_scripts]
guestbook = guestbook:main
""",

      )
