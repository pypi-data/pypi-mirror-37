# ezFreeCAD
Python wrapper for interfacing with FreeCAD; makes it easier to draw 3D objects programmatically

## Installation

First make sure FreeCAD is installed and that FreeCAD.so or FreeCAD.dll is in your python path so that you can do `import FreeCAD` in python without any errors.

```bash
pip install ezFreeCAD
```

### Windows
1. Install [git](https://git-scm.com/downloads) using the default install options
1. Install [WinPython](https://github.com/winpython/winpython/releases/tag/1.2.20151029) with python 2.7
1. Install the latest release of [FreeCAD](https://github.com/FreeCAD/FreeCAD/releases)
1. In a `WinPython Command Prompt.exe` terminal session, run `pip install --upgrade git+https://github.com/AFMD/ezFreeCAD.git`

### Ubuntu
As it turns out, it's not so "ez" to get this library working in Ubuntu. It requires a version of FreeCAD's geometry kernel that I haven't found packaged for Debian, so you have to build the required geometry kernel and also FreeCAD yourself before you're able to use this project. Here are the steps for that:
#### 15.10
```
mkdir ezFreeCAD-stuff
cd ezFreeCAD-stuff
sudo apt-get install tcl-vtk6 ftgl-dev libvtk6-dev tk-dev libxmu-dev mesa-common-dev libxi-dev autoconf libtool automake libgl2ps-dev quilt libtbb-dev libfreeimage-dev cmake build-essential
wget https://users.physics.ox.ac.uk/~christoforo/opencascade/src-tarballs/opencascade-6.9.1.tgz
tar -xvf opencascade-*.tgz
cd opencascade-*
sed -i -e '$aINCLUDE(CPack)' CMakeLists.txt
mkdir -p build
cd build
flags=""
flags="$flags -DCMAKE_BUILD_TYPE=Release"
flags="$flags -DCPACK_PACKAGE_VERSION_MAJOR=6"
flags="$flags -DCPACK_PACKAGE_VERSION_MINOR=9"
flags="$flags -DCPACK_PACKAGE_VERSION_PATCH=1"
#flags="$flags -DINSTALL_PREFIX=/usr"
#flags="$flags -DINSTALL_LIB_DIR=lib/"'$(DEB_HOST_MULTIARCH)'
#flags="$flags -DCMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES=/lib/"'$(DEB_HOST_MULTIARCH)'";/usr/lib/"'$(DEB_HOST_MULTIARCH)'
flags="$flags -DINSTALL_DIR=/opt/occt"
#flags="$flags 3RDPARTY_VTK_INCLUDE_DIR=/opt/vtk6/include"
#flags="$flags 3RDPARTY_VTK_LIBRARY_DIR=/opt/vtk6/lib"
#flags="$flags -DUSE_GL2PS=ON"
#flags="$flags -DUSE_FREEIMAGE=ON"
#flags="$flags -DUSE_TBB=ON"
#flags="$flags -DUSE_VTK=ON"
#flags="$flags -DUSE_TBB=OFF"
#flags="$flags -DUSE_TBB=ON"
cmake $flags ..
make -j4 #<-- "-j4" directs the system to use four compilation threads (don't use more than your number of logical CPU cores)
cpack -D CPACK_GENERATOR="DEB" -D CPACK_PACKAGE_CONTACT="none"
sudo dpkg -i OCCT-*.deb
sudo su -c 'echo "source /opt/occt/env.sh" > /etc/profile.d/occt.sh'
sudo sed -i 's,aScriptPath=\${BASH_SOURCE%/\*}; if \[ -d "\${aScriptPath}" \]; then cd "\$aScriptPath"; fi; aScriptPath="\$PWD";,aScriptPath=\${BASH_SOURCE%/\*}; if \[ -d "\${aScriptPath}" \]; then pushd "\$aScriptPath"; fi; aScriptPath="\$PWD"; popd;,g' /opt/occt/env.sh
source /opt/occt/env.sh

cd ../..
sudo add-apt-repository -su ppa:freecad-maintainers/freecad-stable
apt-get source freecad
sudo apt-get install cmake devscripts tcl8.5-dev tk8.5 tk8.5-dev equivs
cd freecad-*
#sudo sed -i 's| liboce-foundation-dev,|# liboce-foundation-dev,|g' debian/control
#sudo sed -i 's| liboce-modeling-dev,|# liboce-modeling-dev,|g' debian/control
sudo sed -i 's| liboce-ocaf-dev,|# liboce-ocaf-dev,|g' debian/control
sudo sed -i 's| liboce-visualization-dev,|# liboce-visualization-dev,|g' debian/control
sudo sed -i 's| oce-draw,|# oce-draw,|g' debian/control
sudo sed -i 's| netgen-headers,|# netgen-headers,|g' debian/control
mk-build-deps
# Errors in the next few lines, that's fine we'll fix them up with "apt-get -f install" later
#apt-get download netgen-headers libnglib-dev libnglib-4.9.13
#sudo dpkg --force-all -i netgen-headers* libnglib-dev* libnglib-4.9.13*
sudo dpkg -i freecad-build-deps*
sudo apt-get -f install
sed -i 's,-DOCC_INCLUDE_DIR="/usr/include/oce" \\,-DOCC_INCLUDE_DIR="/opt/occt/inc" \\\n-DOCC_LIBRARY_DIR="/opt/occt/lin64/gcc/lib" \\,g' debian/rules
sed -i 's,16.04,16.03,g' debian/rules
dpkg-buildpackage -rfakeroot -uc -b
#sudo apt-get remove netgen-headers libnglib-4.9.13 libnglib-dev
sudo dpkg -i ../freecad_*.deb
sudo apt-get install -f

sudo apt-get install python2.7 python-pip git
pip2 install --upgrade git+https://github.com/AFMD/ezFreeCAD.git #<-- install this library
```
### Arch
```
pacaur -S python2-ezfreecad
```
## Usage
The FreeCAD python module must be imported before `import ezFreeCAD` will work.  
`import FreeCAD` will import directly from the FreeCAD.so (FreeCAD.dll in Windows) file that's distributed with your FreeCAD package. The only catch here is that the directory containing your FreeCAD.so or FreeCAD.dll file must be in your `sys.path` python variable before you try to `import FreeCAD`.  
Here are some of the default locations for the FreeCAD.so file that I'm aware of:  

OS | Directory containing FreeCAD.so
---|---
Ubuntu | /usr/lib/freecad/lib
Arch | /usr/lib/freecad
Windows | C:\\Users\\${USER}\\Downloads\\FreeCAD_0.17.7451_x64_dev_win\\bin

See [unitTest.py](/unitTest.py) for example usage, or add something like
```python
import sys
sys.path.append('/usr/lib/freecad') # path to directory containing your FreeCAD.so or FreeCAD.dll file
import FreeCAD
import ezFreeCAD
```
to your script and start using the functions defined [here](/ezFreeCAD/__init__.py) in your script.

## Hacking
```bash
git clone https://github.com/AFMD/ezFreeCAD.git
cd ezFreeCAD
# do hacking here
python2 setup.py install #<--install your hacked package
./unitTest.py #<--test your hacks
```

TODO: writeup info on installing dxfLibrary
