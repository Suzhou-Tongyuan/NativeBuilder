# package the directory at 'deps/vcpkg' into a zip file located at 'native_build/data/vcpkg.zip'
# if there is an existing zip file, it will be removed and a new one will be created.

import os
import shutil

if __name__ == '__main__':
    if os.path.exists('native_builder/data/vcpkg.zip'):
        os.remove('native_builder/data/vcpkg.zip')

    shutil.make_archive('native_builder/data/vcpkg', 'zip', 'deps/vcpkg')
