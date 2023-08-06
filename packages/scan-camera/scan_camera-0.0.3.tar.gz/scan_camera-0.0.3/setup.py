import setuptools

with open ( "README.md" , "r" ) as fh :
    long_description = fh.read()

setuptools.setup (
    name = "scan_camera" ,
    version = "0.0.3" ,
    author = "Oliver Xu" ,
    author_email = "273601727@qq.com" ,
    description = "A scanner that could scan all the ip off the world" ,
    long_description = long_description ,
    long_description_content_type = "text/markdown" ,
    url = "https://xujh.top" ,
    packages = setuptools.find_packages(),
    install_requires=[
        "requests",
        "gevent",
        "fire",
    ],
    entry_points={
          'console_scripts': [
              'scan_camera=scan_camera.final_scan:execute'
          ],},
    classifiers = [
        "Programming Language :: Python :: 2" ,
        "License :: OSI Approved :: MIT License" ,
        "Operating System :: OS Independent" ,
    ],
)