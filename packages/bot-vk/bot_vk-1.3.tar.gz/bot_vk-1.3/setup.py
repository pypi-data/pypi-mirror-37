from setuptools import setup,find_packages
# __init__.py
__version__ = "0.1"
setup(name='bot_vk',
      version='1.3',
      description='Легкое создание чат-ботов вк',
      long_description='Этот модуль позволит вам без труда создать своего чат-бота вконтакте. ',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6', 'Topic :: Text Processing :: Linguistic',
                    ],
      keywords='vk, vk_api, vk_bot,bot_vk',
      url='https://vk.com/@bot_vk_python-doc-1-0', author='ivan martemyanov',
      author_email='imartemy152@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'vk_api',
          'requests',
          'datetime',
          'lxml'
          
      ],
      include_package_data=True,
      zip_safe=False
)
