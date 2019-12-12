from flask import Blueprint, json
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta

from blue.models import *
import subprocess

mod = Blueprint('utilities', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'svg'}


class Utilities:
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def create_new_dir(self):
        print("I am being called")
        global UPLOAD_FOLDER
        print(UPLOAD_FOLDER)
        UPLOAD_FOLDER = UPLOAD_FOLDER + datetime.datetime.now().strftime("%d%m%y%H")
        cmd = "mkdir -p %s && ls -lrt %s" % (UPLOAD_FOLDER, UPLOAD_FOLDER)
        output = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE).communicate()[0]

        if "total 0" in output:
            print("Success: Created Directory %s" % (UPLOAD_FOLDER))
        else:
            print("Failure: Failed to Create a Directory (or) Directory already Exists", UPLOAD_FOLDER)

    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
