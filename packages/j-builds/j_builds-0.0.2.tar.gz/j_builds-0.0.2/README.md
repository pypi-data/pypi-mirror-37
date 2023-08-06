j builds
---------------------------

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

Build and Deploy!


Install
------------
```
pip3.7 install j_builds
pip3.7 install termcolor
```

Setup
------------
```
cat build.ini
```

```
[main]

[git]
# repo-directory = True to build it, False not to do so
repo-a = True
repo-b = True

[docker]
namespace = mynamespace

[before build]
cmd = echo "this runs before building"

[on success]
cmd = echo "this runs after a successful build"

[on fail]
cmd = echo "this runs after a not successful build"
```

