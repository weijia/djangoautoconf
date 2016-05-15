from django.utils.encoding import force_unicode, is_protected_type
from django.utils.functional import Promise
import six


def python_2_unicode_compatible(klass):
    """
    A decorator that defines __unicode__ and __str__ methods under Python 2.
    Under Python 3 it does nothing.

    To support Python 2 and 3 with a single code base, define a __str__ method
    returning text and apply this decorator to the class.
    """
    if six.PY2:
        if '__str__' not in klass.__dict__:
            raise ValueError("@python_2_unicode_compatible cannot be applied "
                             "to %s because it doesn't define __str__()." %
                             klass.__name__)
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass


def mptt_work_around():
    import sys
    #import django_six
    #from django.utils.six.moves import zip
    import django.utils as utils
    utils.six = six
    sys.modules["django.utils.six"] = six
    sys.modules["django.utils.six.moves"] = six.moves
    # from six.moves import zip
    # utils.six.moves.zip = zip
    # from django.utils import six as django_six
    # django_six.moves = six.moves
    # from django.utils.six.moves import zip
    #
    # import mptt.templatetags.mptt_tags


def force_text_work_around():
    import django.utils.encoding as encoding
    encoding.force_text = force_unicode


def sae_work_around():
    mptt_work_around()
    force_text_work_around()


def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and is_protected_type(s):
        return s
    if isinstance(s, six.memoryview):
        return bytes(s)
    if isinstance(s, Promise):
        return six.text_type(s).encode(encoding, errors)
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join(force_bytes(arg, encoding, strings_only, errors)
                                 for arg in s)
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)