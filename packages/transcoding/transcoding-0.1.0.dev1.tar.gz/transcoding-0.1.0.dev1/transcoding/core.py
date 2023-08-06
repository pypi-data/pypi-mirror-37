"""
Known Problems:
    * Numbers with trailing floating point but no number behind the point like
        '0. 1. ' can not be produced and thus not be parsed with format patterns.
    * format spec ' .4e', '+.4e' not registered -> # show a space or a + for positive numbers
"""
from transcoding import Trigger, LooseTrigger, time_shift
from transcoding import Pattern, Conditional, ParseError

from past.builtins import basestring
import os
from more_itertools import peekable
import logging
import io


class Block(object):
    def __init__(self, *patterns, **kwargs):
        """
        Abstract base class for blocks in a file.
        Each file can be fully described by an arbitrary amount of Blocks.

        Args:
            *patterns (str): format_spec string.
                Use variables only with explicit variable names ie.
                    'the value is {val:.2f} m'.
                Do not use patterns ie.
                    'the value is {0}'.
            **kwargs
                start (Trigger): defines from where to read/write
                stop (Trigger): defines until where to read/write
                barrier (Trigger): like stop but will also trigger if not yet
                    started
                default (dict): default to return if nothing was read

        Attrs:
            _counter (int): points to currently active pattern / variable
            _patterns (list): patterns to parse / format in read/write mode

        Examples:
        """
        start = kwargs.pop('start', None)
        stop = kwargs.pop('stop', None)
        barrier = kwargs.pop('barrier', None)
        default = kwargs.pop('default', None)

        log = logging.getLogger()
        if start is None:
            start = LooseTrigger(lambda x: True, delay=0)
        else:
            # copy triggers in order to not work on the initial instance.
            start = start.copy()
        if stop is None:
            stop = LooseTrigger(lambda x: True, delay=len(patterns))
        else:
            # copy triggers in order to not work on the initial instance.
            stop = stop.copy()
        if barrier is None:
            barrier = LooseTrigger(lambda x: False, delay=0)
        else:
            barrier = barrier.copy()
        self.start = start
        self.stop = stop
        self.barrier = barrier
        self.default = default
        self.patterns = patterns
        self._counter = 0
        if len(kwargs) != 0:
            log.error("kwargs {kwargs} were not "
                           "consumed.".format(**locals()))

    def copy(self):
        kwargs = {}
        for attr in dir(self.__class__):
            if isinstance(getattr(self.__class__, attr), property):
                val = getattr(self, attr)
                if hasattr(val, 'copy'):
                    val = val.copy()
                kwargs[attr] = val
        return self.__class__(*kwargs.pop('patterns'),
                              **kwargs)

    @property
    def patterns(self):
        """
        list of str: patterns to parse / format in read/write mode
        """
        return self._patterns

    @patterns.setter
    def patterns(self, patterns):
        log = logging.getLogger()
        if not hasattr(patterns, '__iter__'):
            patterns = [patterns]
        self._patterns = []
        for p in patterns:
            if issubclass(type(p), Pattern):
                self._patterns.append(p)
            else:
                self._patterns.append(Pattern(p))

    @property
    def start(self):
        """
        transcodings.Trigger: Start trigger
        """
        return self._start
    
    @start.setter
    def start(self, start):
        self._start = start.copy()

    @property
    def stop(self):
        """
        transcodings.Trigger: Stop trigger
        """
        return self._stop

    @stop.setter
    def stop(self, stop):
        self._stop = stop.copy()

    @property
    def barrier(self):
        """
        transcodings.Trigger: Barrier. If this trigger turns on, finish this
            block.
        """
        return self._barrier

    @barrier.setter
    def barrier(self, barrier):
        self._barrier = barrier.copy()

    @property
    def default(self):
        """
        dict: default values of this block
        """
        return dict(self._default)

    @default.setter
    def default(self, default):
        if default is None:
            default = {}
        self._default = default

    def startswith(self, string):
        """
        Check wether first pattern starts with string
        """
        return self.patterns[0].startswith(string)

    def _expired(self):
        """
        Returns
                False: started but not stopped / not yet started
                True: started and stopped again
        """
        return (self._stop.active() and self._start.active()) or self._barrier.active()

    def _get_line(self, iterator):
        """
        Args:
            iterator (peekable)
        Returns:
            line (None / str): None if the trigger is not met
        """

        next_line = iterator.peek(None)

        # feed triggers
        self._start(next_line)
        self._barrier(next_line)
        if self._barrier.active():
            return None

        if self._start.found():
            # stop will not be checked untill start trigger has been found
            self._stop(next_line)

        if self._stop.active():
            return None

        line = iterator.next()
        if self._start.active():
            return line
        else:
            return None

    def _get_pattern(self):
        """
        Returns:
            str: the pattern at counter
        """
        pattern = self.patterns[self._counter]
        return pattern

    def reset(self):
        self._start.reset()
        self._stop.reset()
        self._barrier.reset()
        self._counter = 0

    def _write_line(self, values):
        """
        Args:
            values (dict)
        """
        pattern = self._get_pattern()
        line = pattern.write(values)
        return line

    def _write(self, values):
        log = logging.getLogger()
        while not self._expired():
            # create line with format
            line = self._write_line(values)
            self._start(line)
            self._stop(line)
            if line is not None:
                yield line
            self._counter += 1
        if not self._start.active():
            log.error("Block did not trigger before terminating.\n"
                      "\t\t\tpatterns:\t%r" % ([p._format_string for p in self.patterns]))

    def write(self, values):
        """
        Args:
            values (dict): content to write. needs to fulfill the pattern
        """
        self.reset()
        with time_shift(-1, self._start, self._stop):
            lines = list(self._write(values))
        return lines

    def _read_line(self, line, **kwargs):
        return self._get_pattern().read(line, **kwargs)

    def _read(self, iterator, **kwargs):
        log = logging.getLogger()
        while not self._expired():
            line = self._get_line(iterator)
            if line is not None:
                val = self._read_line(line, **kwargs)
                if val is not None:
                    yield val
                self._counter += 1
        if not self._start.active():
            log.error("Block did not trigger before terminating.\n"
                      "\t\t\tpatterns:\t%r" % (self.patterns))

    def read(self, iterator, **kwargs):
        """
        Args:
            iterator (peekable): iterator containing strings to process
            **kwargs:
                dependencies: already proecessed parts of iterator
                    This is only necessary if your processing pattern depends on any
                    value that was already processed
        """
        self.reset()
        vals = self.default
        for newVals in self._read(iterator, **kwargs):
            vals.update(newVals)
        return vals


class Table(Block):
    """
    Examples:
        >>> from more_itertools import peekable
        >>> import transcoding as tc
        >>> pattern = " {d} = {x:.4e} {y:.4e}"
        >>> start = tc.Trigger(lambda x: 'RAXIS' in x, delay=0)
        >>> stop = tc.Trigger(lambda x: not bool(x), delay=0)

        >>> inp =  " RAXIS = 5.6102e+00 3.7067e-01\\n"
        >>> inp += " ZAXIS = -0.0000e+00 -2.9784e-01"
        >>> inp = inp.split("\\n")

        reading with the same pattern
        >>> iterator = peekable(inp)

        >>> t = tc.Table(pattern, start=start, stop=stop)
        >>> values = t.read(iterator)
        >>> values['y'] == [0.37067, -0.29784]
        True

        write
        >>> outp = t.write(values)
        >>> assert(all([a == b for a, b in zip(inp, outp)]))

    """
    def __init__(self, *args, **kwargs):
        stop = kwargs.get('stop', None)
        if stop is None:
            raise ValueError("stop is a mandatory attribute for Table.")
        super(Table, self).__init__(*args, **kwargs)

    def _get_pattern(self):
        pattern = self.patterns[0]
        return pattern

    def _write_line(self, values):
        """
        Args:
            values (dict)
        """
        pattern = self._get_pattern()
        any_variable = list(self._get_pattern().get_variables(values))[0]
        length = len(values[any_variable])
        if self._counter >= length:
            self._stop.activate()
            line = None
        else:
            line = pattern.write({var: values[var][self._counter]
                                  for var in pattern.get_variables(values)})
        return line

    def read(self, iterator, **kwargs):
        dependencies = kwargs.get('dependencies', None)
        self.reset()
        # kwargs['raise_error'] = True
        read_dicts = self._read(iterator, **kwargs)
        output = self.default
        merged = merge(read_dicts,
                       self._get_pattern().get_variables(dependencies))
        output.update(merged)
        return output


def merge(dicts, variables):
    """
    Merge multiple dicts to one dict with lists
    """
    vals = {attr: [] for attr in variables}
    for d in dicts:
        if d is None or d == {}:
            continue
        for attr in variables:
            vals[attr].append(d[attr])
    return vals


class List(Block):
    def __init__(self, *args, **kwargs):
        self._separator = kwargs.pop('separator')
        self._prefix = kwargs.pop('prefix', '')
        self._suffix = kwargs.pop('suffix', '')
        super(List, self).__init__(*args, **kwargs)

    @property
    def separator(self):
        return self._separator

    @property
    def prefix(self):
        return self._prefix

    @property
    def suffix(self):
        return self._suffix

    def _get_pattern(self):
        pattern = self.patterns[0]
        return pattern

    def _read_line(self, line, **kwargs):
        log = logging.getLogger()
        vals = {}
        if self.prefix is not None:
            import pyTools
            preVals, line = interprete_margin(line,
                                              *pyTools.flatten([self.prefix]),
                                              left=True)
            vals.update(preVals)
        if self.suffix is not None:
            import pyTools
            sufVals, line = interprete_margin(line,
                                              *pyTools.flatten([self.suffix]),
                                              left=False)
            vals.update(sufVals)

        splitLine = line.split(self.separator)
        while '' in splitLine:
            splitLine.remove('')
            # log.warning("'' in splitLine!")
        listVals = merge([super(List, self)._read_line(entry,
                                                       **kwargs)
                          for entry in splitLine],
                         self.patterns[0].get_variables(iterator))
        listVals.update(preVals)
        listVals.update(sufVals)
        return listVals


class Jump(Block):
    def __init__(self, trigger):
        """
        Jump the iterator to the trigger and immediate stop.
        This will destroy bijectivity of a transcoding,
        ie reading and writing again will produce a
        different file.

        Args:
            trigger (transcodings.Trigger): 
        """
        start = trigger
        stop = trigger
        super(Jump, self).__init__(None, start=start, stop=stop)


class Loop(object):
    """
    Collection of repeating structures
    Args:
        name
        blocks (list of Block instances)
        **kwargs:
            head (Bock instance): header of loop
            foot (Bock instance): footer of loop

    Examples:
        >>> from more_itertools import peekable
        >>> import transcoding as tc
        >>> start = tc.Trigger(lambda x: 'RAXIS' in x, delay=0)
        >>> stop = tc.Trigger(lambda x: not bool(x), delay=0)

        >>> inp =  "Start - Name: Looping Lui\\n"
        >>> inp += "Loop 1\\n"
        >>> inp += "Fly high\\n"
        >>> inp += "Fly low\\n"
        >>> inp += "Fly high\\n"
        >>> inp += "Loop 2\\n"
        >>> inp += "Fly low\\n"
        >>> inp += "Fly high\\n"
        >>> inp += "Fly low\\n"
        >>> inp += "Stop - Status: dizzy"
        >>> inp = inp.split("\\n")

        reading with the same pattern
        >>> iterator = peekable(inp)

        >>> l = tc.Loop("looping lui",
        ...             [tc.Block("Loop {loop_no:d}"),
        ...              tc.Table("Fly {fly_value}",
        ...                       stop=tc.Trigger(lambda x: 'Loop' in x or 'Stop' in x))
        ...             ],
        ...             head=tc.Block("Start - Name: {loop_name}"),
        ...             foot=tc.Block("Stop - Status: {loop_status}",
        ...                           start=tc.Trigger(lambda x: 'Stop' in x)))

        >>> values = l.read(iterator)
        >>> values['looping lui'][1]['fly_value']
        ['low', 'high', 'low']
        >>> values['loop_status']
        'dizzy'

        write
        >>> outp = l.write(values)
        >>> assert(all([a == b for a, b in zip(inp, outp)]))

    """
    def __init__(self, name, blocks, **kwargs):
        self._name = name
        if not blocks:
            raise ValueError("Trivial Loop without Blocks.")
        self.blocks = blocks
        self.stop_iter = kwargs.pop('stop_iter', None)
        self.head = kwargs.pop('head', None)
        self.foot = kwargs.pop('foot', None)

    @property
    def name(self):
        return self._name

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, blocks):
        self._blocks = [b.copy() for b in blocks]

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        if head is not None:
            head = head.copy()
        self._head = head

    @property
    def foot(self):
        return self._foot

    @foot.setter
    def foot(self, foot):
        if foot is not None:
            foot = foot.copy()
        if not issubclass(type(foot._start), LooseTrigger):
            if self.stop_iter is None:
                self.stop_iter = foot._start
        self._foot = foot
    
    @property
    def stop_iter(self):
        """
        (Trigger): if stop_iter triggers, this is the signal for the loop to
            terminate
        """
        return self._stop_iter

    @stop_iter.setter
    def stop_iter(self, stop_iter):
        if stop_iter is not None:
            stop_iter = stop_iter.copy()
            stop_iter.reset()
        self._stop_iter = stop_iter

    def _get_first_block(self):
        """
        Returns:
            first occuring block
        """
        if self.head:
            block = self.head
        else:
            block = self.blocks[0]
        return block

    def __getattr__(self, attr):
        if attr == 'startswith':
            return self._get_first_block().startswith
        else:
            raise AttributeError("'{cls}' object has no attribute '{attr}'"
                                 .format(attr=attr, cls=type(self).__name__))

    def _read_body(self, iterator, **kwargs):
        dependencies = kwargs.get('dependencies', {})
        body = []
        start_iter = self.blocks[0]._start.copy()
        if self.stop_iter is None:
            raise ValueError("Please define the end of iteration with the "
                             "stop_iter attribute")
        while True:
            next_line = iterator.peek(None)

            # feed triggers
            start_iter(next_line)
            self.stop_iter(next_line)
            if not start_iter.found() or self.stop_iter.found():
                break
            while start_iter.active_in > 1:
                # forward unto start of loop
                iterator.next()
                next_line = iterator.peek(None)
                # feed triggers
                start_iter(next_line)
                self.stop_iter(next_line)

            # read blocks
            loop_iteration_dict = {}
            for block in self.blocks:
                loop_iteration_dict.update(block.read(iterator, **kwargs))
                if self.name not in dependencies:
                    dependencies[self.name] = [loop_iteration_dict]
                else:
                    dependencies[self.name].append(loop_iteration_dict)
            body.append(loop_iteration_dict)

            start_iter.reset()
                
        body_dict = {self.name: body}
        return body_dict

    def read(self, iterator, **kwargs):
        """
        Read in order head, body, foot
        """
        out_dict = dict()
        if self.head is not None:
            out_dict.update(self.head.read(iterator, **kwargs))

        body_dict = self._read_body(iterator, **kwargs)

        out_dict.update(body_dict)
        if self.foot is not None:
            out_dict.update(self.foot.read(iterator, **kwargs))
        return out_dict

    def write(self, values):
        """
        Write in order head, body, foot
        """
        lines = []
        if self.head:
            lines.extend(self.head.write(values))
        for loop_values in values[self.name]:
            for block in self.blocks:
                lines.extend(block.write(loop_values))
        if self.foot:
            lines.extend(self.foot.write(values))
        return list(lines)


class Transcoding(object):
    """
    Abstract Class that handles transcodings.
    Transcodings are ordered blocks that describe a whole file format.
    See ./transcodings/*.py as examples.
    """
    def __init__(self, *blocks, **kwargs):
        self._blocks = blocks

    @property
    def blocks(self):
        return self._blocks

    def read(self, inp):
        """
        inp will be file object or iterable
        """
        log = logging.getLogger()
        if isinstance(inp, basestring):
            path = os.path.realpath(os.path.abspath(os.path.expanduser(inp)))
            with open(path, 'r') as f:
                inp = f.read().split('\n')
        if isinstance(inp, io.IOBase) or isinstance(inp, file):
            inp = inp.read().split('\n')
        if isinstance(inp, list):
            iterator = peekable(inp)
        else:
            raise ValueError("Input must either be str, buffer or list but is"
                             " {tpe}".format(tpe=type(inp)))
        content_dict = dict()
        for i, block in enumerate(self.blocks):
            try:
                out = block.read(iterator, dependencies=content_dict)
                content_dict.update(out)
            except Exception as err:
                log.exception("Error in block {i}:\n".format(**locals()) +
                              str(err))
                raise err
        return content_dict


def importTranscoding(filePath):
    import imp
    if os.path.exists(filePath):
        transMod = imp.load_source(os.path.basename(filePath).rstrip('.py'), filePath)
    else:
        predefined = "transcodings.{extension}".format(extension=filePath)
        filePath = predefined
        transMod = __import__(filePath, fromlist=[''])
    return transMod


def get_transcoding(filePath):
    transMod = importTranscoding(filePath)
    return transMod.transcoding


if __name__ == '__main__':
    import doctest
    doctest.testmod()
