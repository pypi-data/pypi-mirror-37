Py3DFreeHandUS
==============

**A Python library for 3D free-hand ultra-sound measurements**.

Folder *Py3DFreeHandUS* contains source code and doc.

HTML doc is in *doc/index.html*.

After installing Anaconda/Miniconda, do the following to create a Conda
sandboxed environment and install Py3DFreeHandUS:

*Windows*:

- create a .bat text file and insert the following content:

```
conda create -n 3dfus python=2.7 libpython msvc_runtime mingw spyder pyqt --yes
call activate 3dfus
pip install Py3DFreeHandUS --no-cache-dir
call deactivate
```

- double-click on the .bat file.

You should see a new link also pointing to Spyder for the sandboxed environment.

If clicking that does not work, just create a .bat text file with the following
content:

```
call activate 3dfus
spyder
```

and double-click on it.


**IMPORTANT NOTE**: this library is under active development.
We do our best to try to maintain compatibilty with previous
versions at each update.
