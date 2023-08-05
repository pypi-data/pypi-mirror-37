"""Spell check with Aspell or Hunspell."""
from __future__ import unicode_literals
import os
import codecs
import importlib
from . import util
from . import __version__
from wcmatch import glob

version = __version__.version
version_info = __version__.version_info

glob_flag_map = {
    "FORECECASE": glob.F,
    "F": glob.F,
    "IGNORECASE": glob.I,
    "I": glob.I,
    "RAWCHARS": glob.R,
    "R": glob.R,
    "NEGATE": glob.N,
    "N": glob.N,
    "MINUSNEGATE": glob.M,
    "M": glob.M,
    "GLOBSTAR": glob.G,
    "G": glob.G,
    "DOTGLOB": glob.D,
    "D": glob.D,
    "EXTGLOB": glob.E,
    "E": glob.E,
    "BRACE": glob.B,
    "B": glob.B
}


class Aspell(object):
    """Aspell spell check class."""

    DICTIONARY = 'dictionary.dic'

    def __init__(self, config, name='', binary='', verbose=0):
        """Initialize."""

        # General options
        self.name = name
        self.binary = binary if binary else 'aspell'
        self.verbose = verbose
        self.dict_bin = os.path.abspath(self.DICTIONARY)
        self.documents = config.get('documents', [])
        self.dictionary = config.get('dictionary', [])

    def log(self, text, level):
        """Log level."""
        if self.verbose >= level:
            print(text)

    def normalize_utf(self, encoding):
        """Normalize UTF encoding."""

        if encoding == 'utf-8-sig':
            encoding = 'utf-8'
        if encoding.startswith('utf-16'):
            encoding = 'utf-16'
        elif encoding.startswith('utf-32'):
            encoding = 'utf-32'
        return encoding

    def setup_command(self, encoding, options, personal_dict):
        """Setup the command."""

        cmd = [
            self.binary,
            'list',
            '--encoding', codecs.lookup(encoding).name
        ]

        if personal_dict:
            cmd.extend(['--add-extra-dicts', personal_dict])

        allowed = {
            'conf-dir', 'data-dir', 'add-dict-alias', 'rem-dict-alias', 'dict-dir',
            'encoding', 'add-filter', 'rem-filter', 'add-filter-path', 'rem-filter-path',
            'mode', 'e', 'H', 't', 'n', 'add-extra-dicts', 'rem-extra-dicts', 'home-dir',
            'ingore', 'W', 'dont-ignore-case', 'ignore-case', 'lang', 'l', 'local-data-dir',
            'd', 'master', 'dont-normalize', 'normalize', 'dont-norm-required',
            'norm-required', 'norm-form', 'dont-norm-strict', 'norm-strict', 'per-conf',
            'p', 'personal', 'C', 'B', 'dont-run-together', 'run-together', 'run-together-limit',
            'run-together-min', 'use-other-dicts', 'dont-use-other-dicts', 'add-variety', 'rem-variety',
            'add-context-delimiters', 'rem-context-delimiters', 'dont-context-visible-first',
            'context-visible-first', 'add-email-quote', 'rem-email-quote', 'email-margin',
            'add-html-check', 'rem-html-check', 'add-html-skip', 'rem-html-skip', 'add-sgml-check',
            'rem-sgml-check', 'add-sgml-skip', 'rem-sgml-skip', 'dont-tex-check-comments',
            'tex-check-comments', 'add-tex-command', 'rem-tex-command', 'add-texinfo-ignore',
            'rem-texinfo-ignore', 'add-texinfo-ignore-env', 'rem-texinfo-ignore-env', 'filter'
        }

        for k, v in options.items():
            if k in allowed:
                key = ('-%s' if len(k) == 1 else '--%s') % k
                if isinstance(v, bool) and v is True:
                    cmd.append(key)
                elif isinstance(v, util.ustr):
                    cmd.extend([key, v])
                elif isinstance(v, int):
                    cmd.extend([key, util.ustr(v)])
                elif isinstance(v, list):
                    for value in v:
                        cmd.extend([key, util.ustr(value)])
        return cmd

    def _check_spelling(self, sources, options, personal_dict, filter_index=1):
        """Recursive check spelling filters."""
        for source in sources:
            if source._has_error():
                yield source
            elif not source._is_bytes():
                if filter_index < len(self.filters):
                    f = self.filters[filter_index]
                    if source.category not in f._get_disallowed():
                        yield from self._check_spelling(
                            f.sfilter(source), options, personal_dict, filter_index + 1
                        )
                    else:
                        yield source
                else:
                    yield source
            else:
                yield source

    def check_spelling(self, sources, options, personal_dict):
        """Check spelling."""

        for source in self._check_spelling(sources, options, personal_dict):
            if source._has_error():
                yield util.Results([], source.context, source.category, source.error)
            else:
                if source._is_bytes():
                    text = source.text
                else:
                    text = source.text.encode(self.normalize_utf(source.encoding))
                self.log(text, 3)
                cmd = self.setup_command(self.normalize_utf(source.encoding), options, personal_dict)
                self.log(str(cmd), 2)

                wordlist = util.console(cmd, input_text=text)
                yield util.Results([w for w in sorted(set(wordlist.split('\n'))) if w], source.context, source.category)

    def compile_dictionary(self, lang, wordlists, output):
        """Compile user dictionary."""

        output_location = os.path.dirname(output)
        if not os.path.exists(output_location):
            os.makedirs(output_location)
        if os.path.exists(output):
            os.remove(output)

        self.log("Compiling Dictionary...", 1)
        # Read word lists and create a unique set of words
        words = set()
        for wordlist in wordlists:
            with open(wordlist, 'rb') as src:
                for word in src.read().split(b'\n'):
                    words.add(word.replace(b'\r', b''))

        # Compile wordlist against language
        util.console(
            [
                self.binary,
                '--lang', lang,
                '--encoding=utf-8',
                'create',
                'master', output
            ],
            input_text=b'\n'.join(sorted(words)) + b'\n'
        )

    def walk_src(self, targets, flags, plugin):
        """Walk source and parse files."""

        for target in targets:
            patterns = glob.globsplit(target, flags=flags)
            for f in glob.iglob(patterns, flags=flags):
                if not os.path.isdir(f):
                    yield plugin._parse(f)

    def setup_spellchecker(self, documents):
        """Setup spell checker."""

        return documents.get('aspell', {})

    def setup_dictionary(self, documents):
        """Setup dictionary."""

        dictionary_options = documents.get('dictionary', {})
        output = os.path.abspath(dictionary_options.get('output', self.dict_bin))
        lang = dictionary_options.get('lang', 'en')
        wordlists = dictionary_options.get('wordlists', [])
        if lang and wordlists:
            self.compile_dictionary(lang, dictionary_options.get('wordlists', []), output)
        else:
            output = None
        return output

    def get_filters(self, documents, default_encoding):
        """Get filters."""

        self.filters = []
        kwargs = {}
        if default_encoding:
            kwargs["default_encoding"] = default_encoding
        filters = documents.get('filters', [])
        if not filters:
            filters.append('pyspelling.filters.text')
        for f in filters:
            # Retrieve module and module options
            if isinstance(f, dict):
                name, options = list(f.items())[0]
            else:
                name = f
                options = {}
            if options is None:
                options = {}

            self.filters.append(self.get_module(name, 'get_filter')(options, **kwargs))

    def get_module(self, module, accessor):
        """Get module."""

        if isinstance(module, util.string_type):
            mod = importlib.import_module(module)
        attr = getattr(mod, accessor, None)
        if not attr:
            raise ValueError("Could not find accessor '%s'!" % accessor)
        return attr()

    def _to_flags(self, text):
        """Convert text representation of flags to actual flags."""

        flags = 0
        for x in text.split('|'):
            value = x.strip().upper()
            if value:
                flags |= glob_flag_map.get(value, 0)
        return flags

    def check(self):
        """Walk source and initiate spell check."""

        for documents in self.documents:
            if self.name and self.name != documents.get('name', ''):
                continue

            # Perform spell check
            self.log('\nSpell Checking %s...' % documents.get('name', ''), 1)

            # Setup filters and variables for the spell check
            encoding = documents.get('default_encoding', '')
            options = self.setup_spellchecker(documents)
            output = self.setup_dictionary(documents)
            glob_flags = self._to_flags(documents.get('glob_flags', "N|B|G"))
            self.get_filters(documents, encoding)

            for sources in self.walk_src(documents.get('sources', []), glob_flags, self.filters[0]):
                for result in self.check_spelling(sources, options, output):
                    yield result


# class Hunspell(Aspell):
#     """Hunspell spell check class."""

#     def setup_spellchecker(self, documents):
#         """Setup spell checker."""

#         return documents.get('hunspell', {})

#     def setup_dictionary(self, documents):
#         """Setup dictionary."""

#         dictionary_options = documents.get('dictionary', {})
#         output = os.path.abspath(dictionary_options.get('output', self.dict_bin))
#         lang = dictionary_options.get('lang', 'en_US')
#         wordlists = dictionary_options.get('wordlists', [])
#         if lang and wordlists:
#             self.compile_dictionary(lang, dictionary_options.get('wordlists', []), output)
#         else:
#             output = None
#         return output

#     def compile_dictionary(self, lang, wordlists, output):
#         """Compile user dictionary."""

#         output_location = os.path.dirname(output)
#         if not os.path.exists(output_location):
#             os.makedirs(output_location)
#         if os.path.exists(output):
#             os.remove(output)

#         self.log("Compiling Dictionary...", 1)
#         # Read word lists and create a unique set of words
#         words = set()
#         for wordlist in wordlists:
#             with open(wordlist, 'rb') as src:
#                 for word in src.read().split(b'\n'):
#                     words.add(word.replace(b'\r', b''))

#         # Sort and create wordlist
#         with open(self.dict_bin, 'wb') as dest:
#             dest.write(b'\n'.join(sorted(words)) + b'\n')

#     def setup_command(self, encoding, options, personal_dict):
#         """Setup command."""

#         cmd = [
#             'hunspell',
#             '-l',
#             '-i', codecs.lookup(encoding).name
#         ]

#         if personal_dict:
#             cmd.extend(['-p', personal_dict])

#         allowed = {
#             'check-apostrophe', 'check-url',
#             'i', 'd' 'H', 'n', 'o', 'r', 't', 'X'
#         }

#         for k, v in options.items():
#             if k in allowed:
#                 key = ('-%s' if len(k) == 1 else '--%s') % k
#                 if isinstance(v, bool) and v is True:
#                     cmd.append(key)
#                 elif isinstance(v, util.ustr):
#                     cmd.extend([key, v])
#                 elif isinstance(v, int):
#                     cmd.extend([key, util.ustr(v)])
#                 elif isinstance(v, list):
#                     for value in v:
#                         cmd.extend([key, util.ustr(value)])
#         return cmd
