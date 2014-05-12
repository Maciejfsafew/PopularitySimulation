Required packages:

    pip install simpy
    pip install beautifulsoup4-4.3.2



gui: I really like to choose something with simple installation but it seems that all python gui frameworks are bindings
to existing C++ frameworks like Qt, or wxWidgets. PySide seams to have the simples installation process,
but still it is not trivial

    sudo pip install pyside
    sudo ln -s /usr/local/lib/python2.7/dist-packages/PySide/libpyside-python2.7.so.1.2 /usr/lib/libpyside-python2.7.so.1.2
    sudo ln -s /usr/local/lib/python2.7/dist-packages/PySide/libpyside-python2.7.so.1.2.2 /usr/lib/libpyside-python2.7.so.1.2.2
    sudo ln -s /usr/local/lib/python2.7/dist-packages/PySide/libshiboken-python2.7.so.1.2 /usr/lib/libshiboken-python2.7.so.1.2
    sudo ln -s /usr/local/lib/python2.7/dist-packages/PySide/libshiboken-python2.7.so.1.2.2 /usr/lib/libshiboken-python2.7.so.1.2.2
    sudo sed -i "1 c__all__ = ['QtUiTools', 'QtCore', 'QtGui', 'QtNetwork', 'QtOpenGL', 'QtSql', 'QtSvg', 'QtTest', 'QtWebKit', 'QtScript']" /usr/local/lib/python2.7/dist-packages/PySide/__init__.py

database:

    #database itself
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
    sudo apt-get update
    sudo apt-get install mongodb-org
    sudo /etc/init.d/mongod start

    #python bindings
    pip install pymongo
    sudo apt-get install python2.7-dev
