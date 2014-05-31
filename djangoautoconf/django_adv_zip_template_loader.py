import os
import zipfile
from django.conf import settings
from django.template import TemplateDoesNotExist
#import django.template.loaders.app_directories.Loader
import sys
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
import logging
from django.template.loader import BaseLoader


# At compile time, cache the directories to search.

fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
app_template_dirs = []
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError, e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    app_template_dirs.append(template_dir.decode(fs_encoding))

# It won't change, so convert it to a tuple to save memory.
app_template_dirs = tuple(app_template_dirs)


def get_zip_file_and_relative_path(full_path_into_zip):
    full_path_into_zip = full_path_into_zip.replace("\\", "/")
    zip_ext = ".zip"
    zip_ext_start_index = full_path_into_zip.find(zip_ext + "/")
    lib_path = full_path_into_zip[0:zip_ext_start_index] + zip_ext
    inner_path = full_path_into_zip[zip_ext_start_index + len(zip_ext) + 1:]
    return lib_path, inner_path


log = logging.getLogger(__name__)


class Loader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        """Template loader that loads templates from zipped modules."""
        #Get every app's folder
        log.error("Calling zip loader")
        for folder in app_template_dirs:
            if ".zip/" in folder.replace("\\", "/"):
                lib_file, relative_folder = get_zip_file_and_relative_path(folder)
                log.error(lib_file, relative_folder)
                try:
                    z = zipfile.ZipFile(lib_file)
                    log.error(relative_folder + template_name)
                    template_path_in_zip = os.path.join(relative_folder, template_name).replace("\\", "/")
                    source = z.read(template_path_in_zip)
                except (IOError, KeyError) as e:
                    import traceback
                    log.error(traceback.format_exc())
                    try:
                        z.close()
                    except:
                        pass
                    continue
                z.close()
                # We found a template, so return the source.
                template_path = "%s:%s" % (lib_file, template_path_in_zip)
                return (source, template_path)

        # If we reach here, the template couldn't be loaded
        raise TemplateDoesNotExist(template_name)

_loader = Loader()