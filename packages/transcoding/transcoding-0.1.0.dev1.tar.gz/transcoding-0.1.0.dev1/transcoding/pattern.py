import logging
import parse


class ParseError(Exception):
    pass


class Pattern(object):
    def __init__(self, format_string, read_method=None):
        """
        String subclass dedicated to explicitly storing format strings
        Examples:
            >>> import transcoding as tc
            >>> fs = tc.Pattern('Input = {inp:.4f}, Output = {outp:.4f}')
            >>> fs.format(inp=42, outp=21)
            'Input = 42.0000, Output = 21.0000'

        """
        self._format_string = format_string
        self._read_method = read_method
        self._parser = None

    def __getattr__(self, attr):
        return getattr(self._format_string, attr)

    def _set_parser(self):
        try:
            parser = parse.Parser(self._format_string)
            self._parser = parser
        except Exception as err:
            log = logging.getLogger()
            log.error("Could not set parser with format_string"
                      " '{self._format_string}'".format(**locals()))
            raise err

    @property
    def read_method(self):
        """
        (callable): method to shortcut the parsing.
            Must input string and optional dependencies
            Must output a dictionary with keys = self.values
        """
        return self._read_method

    @read_method.setter
    def read_method(self, method):
        if not callable(method):
            raise ValueError("Method must be callable")
        self._read_method = method

    @property
    def parser(self):
        if self._parser is None:
            self._set_parser()
        return self._parser

    @property
    def variables(self):
        """
        (list of str): the variables of the format string
        """
        return set(self.parser._named_fields)

    def parse(self, string, raise_error=True):
        """
        inverse method of format
        evaluate a full string
        Args:
            string (basestring): main pattern and alternatives
            **kwargs

        Examples:

        Raises:
            >>> import transcoding as tc
            >>> tc.Pattern("test {value}").parse("42")  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            ParseError: Could not parse:...

        """
        log = logging.getLogger()
        
        if self.read_method is not None:
            vals = self.read_method(string, raise_error=raise_error)
        else:
            result = self.parser.parse(string)
            if result is None:
                vals = {}
                message = ("Could not parse:\n"
                           "\t\t\tline:\t\t%r\n"
                           "\t\t\twith format string:\t%r" % (string,
                                                              self._format_string))
                log.error(message)
                if raise_error:
                    raise ParseError(message)
                else:
                    log.error(message)
            else:
                vals = result.named
        log.debug("Parsing:\n"
                  "\t\t\tline:\t\t%r\n"
                  "\t\t\twith format string:\t%r\n"
                  "\t\t\tyielded:\t\t%r" % (string, self._format_string, vals))
        return vals
    
    def parse_margin(self, string, **kwargs):
        """
        evaluate pre- or suffix
        """
        log = logging.getLogger()
        left = kwargs.pop('left', True)
        log_message = None
        vals = None
        for i, pattern in enumerate(patterns):
            ''' evaluate string '''
            if isinstance(pattern, basestring):
                variables = parse.Parser(pattern)._named_fields
                if len(variables) == 0:
                    if left:
                        if not string.startswith(pattern):
                            continue
                        string = string.lstrip(pattern)
                    else:
                        if not string.endswith(pattern):
                            continue
                        string = string.rstrip(pattern)
                    vals = {}
                else:
                    if left:
                        pattern = pattern + '{REST}'
                    else:
                        pattern = '{REST}' + pattern
                    parser = parse.parse(pattern,
                                         string)
                    if parser is not None:
                        vals = parser.named
                        string = vals.pop('REST')
            elif callable(pattern):
                vals = pattern(string)
            else:
                raise TypeError("Wrong type {}".format(type(pattern)))
    
            ''' combine log messages '''
            if vals is None:
                if i == 0:
                    log_message = ("Could not parse:\n"
                                   "\t\t\tline:\t\t\t%r\n"
                                   "\t\t\twith margin pattern:\t%r" % (string, pattern))
                elif len(patterns) == 1:
                    log_message += "\n\t\t\tno alternative given."
                else:
                    log_message += "\n\t\t\tand alternative\t\t%r" % (pattern)
            else:
                break
    
        if log_message is not None:
            if vals is None:
                log.error(log_message)
            else:
                log.debug(log_message)
        if vals is None:
            vals = {}
        return vals, string

    def get_variables(self, dependencies=None):
        return set(self.parser._named_fields)

    def read(self, line, dependencies=None, raise_error=False):
        return self.parse(line, raise_error=raise_error)

    def write(self, content):
        return self.format(**content)


class Conditional(Pattern):
    """
    Examples:
        >>> import transcoding as tc
        >>> pattern = tc.Conditional(('number', 'variables', -1),
        ...                          (1, 2),
        ...                          ('entry_{v0}', 'entry_{v0}_entry_{v1}'))
        >>> sorted(pattern.variables)
        ['v0', 'v1']

        >>> line = 'entry_42_entry_21'
        >>> content = {'number': {'variables': [1, 2]}}
        >>> values = pattern.read(line, content)
        >>> values['v1'] == '21'
        True
        >>> content.update(values)
        >>> pattern.write(content) == line
        True

    """
    def __init__(self, keys, values, patterns, read_method=None):
        self._patterns = [Pattern(p) for p in patterns]
        self._keys = keys
        self._values = values
        super(Conditional, self).__init__(None, read_method)

    def get_pattern(self, dependencies):
        dependency_value = dependencies
        for key in self._keys:
            dependency_value = dependency_value[key]

        for value, pattern in zip(self._values, self._patterns):
            if value == dependency_value:
                break
        return pattern

    def get_variables(self, dependencies=None):
        return self.get_pattern(dependencies).get_variables()
        
    def read(self, line, dependencies=None, raise_error=False):
        if self.read_method is not None:
            vals = self.read_method(line,
                                    dependencies=dependencies,
                                    raise_error=raise_error)
        else:
            pattern = self.get_pattern(dependencies)
            vals = pattern.read(line,
                                dependencies=dependencies,
                                raise_error=raise_error)
        return vals

    def write(self, content):
        pattern = self.get_pattern(content)
        return pattern.format(**content)

    @property
    def variables(self):
        variables = set([])
        for pattern in self._patterns:
            variables = variables.union(pattern.variables)
        return variables


if __name__ == '__main__':
    import doctest
    doctest.testmod()
