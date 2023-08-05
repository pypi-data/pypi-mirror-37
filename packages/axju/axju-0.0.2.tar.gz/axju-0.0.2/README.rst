axju
====

.. image:: https://img.shields.io/gitter/room/nwjs/nw.js.svg
  :alt: Gitter
  :target: https://gitter.im/axju/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link

.. image:: https://img.shields.io/twitter/url/https/github.com/axju/axju.svg?style=social
  :alt: Twitter
  :target: https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Faxju%2Faxju


Install
-------
::

  pip install axju


Functions
---------
::

  axju --help
  axju setup
  axju me

  axju-proj list
  axju-proj push --commit "text"


Coming soon
-----------
::

  axju-sys create  # create the folder structure
  axju-sys install # install the programms
  axju-sys update  # update the os and programms

  axju-proj open --ide atom <name|dir|.>
  axju-proj update <name|dir|.>
  axju-proj backup <name|dir|.>
  axju-proj push <name|dir|.>

  axju-alias <name>

  axju-temp package
  axju-temp readme


Development
-----------
Clone repo::

  git clone https://github.com/axju/axju.git

Create virtual environment and update dev-tools::

  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade wheel pip setuptools twine

Install local::

  pip install -e .

Publish the packages::

  python setup.py sdist bdist_wheel
  twine upload dist/*
