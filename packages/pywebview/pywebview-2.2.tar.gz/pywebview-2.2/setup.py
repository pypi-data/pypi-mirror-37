import os
import platform
from setuptools import setup


if platform.system() == "Windows":
    install_requires = ['pythonnet']
elif platform.system() == "Darwin":
    install_requires = ['pyobjc']
elif platform.system() == "Linux":
    install_requires = ['PyQt5'] if 'KDE_FULL_SESSION' in os.environ else ['PyGObject']
elif platform.system() == 'OpenBSD':
    install_requires = ['PyQt5']


setup(
    name="pywebview",
    author="Roman Sirokov",
    author_email="roman@flowrl.com",
    description=("A cross-platform lightweight native wrapper around a web view component"),
    url="http://github.com/r0x0r/pywebview",
    download_url="https://github.com/r0x0r/pywebview/archive/2.2.tar.gz",
    keywords=["gui", "webkit", "html", "web"],
    install_requires=install_requires,
    version="2.2",
    include_package_data=True,
    packages=["webview", "webview.js"],
    package_data={"webview": ['webview/lib/WebBrowserInterop.x64.dll', 'webview/lib/WebBrowserInterop.x86.dll']},
    license="New BSD license",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: GTK",
        "Environment :: X11 Applications :: Qt",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces"
        ],
)
