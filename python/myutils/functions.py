# Bunch of functions i use on daily basis
try:
    import __builtin__
    from __builtin__ import unicode
except (ImportError,):
    import builtins as __builtin__  # python3

import os
import re
import csv
import json
import time
import uuid
import datetime
import tempfile
import subprocess
import webbrowser

from functools import wraps
from xml.dom import minidom
from xml.etree import ElementTree as etree


# USEFUL FUNCTIONS
def set_builtin_var(name, value):
    setattr(__builtin__, name, value)


def get_realpath(f):
    """Retuns the realpath of a file
    """
    return os.path.realpath(f)


def get_joined_path(*args):
    """Returns joined path of to file
    """
    return os.path.join(*args)


def get_file_content(filename):
    """Returns content of a given file
    """
    with open(filename) as f:
        return f.read()


def write_content_into_file(content, filename):
    """Save content into the given file
    """
    with open(filename, 'wb') as fd:
        fd.write(content)


# JSON TOOL
def json_get_data(json_file):
    """Returns a json data
    """
    with open(json_file) as f:
        json_data = json.load(f)

    return json_data


def json_write_data(json_data, output):
    """Write data into a json file
    """
    with open(output, 'w') as f:
        json.dump(json_data, f, indent=4, encoding='utf-8', sort_keys=True)
        return True
    return False


def json_get_lines(filename):
    data = []
    with open(filename, 'rb') as fd:
        for line in fd:
            data.append(json.loads(line))
    return data


# XML TOOL
def xml_get_data(xml_file):
    root = etree.parse(xml_file)
    return root.getroot()


def xml_write_data(xml, filename):
    with open(filename, 'wb') as fd:
        data = xml_pretty(xml_to_string(xml))
        fd.write(data)
        return True


def xml_to_string(elt):
    return etree.tostring(elt)


# CSV TOOL
def csv_get_dialect(filename):
    with open(filename, 'rb') as fd:
        content = fd.read()
        content = content.decode('utf-8-sig', 'ignore').encode('utf-8')
        dialect = csv.Sniffer().sniff(content)
        return dialect


def csv_unicode_to_str(data):
    for datum in data:
        for key, value in datum.items():
            if isinstance(value, (unicode,)):
                datum[key] = value.encode('utf-8')
            else:
                datum[key] = value
    return data


def csv_get_data(filename, as_dict=False, skip_header=False):
    data = []
    with open(filename, 'rb') as fd:
        read_method = 'DictReader' if as_dict else 'reader'
        rows = vars(csv)[read_method](fd, delimiter=',', quotechar='"')
        if read_method == 'reader' and skip_header:
            rows.next()
        for row in rows:
            data.append(row)

        return data


def csv_get_dict_data(filename, fieldnames=[], delimiter=None, skip_header=False):
    with open(filename, 'rb') as fd:
        kwargs = {'fieldnames': fieldnames}

        # use dialect if delimiter not set
        if not delimiter:
            kwargs['dialect'] = csv_get_dialect(filename)
        else:
            kwargs['delimiter'] = delimiter

        reader = csv.DictReader(fd, **kwargs)
        if skip_header:
            reader.next()
        return list(reader)
    return False


def csv_write_dict_data(data, filename, fieldnames=[], delimiter=';', header=True, unicode_to_str=False):
    with open(filename, 'wb') as fd:
        if not fieldnames:
            fieldnames = data[0].keys()
        if unicode_to_str:
            data = csv_unicode_to_str(data)
        writer = csv.DictWriter(fd, fieldnames, delimiter=delimiter)
        if header:
            writer.writeheader()
        writer.writerows(data)


# JSON/XML prettyfier
def json_pretty(data):
    if isinstance(data, str):
        data = json.loads(data.decode('utf-8'))
    return json.dumps(data, indent=2, sort_keys=True)


def xml_pretty(data):
    parsed_string = minidom.parseString(data.decode('utf-8'))
    return parsed_string.toprettyxml(indent='\t', encoding='utf-8')


def xml_dump(element):
    print(xml_pretty(etree.tostring(element)))


# MY DECORATORS
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{0} executed in {1}".format(func.__name__, end - start))
        return result
    return wrapper


def coroutine(func):
    @wraps(func)
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start


# UUID
def uuidgen():
    return uuid.uuid4().bytes.encode('base64').rstrip('=\n').replace('/', '_')


def run_bash_command(command, cwd='.'):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=cwd, shell=True)
    result = process.communicate()
    return result


def datetime_now():
    return datetime.datetime.now()


def get_datetime_from(dts):
    return datetime.datetime.strptime(dts, '%Y-%m-%d %H:%M')


def showbrowser(content=None, filepath=None):
    if not any((content, filepath)):
        raise Exception('<content> or <filepath> must be set')
    if content:
        with tempfile.NamedTemporaryFile(prefix='py-shell', suffix='.html', delete=False) as tpf:
            tpf.write(content)
            filepath = tpf.name

    webbrowser.open_new_tab(filepath)
    return True


def slugify(value):
    import unicodedata

    _slugify_strip_re = re.compile(r'[^\w\s-]')
    _slugify_hyphenate_re = re.compile(r'[-\s]+')

    if not isinstance(value, unicode):
        value = unicode(value, errors='ignore')
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(_slugify_strip_re.sub('', value).strip().lower(), errors='ignore')
        return _slugify_hyphenate_re.sub('-', value)
