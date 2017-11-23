import xenon
import textwrap

xenon.init()


class Table:
    def __init__(self, headings, data):
        self.headings = headings
        self.data = data
        self.n_cols = len(self.headings)
        self.n_rows = len(self.data)

    @staticmethod
    def from_sequence(seq, **getters):
        headings = list(getters.keys())
        data = [
            tuple(getters[k](x) for k in headings)
            for x in seq
        ]
        return Table(headings, data)

    def print_rst(self, fmt_width=100):
        column_max = [
            max(max(len(row[c]) for row in self.data), len(self.headings[c]))
            for c in range(self.n_cols)
        ]

        # take all columns that are less than 10 characters max, and see how
        # much space we have left
        space_left = fmt_width - sum(n for n in column_max if n <= 30)
        space_needed = sum(n > 30 for n in column_max) * 30

        if space_needed > space_left:
            raise ValueError("Table is too wide.")

        large_column_width = space_left \
            // max(1, sum(n > 30 for n in column_max))
        aimed_column_width = [
            min(large_column_width, n) for n in column_max
        ]

        def max_width(text, aimed_width):
            return max(
                len(l)
                for l in textwrap.wrap(
                    text, width=aimed_width, break_long_words=False))

        def column_min_widths():
            return [
                max(max(
                    max_width(row[i], aimed_column_width[i])
                    for row in self.data), aimed_column_width[i])
                for i in range(self.n_cols)]

        column_width = column_min_widths()

        def hline(c):
            return '+' + c + (c + '+' + c).join(c*w for w in column_width) \
                + c + '+'

        def row_height(row):
            return max(
                len(textwrap.wrap(x, width=w))
                for x, w in zip(row, column_width))

        def row_strings(row):
            texts = [
                textwrap.wrap(x, width=w)
                for x, w in zip(row, column_width)
            ]
            row_height = max(len(t) for t in texts)

            def extend_text(text, width):
                n = len(text)
                r = [t + ' ' * (width - len(t)) for t in text] + \
                    [' ' * width] * (row_height - n)
                return r

            extended_texts = list(map(extend_text, texts, column_width))

            return [
                '| ' + ' | '.join(t[l] for t in extended_texts) + ' |'
                for l in range(row_height)
            ]

        print(hline('-'))
        for l in row_strings(self.headings):
            print(l)
        print(hline('='))
        for row in self.data:
            for l in row_strings(row):
                print(l)
            print(hline('-'))


def property_table(d):
    def prop_typename(p):
        typemap = {v: k for k, v in p.Type.items()}
        return typemap[p.type].lower()

    return Table.from_sequence(
        d.supported_properties,
        name=lambda p: '.'.join(p.name.split('.')[3:]),
        description=lambda p: p.description,
        data_type=prop_typename,
        default=lambda p: ('`{}`'.format(p.default_value)
                           if p.default_value else '(empty)'))


def print_adaptor_descriptions(desc, extra=[]):
    for d in desc:
        print(d.name.title())
        print('~' * len(d.name))
        print(textwrap.fill(d.description))
        print()
        if extra:
            Table.from_sequence(
                extra,
                field=lambda x: x,
                value=lambda x: str(getattr(d, x))).print_rst()
            print()
        print('location string:')
        print('\n'.join('    * `{}`'.format(l) for l in d.supported_locations))
        print()
        print('supported properties:')
        print()
        property_table(d).print_rst()
        print()


scheduler_adaptor_props = [
    'is_embedded',
    'supports_interactive',
    'supports_batch',
    'uses_file_system'
]

file_system_adaptor_props = [
    'supports_third_party_copy',
    'can_create_symboliclinks',
    'can_read_symboliclinks',
    'is_connectionless'
]

print("""Adaptors
========
This section contains the adaptor documentation which is generated from the
information provided by the adaptors themselves.

.. contents::

""")

print("File System")
print("-----------")
print("""
.. note:: Supported property names should be prefixed with
``"xenon.adaptors.filesystems"``.  We've left this prefix out to improve
readability of the tables.
""")
print()
print_adaptor_descriptions(
    xenon.FileSystem.get_adaptor_descriptions(),
    extra=file_system_adaptor_props)
print()

print("Scheduler")
print("---------")
print("""
.. note:: Supported property names should be prefixed with
``"xenon.adaptors.schedulers"``.  We've left this prefix out to improve
readability of the tables.
""")
print()
print_adaptor_descriptions(
    xenon.Scheduler.get_adaptor_descriptions(),
    extra=scheduler_adaptor_props)
