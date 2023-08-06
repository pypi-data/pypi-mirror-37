#!/usr/bin/env python
# -*- coding: utf-8 -*-
import exit
import mac_appify
import mkalias
import os
import plistlib
import public
import shutil
import sys
import time


"""
path/to/<name>.py                                 class Name(mac_app.App)
/usr/local/var/images/<name>.png                  (customizable)

output:
~/Applications/.appify/<name>.app                 (customizable)
path/to/alias                                     (optional)

app logs:
~/Library/Logs/Applications/<name>/out.log        (customizable)
~/Library/Logs/Applications/<name>/out.log        (customizable)

app files:
<name>.app/Contents/MacOS/executable              bash wrapper (hack to keep app visible)
<name>.app/Contents/MacOS/agent.plist             LaunchAgent
<name>.app/Contents/MacOS/run.py                  (your class file)
"""

APPLICATIONS = os.path.join(os.environ["HOME"], "Applications")
LOG = os.path.join(os.environ["HOME"], "Library/Logs/Applications")
CODE = """#!/usr/bin/env bash

# LaunchAgent required to keep app visible in Dock
set "${0%/*}"/agent.plist
trap "launchctl unload '$1'" EXIT
PlistBuddy() { /usr/libexec/PlistBuddy "$@"; }
PlistBuddy -c "Delete WorkingDirectory" -c "Add WorkingDirectory string ${0%/*}" "$1"

Label="$(PlistBuddy -c "Print Label" "$1")"
# logs must exists or launchd will create logs with root permissions
logs="$(PlistBuddy -c "Print StandardErrorPath" -c "Print StandardOutPath" "$1")"
dirs="$(echo "$logs" | grep / | sed 's#/[^/]*$##' | uniq)"
( IFS=$'\\n'; set -- $dirs; [ $# != 0 ] && mkdir -p "$@" )

launchctl unload "$1" 2> /dev/null; launchctl load "$1"
while :; do sleep 0.3 && launchctl list "$Label" | grep -q PID || exit 0; done
"""


@public.add
class App:
    _app_name = None
    _app_script = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)
        if ".app/" in self.app_script:
            exit.register(self.atexit)

    def atexit(self):
        pass

    @property
    def app_name(self):
        """
app name concepts:
1)   custom name self._app_name with @app_name.setter
2)   class name self.__class__.__name__.lower().replace("_", "-")
3)   module name (os.path.splitext(os.path.basename(self.app_script))[0].replace("_", "-"))
        """
        if self._app_name:
            return self._app_name
        return self.__class__.__name__.lower().replace("_", "-")

    @app_name.setter
    def app_name(self, name):
        self._app_name = name

    @property
    def app_script(self):
        if self._app_script:
            return self._app_script
        return sys.modules[self.__class__.__module__].__file__

    @app_script.setter
    def app_script(self, path):
        self._app_script = path

    @property
    def app_path(self):
        return os.path.join(APPLICATIONS, ".appify", "%s.app" % self.app_name)

    @property
    def appified(self):
        return os.path.exists(self.app_path)

    def rm_app(self):
        if os.path.exists(self.app_path):
            shutil.rmtree(self.app_path)
        return self

    @property
    def app_image(self):
        return "/usr/local/var/images/%s.png" % self.app_name.lower()

    @property
    def app_stdout(self):
        return os.path.join(LOG, self.app_name, "out.log")

    @property
    def app_stderr(self):
        return os.path.join(LOG, self.app_name, "err.log")

    def copy_script(self):
        dst = os.path.join(self.app_path, "Contents", "MacOS", "run.py")
        shutil.copy(self.app_script, dst)
        return self

    def appify(self):
        if ".app/" not in os.getcwd():
            mac_appify.Code(CODE).appify(self.app_path, self.app_image)
            self.copy_script()
            self.create_agent()
        return self

    def create_agent(self):
        Label = "%s.app" % self.app_name
        """
`bash -l` load your environment variables
        """
        ProgramArguments = ["bash", "-l", "-c", "python -u run.py"]
        data = dict(Label=Label, ProgramArguments=ProgramArguments, RunAtLoad=True, StandardOutPath=self.app_stdout, StandardErrorPath=self.app_stderr)
        path = os.path.join(self.app_path, "Contents", "MacOS", "agent.plist")
        plistlib.writePlist(data, path)

    def mkalias(self, dst):
        mkalias.mkalias(self.app_path, dst)
        os.utime(os.path.dirname(dst), None)  # refresh Dock icon
        return self

    def sleep(self, seconds):
        time.sleep(seconds)
        return self

    def __str__(self):
        return '<App "%s">' % self.app_path

    def __repr__(self):
        return self.__str__()
