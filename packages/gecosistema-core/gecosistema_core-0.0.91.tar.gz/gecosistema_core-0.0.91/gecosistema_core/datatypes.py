# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2018 Luzzi Valerio 
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
#
# Name:        datatypes
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     04/09/2018
# -------------------------------------------------------------------------------
from .strings import *
from .stime   import *
import numpy as np

def parseInt(text):
    """
    parseInt
    """
    if isinstance(text, (int,)):
        return text
    if isinstance(text, (np.int,np.int0,np.int8,np.int16,np.int32,np.int64,np.integer)):
        return np.asscalar(text)
    if isstring(text):
        PATTERN1 = """^[-+]?\d+$"""
        PATTERN = """(?P<target>(%s))""" % (PATTERN1)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return int(res)
    return None


def parseFloat(text):
    """
    parseFloat
    """
    if isinstance(text, (float,)):
        return text
    if isinstance(text, (np.float,np.float16,np.float32,np.float64,np.floating)):
        return np.asscalar(text)
    if isstring(text):
        PATTERN1 = """^[-+]?(?:(\d+|\d+\.\d*|\d*\.\d+)(e[-+]?\d+)?)$"""
        PATTERN = """(?P<target>(%s))""" % (PATTERN1)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return float(res)
    return None


def parseDate(text):
    """
    parseDate
    """
    if isinstance(text,(datetime.date,)):
        return text
    if isstring(text):
        PATTERN1 = """^\d{1,2}-\d{1,2}-(\d{4,4}|\d{2,2})$"""  # 1-1-2017
        PATTERN2 = """^\d{1,2}(\/)\d{1,2}(\/)(\d{4,4}|\d{2,2})$"""  # 1/1/2017
        PATTERN3 = """^\d{4,4}-\d{1,2}-\d{1,2}$"""  # 2017-01-01
        PATTERN = """(?P<target>(%s)|(%s)|(%s))""" % (PATTERN1, PATTERN2, PATTERN3)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return strftime("%Y-%m-%d", res)
    return None


def parseDatetime(text):
    """
    parseDatetime
    """
    if isinstance(text,(datetime.datetime,)):
        return text
    if isstring(text):
        PATTERN1 = """^\d{1,2}-\d{1,2}-(\d{4,4}|\d{2,2})(\s\d{1,2}(:|\.)\d{2,2}((:|\.)\d\d)?)?$"""
        PATTERN2 = """^\d{1,2}(\/)\d{1,2}(\/)(\d{4,4}|\d{2,2})(\s\d{1,2}(:|\.)\d{2,2}((:|\.)\d\d)?)?$"""
        PATTERN3 = """^\d{4,4}-\d{1,2}-\d{1,2}(\s\d{1,2}(:|\.)\d{2,2}((:|\.)\d\d)?)?$"""
        PATTERN = """(?P<target>(%s)|(%s)|(%s))""" % (PATTERN1, PATTERN2, PATTERN3)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return strftime("%Y-%m-%d %H:%M:%S", res)
    return None


def parseBool(text):
    """
    parseBool
    """
    if type(text)==type(True):
        return text
    if isstring(text):
        if text.lower() in ("true", "1", "on"):
            return True
        elif text.lower() in ("false","0","off"):
            return False
    return None

def isarray(value):
    return isinstance(value, (tuple, list, np.ndarray))

def isint(text):
    return not parseInt(text) is None

def isfloat(text):
    return not parseFloat(text) is None

def isdate(text):
    return not parseDate(text) is None

def isdatetime(text):
    return not parseDatetime(text) is None

def isbool(text):
    return not parseBool(text) is None

def parseValue(value, nodata=("", "Na", "NaN", "-", "--", "N/A")):
    """
    parseValue - parse values from string
                 used to parse string data (importcsv)
    """
    if value is None:
        return None
    if isstring(value) and value in nodata:
        return None
    elif isdate(value):
        return strftime("%Y-%m-%d", value)
    elif isdatetime(value):
        return strftime("%Y-%m-%d %H:%M:%S", value)
    elif isint(value):
        return parseInt(value)
    elif isfloat(value):
        return parseFloat(value)
    elif isbool(value):
        return parseBool(value)
    elif isstring(value):
        return value
    elif isarray(value):
        return [parseValue(item) for item in value]
    return None