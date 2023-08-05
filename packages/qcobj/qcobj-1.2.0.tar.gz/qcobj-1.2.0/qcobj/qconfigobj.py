from __future__ import print_function
import os
import sys
import textwrap
import warnings
import math
from pint import UnitRegistry, set_application_registry
from configobj import (ConfigObj, get_extra_values, flatten_errors,
        ConfigObjError)
from validate import Validator, ValidateError

from io import BytesIO

#==============================================================================
# LOCAL IMPORTS
#==============================================================================
try:
    from colorize.colorize import colorize
except ImportError:
    def colorize(*args):
        return args[0]

#==============================================================================
# CONSTANTS
#==============================================================================
MANY = '__many__'
CONFIGFILES_KEY = 'configFiles'
ERROR_COLOR = 'Zinnia'
EXTRA_COLOR = 'Forest'

# This is the magic: create a SINGLE UnitRegistry object, or you will not
# be able to compare / add quantities:
# WARNING: THIS STATEMENT CAN TAKE MORE THAN 0.1 second!
UR = UnitRegistry(autoconvert_offset_to_baseunit=True)
set_application_registry(UR)
URQ = UR.Quantity

#------------------------------------------------------------------------------
def eng_string(x, fmt='%s', si=False, doround=None):
    """ Returns float/int value <x> formatted in a simplified engineering
        format using an exponent that is a multiple of 3.

        Args:
            fmt (string): printf-style string used to format the value
                before the exponent.
            si (boolean): if True, use SI suffix for exponent, e.g. k
                instead of e3, n instead of e-9 etc.
            doround (boolean): if not None round the number to
                `doround` decimal digits

        Returns: float/int value <x> formatted in a simplified engineering
            format using an exponent that is a multiple of 3.

        ::

            E.g. with fmt='%.2f':
                1.23e-08 => 12.30e-9
                    123 => 123.00
                1230.0 => 1.23e3
            -1230000.0 => -1.23e6

            and with si=True:
                1230.0 => 1.23k
            -1230000.0 => -1.23M

            and with doround=6
            0.30000000000000004 => 0.3

    """
    sign = ''
    if x < 0:
        x = -x
        sign = '-'
    if x > 0:
        exp = int(math.floor(math.log10(x)))
    else:
        exp = 0
    exp3 = exp - (exp % 3)
    if exp3 == 3 and x < 10e3:
        exp3 = 0
        x3 = x
    else:
        x3 = x / (10 ** exp3)
    if doround is not None:
        x3 = round(x3, doround)

    if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
        exp3_text = 'yzafpnum kMGTPEZY'[(exp3 - (-24)) // 3]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = 'e%s' % exp3

    return ('%s'+fmt+'%s') % (sign, x3, exp3_text)

#------------------------------------------------------------------------------
def extract(string, start='(', stop=')', firststop=True):
    """ Return substring between `start` and first/last `stop` characters

        Args:
            string (string): the string to extract from
            start (string): the left delimiter string
            stop (string): the right delimiter string
            firststop (bool): if True extract to the rightmost stop

        Returns:
            the extracted string
    """
    try:
        if firststop:
            extracted = string[string.index(start) + len(start)
                    : string.index(stop)]
        else:
            extracted = string[string.index(start) + len(start)
                    : string.rindex(stop)]
    except ValueError:
        if start == stop == "'":
            start = stop = '"'
        elif start == stop == '"':
            start = stop = "'"
        try:
            if firststop:
                extracted = string[string.index(start) + len(start)
                        : string.index(stop)]
            else:
                extracted = string[string.index(start) + len(start)
                        : string.rindex(stop)]
        except ValueError:
            extracted = ''
    return extracted


#------------------------------------------------------------------------------
def isStringLike(s):
    """ Returns True if s acts "like" a string, i.e. is str or unicode.

        Args:
            s (string): instance to inspect

        Returns:
            True if s acts like a string
    """
    try:
        s + ''
    except:
        return False
    else:
        return True

#------------------------------------------------------------------------------
def qLike(value, section, key):
    """ Return value converted to a quantity like `key` in `section`

        Args:
            value (float or int): value to convert
            section (:class:`qcobj.qconfigobj.QConfigObj`.Section`): instance
            key (string): an existing key in `section`

        Returns:
            A :class:`qcobj.qconfigobj.Q_` instance like the one at section[key] with
            magnitude `value`
    """
    return Q_(value, section.main.configUnits(section, key))

#------------------------------------------------------------------------------
def msec2cmyear(ms):
    """ Return m/s converted to cm/year Quantity

        Args:
            ms (float): meters per second

        Returns:
            cm / year
    """
    return (ms * UR.m / UR.s).to(UR.cm / UR.year).magnitude

#------------------------------------------------------------------------------
def errors(cobj, ok):
    """ Return errors in a configuration file in terse format

        Args:
            cobj (:class:`qcobj.qconfigobj.QConfigObj` instance): instance
            ok (dict):  results dictionary returned by validate

        Returns:
            error messages string
    """
    fname = cobj.filename
    if fname is None:
        msg = "ConfigSpec File is invalid:\n"
    else:
        msg = "Parameter File '%s' is invalid:\n" % cobj.filename
    for entry in flatten_errors(cobj, ok):
        # each entry is a tuple
        section_list, key, error = entry
        if key is not None:
            section_list.append(key)
        else:
            section_list.append('<-- section is missing!')
        section_string = ''.join(["[%s] " % s for s in section_list])
        if error == False:
            error = 'Missing value or section.'
        msg += "%s =\n --> %s\n" % (section_string, error)
    msg += "\n"
    return msg


#------------------------------------------------------------------------------
def makeSpecEntry(key, spec):
    """ Accept new syntax suggested by Reviewer #1

        Args:
            key (string): keyword
            spec (dict): dictionary defining the quantity and valid range.
                Valid keywords:

                    - comments: a comment string or a list of comment strings

                    - units: a string with the units of measure

                    - default: a default value (optional)

                    - min: minimum value accepted (optional)

                    - max: maximum value accepted (optional)

        Returns:
            configSpec string for `key`
    """
    specentry = ''
    comments = spec.get('comments', None)
    if comments is not None:
        # Accept single comment as well as list of comments
        if isinstance(comments, (list, tuple)):
            for com in comments:
                specentry += "# %s\n" % com
        else:
            specentry += "# %s\n" % comments

    units = spec.get('units', None)
    default = spec.get('default', None)
    min = spec.get('min', None)
    max = spec.get('max', None)
    if units is not None:
        if isinstance(units, list):
            specentry += ("%s = option(%s, default=%s)\n" %
            (key, ', '.join(units), default))
        elif 'bool' in units:
            # Special boolean keyword
            specentry += "%s = boolean(default=%s)\n" % (key, default)
        elif 'int' in units:
            # Special int keyword
            if min is not None:
                smin = "min=%s, " % min
            else:
                smin = ""
            if max is not None:
                smax = "max=%s, " % max
            else:
                smax = ""
            if default is not None:
                sdefault = "default=%s" % default
            else:
                sdefault = ""
            specentry += ("%s = integer(%s%s%s)\n"
                    % (key, smin, smax, sdefault))
        elif 'float' in units:
            # Special float keyword
            if min is not None:
                smin = "min=%s, " % min
            else:
                smin = ""
            if max is not None:
                smax = "max=%s, " % max
            else:
                smax = ""
            if default is not None:
                sdefault = "default=%s" % default
            else:
                sdefault = ""
            specentry += ("%s = float(%s%s%s)\n" % (key, smin, smax, sdefault))
        elif 'string_list' in units:
            # String List
            if min is not None:
                smin = "min=%s, " % min
            else:
                smin = ""
            if max is not None:
                smax = "max=%s, " % max
            else:
                smax = ""
            if default is not None:
                sdefault = "default=list(%s)" % default
            else:
                sdefault = ""
            specentry += ("%s = string_list(%s%s%s)\n"
                    % (key, smin, smax, sdefault))
        elif 'string' in units:
            # String
            specentry += ("%s = string(default='%s')\n" %
                (key, str(default)))
        else:
            # keyword has dimensions!
            if min is not None:
                smin = ", min=%s" % min
            else:
                smin = ""
            if max is not None:
                smax = ", max=%s" % max
            else:
                smax = ""
            if default is not None:
                sdefault = ", default='%s %s'" % (default, units.strip())
            else:
                sdefault = ""
            specentry += ("%s = quantity(units=%s%s%s%s)\n" %
                            (key, units.strip(), smin, smax, sdefault))
    else:
        # Simple string value
        specentry += "%s = string(default='%s')\n" % (key, str(defval))
    return specentry

#------------------------------------------------------------------------------
def makeSpec(name, params, level=0):
    """ Create ConfigObj configspec string definition for section `name`

        Args:
            name (string): name of the section we are building
            params (Odict): ordered dict instance with the directives:
                The directives are (key, value) where value is a dictionary
                with the keywords:

                    - comments: a comment string or a list of comment strings

                    - units: a string with the units of measure

                    - default: a default value (optional)

                    - min: minimum value accepted (optional)

                    - max: maximum value accepted (optional)

            OLD (deprecated) params:
            params (Odict): ordered dict instance with the directives:
                The directives are (key, value) where value is a tuple
                of (comment, comment, ... comment, 'units, min, max',
                default).
                In case  of int and float optional minimum or min and
                max values can be specified separated by ONE SINGLE
                blank char
            level (int): indentation level

        Returns:
            configSpec string
    """
    s = ''
    for key, value in params.items():
        if not isinstance(value, (list, tuple)):
            # New syntax
            s += makeSpecEntry(key, value)
        else:
            # Old (obsolete and now deprecate) syntax.
            for v in value[:-2]:
                # Add comment lines, NOT units
                s += "# %s\n" % v
            v = value[-2]
            defval = value[-1]
            if v:
                # Last comment is NOT empty
                if isinstance(v, list):
                    s += ("%s = option(%s, default=%s)\n" %
                    (key, ', '.join(v), defval))
                elif 'bool' in v:
                    # Special boolean keyword
                    s += "%s = boolean(default=%s)\n" % (key, defval)
                elif 'int' in v:
                    # Special int keyword
                    # Remove blanks
                    v = v.replace(' ', '')
                    items = v.split(',')
                    if len(items) == 1:
                        s += "%s = integer(default=%s)\n" % (key, defval)
                    elif len(items) == 2:
                        s += ("%s = integer(min=%s, default=%s)\n" %
                            (key, items[1], defval))
                    else:
                        s += ("%s = integer(min=%s, max=%s, default=%s)\n" %
                            (key, items[1], items[2], defval))
                elif 'float' in v:
                    # Special float keyword
                    # Remove blanks
                    v = v.replace(' ', '')
                    items = v.split(',')
                    if len(items) == 1:
                        s += "%s = float(default=%s)\n" % (key, defval)
                    elif len(items) == 2:
                        s += ("%s = float(min=%s, default=%s)\n" %
                            (key, items[1], defval))
                    else:
                        s += ("%s = float(min=%s, max=%s, default=%s)\n" %
                            (key, items[1], items[2], defval))
                elif 'string_list' in v:
                    # String List
                    # Remove blanks
                    v = v.replace(' ', '')
                    items = v.split(',')
                    if len(items) == 1:
                        s += ("%s = string_list(default=list(%s))\n" % (key,
                            defval))
                    elif len(items) == 2:
                        s += ("%s = string_list(min=%s, default=list(%s))\n" %
                            (key, items[1], defval))
                    else:
                        s += ("%s = string_list(min=%s, max=%s, "
                            "default=list(%s))\n" %
                            (key, items[1], items[2], defval))
                elif 'string' in v:
                    # String
                    s += ("%s = string(default='%s')\n" %
                        (key, str(defval)))
                else:
                    # keyword has dimensions!
                    default = str(defval)
                    # Remove blanks
                    items = v.split(',')
                    if len(items) == 1:
                        # No min, no max
                        sd = ("%s = quantity(units=%s, default='%s %s')\n" %
                            (key, items[0].strip(), default, v))
                    elif len(items) == 2:
                        # Only min, no max
                        sd = ("%s = quantity(units=%s, min=%s, "
                            "default='%s %s')\n" %
                            (key, items[0].strip(), items[1].strip(),
                            default, items[0].strip()))
                    elif len(items) == 3:
                        # Both min and max
                        sd = ("%s = quantity(units=%s, min=%s, max=%s, "
                            "default='%s %s')\n" %
                            (key, items[0].strip(), items[1].strip(),
                            items[2].strip(), default,
                            items[0].strip()))
                    s += sd
                    #if key == 'Ti':
                        #print("sd=", sd, "items=", items)
            else:
                # Simple string value
                s += "%s = string(default='%s')\n" % (key, str(defval))
    if name:
        header = "%s%s%s\n" % ('[' * level, name, level * ']')
    else:
        header = ''
    retstring = "%s%s" % (header, reindent(s, 4))
    return reindent(retstring, level * 4)


#------------------------------------------------------------------------------
def reindent(s, numSpaces=4, no_empty_lines=False):
    """ Return string s reindented by `numSpaces` spaces

        Args:
            s (string): string to reindent
            numSpaces (int): number of spaces to shift to the right
            no_empty_lines (bool): if True remove empty lines

        Returns:
            reindented string
    """
    if no_empty_lines:
        lines = [numSpaces * " " + line if line
                else line for line in  s.splitlines()]
    else:
        lines = [numSpaces * " " + line for line in s.splitlines()]
    return "\n".join(lines)


#------------------------------------------------------------------------------
def setVal(section, key, value):
    """ Set `value` to section[key] converted to default units

        Args:
            section (:class:`qcobj.qconfigobj.QConfigObj`.Section`): instance
            key (string): valid key for `section`
            value (float or int): value to set at section[key] converted
                to Quantity
    """
    section[key] = section.main.val_to_default(section, key, value)

#------------------------------------------------------------------------------
def splitPolygons(s):
    """ Return a list of polygons from s. Separator is a blank line.
        Separation lines with blanks are digested as well.

        Args:
            s (string): string defining polygon(s) separated by a blank
                line. One vertex per line

        Returns:
            list with polygons
    """
    ss = "\n".join([l if l.strip() else '\n'
            for l in s.strip().splitlines()])
    return ss.split('\n\n')

#------------------------------------------------------------------------------
def sumVal(section, key, value):
    """ Add `value` to section[key] converted to default units

        Args:
            section (:class:`qcobj.qconfigobj.QConfigObj`.Section`): instance
            key (string): valid key for `section`
            value (float or int): value to add to section[key]
    """
    section[key] += section.main.val_to_default(section, key, value)

#------------------------------------------------------------------------------
def toBaseUnits(q):
    """ Return magnitude of quantity `q` converted to base units
        * * Used for polygons * *

        Args:
            q (:class:`qcobj.qconfigobj.Q_`): instance

        Returns:
            magnitude of q in base units
    """
    return q.to_base_units().magnitude

#------------------------------------------------------------------------------
def val(section, key):
    """ Return value of section[key] in units specified in configspec

        Args:
            section (:class:`qcobj.qconfigobj.QConfigObj`.Section`): instance
            key (string): valid key for `section`

        Returns:
            values in section[key] converted to units defined in configspec
    """
    value = section[key]
    units = section.main.configUnits(section, key)
    if isinstance(value, (list, tuple)):
        try:
            return [q.to(units).magnitude for q in value]
        except AttributeError:
            return [q for q in value]
    else:
        try:
            return value.to(units).magnitude
        except AttributeError:
            return value

#------------------------------------------------------------------------------
def vval(d, k):
    """ Return magnitude in units specified in configspec for
        key `k' in qconfigobj section `d` or simply magnitude if
        `d` is a dict instance

        Args:
            d (dict or :class:`qcobj.qconfigobj.QConfigObj`.Section instance):
                dict_like
            k (string): key in d

        Returns:
            result of :func:`qcobj.qconfigobj.val` (d, k) or simply
            the magnitude of d[k]
    """
    try:
        return val(d, k)
    except AttributeError:
        return d[k].magnitude

#==============================================================================
class Q_(URQ):
    """ A Quantity class with user settable preferred units for
        representation
    """
    def __new__(cls, *args, **kargs):
        # I'm not proud of it, but it works
        if len(args) == 2:
            obj = super(Q_, cls).__new__(cls, *args, **kargs)
        else:
            # args[0] is " 1.2345  aunit * another "
            val, _, units = args[0].strip().partition(' ')
            obj = super(Q_, cls).__new__(cls, float(val), units)
        return obj

    def __reduce__(self):
        dummy, reduce_string = super(Q_, self).__reduce__()
        return (self.__class__, reduce_string)

    def __str__(self):
        """ Return :func:`qcobj.qconfigobj.eng_string` representation
            of magnitude rounded at 6 decimals with units
        """
        #default = super(Q_, self).__str__()
        eng = "%s %s" % (eng_string(self.magnitude, doround=6), self.units)
        return eng

    def __repr__(self):
        """ Return UnitRegistry Quantity representation
        """
        return super(Q_, self).__repr__()


#==============================================================================
class QConfigObjInvalid(ConfigObjError):
    """ Invalid value error
    """
    def __init__(self, value):
        super(QConfigObjInvalid, self).__init__(
                'invalid cfg file:\n%s' % (value,))


#==============================================================================
class QConfigObjExtra(ConfigObjError):
    """ Extra value / section error
    """
    def __init__(self, value):
        super(QConfigObjExtra, self).__init__(
                'extra values / sections in cfg file:\n%s' % (value,))


#==============================================================================
class _QConfigObj(ConfigObj):
    """ A Quantity aware ConfigObj class
    """
    def __init__(self, *args, **kargs):
        """ Create a new instance. kargs are from ConfigObj

            Keyword Args:
                infile (file instance): Input file (None)
                configspec (list of strings): configspec (None)
                encoding (string): encoding (None)
                interpolation (bool): True
                raise_errors (bool): False
                list_values (bool): True
                create_empty (bool): False
                file_error (bool): False
                stringify (bool): True,
                indent_type (string): None
                default_encoding (string): None
                unrepr (bool): False
                write_empty_values (bool): False
                _inspec (bool): False
                strict (bool): True
                noextra (bool): True
        """
        strict = kargs.get('strict', True)
        if 'strict' in kargs:
            del kargs['strict']
        noextra = kargs.get('noextra', True)
        if 'noextra' in kargs:
            del kargs['noextra']
        super(_QConfigObj, self).__init__(*args, **kargs)
        self.errorsmsg = ''
        self.extramsg = ''
        self.report = dict()
        if self.configspec:
            # Validate against configspec
            self.report = self.validate(
                    Certifier(), preserve_errors=True, copy=True)
            self._saveErrors()
            self._extra()
        else:
            self.errorsmsg = '\nWARNING! no configspec! Cannot validate!\n'
        if self.errorsmsg and strict:
            raise QConfigObjInvalid(colorize(self.errorsmsg, ERROR_COLOR))
        if self.extramsg and noextra:
            raise QConfigObjExtra(colorize(self.extramsg, EXTRA_COLOR))

    def _saveErrors(self):
        """ Save errors in a configuration file in terse format
        """
        fname = self.filename
        msg = "\nERROR!\n"
        if fname is None:
            msg = "ConfigSpec File is invalid:\n"
        else:
            msg = "Parameter File '%s' is invalid:\n" % self.filename
        errmsg = ''
        for entry in flatten_errors(self, self.report):
            # each entry is a tuple
            section_list, key, error = entry
            if key is not None:
                section_list.append(key)
            else:
                section_list.append('<-- section is missing!')
            section_string = ''.join(["[%s]" % s for s in section_list])
            if error == False:
                error = 'Missing value or section.'
            errmsg += "%s =\n    --> %s\n" % (section_string, error)
        if errmsg:
            self.errorsmsg = msg + errmsg + "\n"

    def _extra(self):
        """ Save extra values / sections in instance
        """
        msg = ''
        for sections, name in get_extra_values(self):
            # this code gets the extra values themselves
            the_section = self
            for section in sections:
                the_section = the_section[section]

            # the_value may be a section or a value
            the_value = the_section[name]

            msg += ''.join(["[%s]" % s for s in sections])
            if isinstance(the_value, dict):
                msg += "[%r]  --> is an extra section\n" % name
            else:
                msg += ("[%r] = '%s'\n" % (name, the_value))
        if msg:
            msg = ("\nWARNING..... Parameter file %s has extra "
                    "values / sections\n" % self.filename + msg)
        self.extramsg = msg

    def _specAtPath(self, path):
        """ Return configspec section at `path`

            Args:
                path (list): list of section names

            Returns:
                configspec section at `path`
        """
        section = self.configspec
        for p in path:
            try:
                section = section[p]
            except KeyError:
                section = section[MANY]
        return section

    def comment(self, path, key):
        """ Return comment from configspec for `key` at `path`

            Args:
                path (list): list of section names
                key (string): valid key in section at `path`

            Returns:
                comment from configspec for `key` at `path`
        """
        section = self._specAtPath(path)
        # Now section is the configspec section at path
        try:
            comments = section.comments[key]
        except KeyError:
            return "Main Section" + str(path)

        comment = '\n'.join([com.strip().strip('#').strip()
                for com in comments])
        try:
            values = section[key].replace('$', '\n')
        except AttributeError:
            return "Section [%s]" % (key, )
        else:
            return "%s\n--->%s" % (comment, textwrap.dedent(values))


    def validRange(self, path, key):
        """ Return valid range for quantity `key` at `path`

            Args:
                path (list): list of section names
                key (string): valid key in section at `path`

            Returns:
                valid range for quantity `key` at `path`
        """
        section = self._specAtPath(path)
        # Now section is the configspec section at path
        try:
            values = section[key].replace('$', '\n')
        except AttributeError:
            return None
        else:
            return textwrap.dedent(values)

    def configUnits(self, section, key):
        """ Return units string for `key` in `section` or None

            Args:
              section (:class:`qcobj.qconfigobj.QConfigObj`.Section): instance
              key (string): valid key in `section`

            Returns:
              Return units string for `key` in `section` or None
        """
        path = []
        while section.name is not None:
            path.insert(0, section.name)
            section = section.parent

        configsec = self.configspec
        for secname in path:
            try:
                configsec = configsec[secname]
            except KeyError:
                try:
                    configsec = configsec[MANY]
                except KeyError:
                    print("NO %s section!" % MANY)

        configspec = configsec[key]
        if not configspec.startswith('quantity'):
            units = None
        else:
            units = extract(extract(configspec, 'units', ','),
                    '=', '', firststop=False).strip()
        return units

    def pretty(self):
        """ Return pretty string representation for report attribute

            Returns:
                pretty string representation for report attribute
        """
        def pretty(d, d1, sep='    ', level=0):
            """ Return pretty string representation for dictionary `d`
            """
            s = ''
            for key in d.keys():
                value = d[key]
                if d1 is True:
                    value1 = True
                else:
                    try:
                        value1 = d1[key]
                    except (TypeError, KeyError):
                        value1 = None
                if isinstance(value, dict):
                    s += "%s%s%s%s\n" % (sep * level, '[' * (level + 1), key,
                            ']' * (level + 1))
                    s += pretty(d[key], value1, sep, level + 1)
                else:
                    s += "%s%s: " % (sep * level, key)
                    if isinstance(value, str):
                        if value1 is True:
                            s += '"%s"\n' % value
                        else:
                            s += '"%s" -----> %s\n' % (value, value1)
                    else:
                        if value1 is True:
                            if isinstance(value, tuple):
                                sr = '(%s)\n' % ", ".join(
                                        [repr(vs) for vs in value])
                            else:
                                sr = '%r\n' % value
                            s += sr
                        else:
                            s += '%r ---> %s\n' % (repr(value), value1)
            return s
        return pretty(self, self.report)

    def reference_quantity(self, section, key):
        """ Return reference quantity for section[key]

            Args:
              section (:class:`qcobj.qconfigobj.QConfigObj`.Section): instance
              key (string): valid key in `section`

            Returns:
                Return reference quantity for section[key]

            Note:
                At present USED ONLY IN :class:GMOD2.boundaryCondition
        """
        units = self.configUnits(section, key)
        if units is None:
            return None
        else:
            return Q_(1, units)

    def val_to_default(self, section, key, value):
        """ Set section[key] with value converted to default units (if any)

            Args:
              section (:class:`qcobj.qconfigobj.QConfigObj`.Section): instance
              key (string): valid key in `section`
              value (float or int): new value

            Note:
                At present used only in addMag and setMag
        """
        units = self.configUnits(section, key)
        if units is None:
            return value
        else:
            return Q_(value, units)

    def write_to_string(self):
        """ Return write content in a string

            Returns:
                Return write content in a string
        """
        tmp = BytesIO()
        self.write(tmp)
        return tmp.getvalue()


#==============================================================================
class QConfigObj(_QConfigObj):
    """ A Quantity aware ConfigObj class with CONFIGFILES_KEY support
    """
    def __init__(self, *args, **kargs):
        super(QConfigObj, self).__init__(*args, **kargs)
        # WARNING: EXPERIMENTAL CODE: NO CHECK AGAINST ERRORS YET
        try:
            configfiles = self[CONFIGFILES_KEY]
        except KeyError:
            configfiles = None
        if configfiles:
            # There is at least one config file!
            if ' ' in  configfiles:
                configFiles = tuple(configfiles.split())
            else:
                configFiles = (configfiles, )
            # Loop on the remaining file(s)
            cfg = ''
            for fn in (os.path.basename(self.filename), ) + configFiles:
                # Create the full pathname for the file to be included
                newpath = os.path.join(os.path.dirname(self.filename), fn)
                # Load it
                cfg += open(newpath).read()
            filename = self.filename
            self.clear()
            super(QConfigObj, self).__init__(cfg.splitlines(), **kargs)
            self.filename = filename


if sys.version_info >= (3, 0):
    QConfigObj.__init__.__doc__ = _QConfigObj.__init__.__doc__
else:
    QConfigObj.__init__.__func__.__doc__ = _QConfigObj.__init__.__doc__
#==============================================================================
class VdtUnitsError(ValidateError):
    """ Missing `units` keyword in quantity type specifier
    """
    def __init__(self, value):
        super(VdtUnitsError, self).__init__(
                'missing units keyword for value "%s".' % (value,))


#==============================================================================
class VdtDimensionalityError(ValidateError):
    """ Dimensionality error class
    """
    def __init__(self, dim1, dim2):
        super(VdtDimensionalityError, self).__init__(
                'dimensions disagree: [%s <> %s].' % (dim1, dim2,))


#==============================================================================
class VdtRangeError(ValidateError):
    """ Range error class
    """
    def __init__(self, value, vmin, vmax, units):
        super(VdtRangeError, self).__init__(
                'value "%s" out of range: [%s, %s] %s.' %
                (value, vmin, vmax, units))


#==============================================================================
class Certifier(Validator):
    """ A Validator for Quantities

        See Also:
            Validator class
    """
    def __init__(self, *args, **kargs):
        super(Certifier, self).__init__(*args, **kargs)
        # Set validator function for quantity
        self.functions['quantity'] = self.quantity_chek

    def quantity_chek(self, value, *args, **kargs):
        """ Check if value has the right dimensions and is in the allowed
            range.

            Quantity **MUST** be specified in configspec like:
            >>> quantity(units='Pa / s', min=0, max=100, default=50 Pa /s)

            where:
                - min and max *CAN* be positional arguments
                - default value can be specified in any dimensionally correct
                  unit after the first blank

            Args:
                value (instance): the value we are checking

            Returns:
                validated quantity (or quantities)

            Raises:
                VdtUnitsError if no units are specified
                ValueError if `value` is not a quantity
                SyntaxError if quantity specification uses a wrong syntax
                VdtDimensionalityError if value has the wrong physical
                    dimension
                VdtRangeError if value (converted to the units defined
                    in configspec) is not in range [vmin, vmax]
        """
        if 'units' in kargs:
            units = kargs['units']
        else:
            raise VdtUnitsError(value)

        vmin = vmax = None
        if len(args) > 0:
            vmin = float(args[0])
        if len(args) > 1:
            vmax = float(args[1])
        if 'min' in kargs:
            vmin = float(kargs['min'])
        if 'max' in kargs:
            vmax = float(kargs['max'])

        #print("quantity_chek=%s [%s<->%s]" % (value, vmin, vmax), args, kargs)

        # For configspec only: Is it tuple?
        atuple = extract(value)
        if atuple:
            values = ["%s %s" % (v, units) for v in atuple.split(',')]

        # For cfg: Is it a tuple?
        elif isinstance(value, (list, tuple)):
            values = value
        else:
            values = (value, )

        # Build quantities
        quantities = ()
        for value in values:
            try:
                quantity = Q_(value)
            except ValueError:
                raise ValueError("Value '%s' is NOT a quantity!" % value)
            except SyntaxError:
                msg = "Quantity Syntax Error in '%s': Old syntax?" % value
                warnings.warn(msg, SyntaxWarning)
                try:
                    tmp = value.replace('*', '', 1)
                    quantity = Q_(tmp)
                except SyntaxError:
                    raise SyntaxError("Value '%s' is NOT a quantity!" % value)

            # Check if quantity dimensionality is correct
            default = Q_(1, units)
            if quantity.dimensionality != default.dimensionality:
                raise VdtDimensionalityError(
                        quantity.dimensionality, default.dimensionality)

            # Check if quantity is in range [min, max]:
            if quantity.units == default.units:
                current_quantity = quantity
            else:
                current_quantity = quantity.to(default.units)
            mag = current_quantity.magnitude
            if (vmin is not None) and (mag < vmin):
                raise VdtRangeError(value, vmin, vmax, default.units)
            if (vmax is not None) and (mag > vmax):
                raise VdtRangeError(value, vmin, vmax, default.units)

            # Append quantity to tuple
            quantities += (quantity, )

        if len(quantities) == 1:
            return quantity
        else:
            return quantities


#==============================================================================
if __name__ == '__main__':
    import sys
    import os
    import argparse

    parser = argparse.ArgumentParser(
        description="\nA Quantity aware ConfigObject Module example.",
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog=os.path.basename(sys.argv[0]))

    parser.add_argument('-t', '--makeTemplate',
            default=None,
            help="Create default configuration file from given configspec"
            " in current directory and exit (default: %(default)s)")

    parser.add_argument('cfg', default=None, nargs='*',
        help=("Configuration file. Configuration parameters will be loaded "
            "from this file ")
        )
    options = parser.parse_args(sys.argv[1:])

    if options.makeTemplate is not None:
        # Write default cfg and exit
        name, ext = os.path.splitext(options.makeTemplate)
        if not ext:
            ext = '.cfg'
        default = "template%s" %  ext
        template = QConfigObj(default, configspec=options.makeTemplate)
        template.write()
        raise SystemExit("Default cfg file '%s' has been written." % default)

    if options.cfg:
        pn = options.cfg
    else:
        wrongConfigSpec = """
        oneten = integer(min=110, max=1010, default=510)
        a = quantity(units=meter, min=2, max=10, default='5 m')
        b = quantity(units=Pa / s, min=0, max=100, default='50 Pa /s')
        temp = quantity(units=degC, min=0, max=30, default='20 degC')
            [Section0]
                key0 = integer(1, 10, default=5)
                key1 = string(default=ccqq)
                key2 = boolean(default=False)
            [Section1]
                c0 = quantity(units=A, 0, 10) # Missing default!
                c1 = quantity(units=A, 0, 10, default='0.5 mA')
                c2 = quantity(units=ohm, 0, 4700, default='2200 ohm')
                # Wrong unit in default
                c3 = quantity(units=siemens, min=0, default='2200 ohm')
        """
        rightConfigSpec = """
        oneten = integer(min=110, max=1010, default=510)
        a = quantity(units=meter, min=2, max=10, default='5 m')
        b = quantity(units=Pa / s, min=0, max=100, default='50 Pa /s')
        temp = quantity(units=degC, min=0, max=30, default='20 degC')
            [Section0]
                key0 = integer(1, 10, default=5)
                key1 = string(default=ccqq)
                key2 = boolean(default=False)
            [Section1]
                c1 = quantity(units=A, 0, 10, default='0.5 mA')
                c2 = quantity(units=ohm, 0, 4700, default='2200 ohm')
                c3 = quantity(units=siemens, min=0, default='2200 siemens')
        """
        pn = BytesIO(b"""
        #oneten = 1000
        a = 5 cm
        #aa = 99 * Pa * s **2
        b = 2 Pa / s
        extra1 = 111
        extra2 = Extra2
        temp = 275 K
        # Now starts section0,
        # the 1st section
        [Section0] # Ready...
            key0 = 999 # key0 with no units
            # Now first key
            key1 = contains a string
        [Section1] # Another section
            # key c1, current
            c1 = 300 A  # 300 Ampere, wow!
            # c2 is resitance
            c2 = 4 ohm # low value
            c3 = -3 siemens
            # A new section, not defined in configSpec
            [[Subsection11]]
                whee = 88
                [[[Subsection111]]]
                    whoo = 99
        """)

    try:
        print("************* Example without configspec *************")
        cobj = QConfigObj(pn, strict=False)
        print(cobj)
    except QConfigObjInvalid as e:
        print("!!!!! Exception was rised, error was:\n%s" % e)
        print("\n")

    try:
        print("************* Example with wrong configspec *************")
        cobj = QConfigObj(pn, configspec=wrongConfigSpec.split("\n"))
        print(cobj)
    except QConfigObjInvalid as e:
        print("!!!!! Exception was rised, error was:\n%s" % e)
        print("\n")

    try:
        print("************* Example with right configspec *************")
        cobj = QConfigObj(pn, configspec=rightConfigSpec.split("\n"))
        print(cobj.pretty())
        print("************* cobj.errorsmsg *************")
        print(cobj.errorsmsg)
        print("************* extramsg *************")
        print(cobj.extramsg)
    except:
        print("This will not be printed ;-)")

    raise SystemExit





    try:
        print("*** Example without configspec, noextra=False ***")
        cobj = QConfigObj(pn, noextra=False)
        print(cobj)
        print("************* cobj.errorsmsg *************")
        print(cobj.errorsmsg)
        print("************* cobj.extrasmsg *************")
        print(cobj.extramsg)
    except QConfigObjExtra as e:
        print("!!!!! Exception was rised, error was:\n%s" % e)
        print("\n")

    try:
        print("************* Example with right configspec *************")
        cobj = QConfigObj(pn, configspec=rightConfigSpec.split("\n"))
        print(cobj.pretty())
        print("************* cobj.errorsmsg *************")
        print(cobj.errorsmsg)
        print("************* extramsg *************")
        print(cobj.extramsg)
    except:
        print("This will not be printed ;-)")

    try:
        print("************* Example with right configspec *************")
        cobj = QConfigObj(pn, configspec=rightConfigSpec.split("\n"),
                noextra=True)
        print(cobj.pretty())
        print("************* cobj.errorsmsg *************")
        print(cobj.errorsmsg)
        print("************* extramsg *************")
        print(cobj.extramsg)
    except:
        print("This will not be printed ;-)")

    #print(cobj.errorsmsg)
    #print("************* cobj.extrasmsg *************")
    #print(cobj.extramsg)
    ##cobj = QConfigObj(pn, configspec=configSpec.split("\n"), strict=False,
            ##noextra=False)
    #print(cobj.errorsmsg)
    #print("************* cobj *************")
    ##print(repr(cobj))
    #print(cobj.pretty())
