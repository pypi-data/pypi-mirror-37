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
/usr/local/var/log/Applications/<name>/out.log    (customizable)
/usr/local/var/log/Applications/<name>/out.log    (customizable)

app files:
<name>.app/Contents/MacOS/executable              bash wrapper (hack to keep app visible)
<name>.app/Contents/MacOS/agent.plist             LaunchAgent
<name>.app/Contents/MacOS/run.py                  (your class file)
"""

APPLICATIONS = os.path.join(os.environ["HOME"], "Applications")
CODE = """#!/usr/bin/env bash

# hack to keep app visible in Dock
set "${0%/*}"/agent.plist
trap "launchctl unload '$1'" EXIT
/usr/libexec/PlistBuddy -c "Delete WorkingDirectory" -c "Add WorkingDirectory string ${0%/*}" "$1"
launchctl unload "$1" 2> /dev/null; launchctl load "$1"

Label="$(/usr/libexec/PlistBuddy -c "Print Label" "$1")"
while :; do sleep 0.3 && launchctl list "$Label" | grep -q PID || exit 0; done
"""
LOG = "/usr/local/var/log/Applications"


@public.add
class App:
    _name = None
    _script = None
    alias = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)
        if ".app/" in self.script:
            exit.register(self.atexit)

    def atexit(self):
        pass

    @property
    def name(self):
        """
app name concepts:
1)   custom name self._name with @name.setter
2)  class name self.__class__.__name__.lower().replace("_", "-")
3)   module name (os.path.splitext(os.path.basename(self.script))[0].replace("_", "-"))
        """
        if self._name:
            return self._name
        return self.__class__.__name__.lower().replace("_", "-")

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def script(self):
        if self._script:
            return self._script
        return sys.modules[self.__class__.__module__].__file__

    @script.setter
    def script(self, path):
        self._script = path

    @property
    def path(self):
        return os.path.join(APPLICATIONS, ".appify", "%s.app" % self.name)

    @property
    def exists(self):
        return os.path.exists(self.path)

    def rm(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    @property
    def image(self):
        return "/usr/local/var/images/%s.png" % self.name.lower()

    @property
    def stdout(self):
        return os.path.join(LOG, self.name, "out.log")

    @property
    def stderr(self):
        return os.path.join(LOG, self.name, "out.log")

    def copy_script(self):
        dst = os.path.join(self.path, "Contents", "MacOS", "run.py")
        shutil.copy(self.script, dst)
        return self

    def appify(self):
        if ".app/" not in os.getcwd():
            mac_appify.Code(CODE).appify(self.path, self.image)
            self.copy_script()
            self.create_agent()
            if self.alias:
                self.mkalias(self.alias)
        return self

    def create_agent(self):
        Label = "%s.app" % self.name
        """
`bash -l` load your environment variables
        """
        ProgramArguments = ["bash", "-l", "-c", "python -u run.py"]
        data = dict(Label=Label, ProgramArguments=ProgramArguments, RunAtLoad=True, StandardOutPath=self.stdout, StandardErrorPath=self.stderr)
        path = os.path.join(self.path, "Contents", "MacOS", "agent.plist")
        plistlib.writePlist(data, path)

    def mkalias(self, dst):
        mkalias.mkalias(self.path, dst)
        os.utime(os.path.dirname(dst), None)  # refresh Dock icon
        return self

    def sleep(self, seconds):
        time.sleep(seconds)
        return self

    @property
    def pid(self):
        # get app pid (from another python process)
        # todo: check
        out = os.popen("ps -ax | grep -v grep | grep -v '0:00.00' | grep %s/" % self.app).read()
        if out:
            try:
                return int(out.lstrip().split(" ")[0])
            except ValueError as e:
                print(str(e))


    def __str__(self):
        return '<App "%s">' % self.path

    def __repr__(self):
        return self.__str__()
