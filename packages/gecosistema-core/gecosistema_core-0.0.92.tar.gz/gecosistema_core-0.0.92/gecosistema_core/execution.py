# -----------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2018 Luzzi Valerio for Gecosistema S.r.l.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Name:        execution
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     27/07/2018
# -----------------------------------------------------------------------------
import os,sys,json
import subprocess
from .strings import *
from .platform import *
import datetime

def Exec(command, env={}, precond=[], postcond=[], remove=[], skipIfExists=False, nowait=False, verbose=False):
    """
    Exec
    """
    t1 = datetime.datetime.now()
    res = True

    if skipIfExists:
        # check post conditions
        for filename in postcond:
            if not os.path.isfile(filename):
                res = False
                break
        if res:
            t2 = datetime.datetime.now()
            if verbose:
                command = sformat(command, env)
                print("Post conditions already fulfilled for %s[...]!" % command[:12])
                print("Done in %ss." % ((t2 - t1).total_seconds()))
            return res

    res = True
    # check pre conditions (file existence)
    for filename in listify(precond):
        if not os.path.isfile(filename):
            res = False
            break
    if verbose:
        print(sformat(command, env))
    if res:

        if isWindows():
            command = sformat(command, env)
            args = command
        else:
            command = command.replace('"{', '{').replace('}"', '}')
            command = sformat(command, env)
            command = normalizestring(command)
            args = listify(command, " ", '"')
        if nowait:
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
            res = p.communicate()
        else:
            try:
                subprocess.call(args, shell=False)

            except Exception as ex:
                if verbose:
                    print(ex)
                    return False

    # check post conditions
    for filename in listify(postcond):
        if verbose:
            print("Checking post conditions:%s" % filename)
        if not os.path.isfile(filename):
            res = False
            break
    # remove temporary files
    for filename in listify(remove):
        if verbose:
            print("removing temp file:%s" % filename)
        if os.path.isfile(filename):
            os.remove(filename)
    t2 = datetime.datetime.now()
    if verbose:
        print("Done in %ss." % ((t2 - t1).total_seconds()))
    return res

def EXEC(command):
    """
    shortcut for Exec
    """
    return Exec(command)

def Python(command, env={}, precond=[], postcond=[], remove=[], skipIfExists=False, verbose=False, outputmode="boolean"):
    """
    Python
    """

    res = Exec("python " + command, env, precond, postcond, remove, skipIfExists, nowait=False, verbose=verbose)
    if outputmode=="boolean":
        res
    elif outputmode=="json":
        res = json.loads(res)

    return res

def PYTHON(command):
    """
    PYTHON
    """
    return Python(command,verbose=True,outputmode="boolean")

def Rscript(command, additional_lib="", verbose=False):
    """
    Rscript -  call  rscript interpreter
    """

    command = """Rscript --vanilla %s""" % (command)
    if verbose:
        print(command)
    environ = os.environ
    environ['R_LIBS_USER'] = additional_lib
    p = subprocess.Popen(command, env=environ, stdout=subprocess.PIPE)

    res = p.communicate()
    res = [item for item in res if item]
    res = res[0].split("\r\n") if len(res) > 0 else []
    res = [item.strip("[1] ") for item in res if item]
    if verbose:
        for item in res:
            print( "-->" + item)
    res = res[-1] if len(res) > 0 else ""
    return res