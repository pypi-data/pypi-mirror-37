"Yet another pretty print table"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2018, Paresh Adhia"

from decimal import Decimal
import datetime as dt

class HumanInt(int):
	"An int subclass that formats values for human readability (similar to --human-readable option of the ls command)"
	def __format__(self, spec):
		if spec == '':
			width, prec, typ = None, '.1', 'h'
		else:
			import re
			m = re.match(r'(\d*)(.\d+)?(h|s|e)$', spec)
			if not m:
				return int.__format__(self, spec)
			width, prec, typ = m.groups()

		if typ == 'e':
			if prec:
				raise ValueError('Precision not allowed in integer format specifier')

			if self == 0:
				s = '0'
			else:
				for e in [12, 9, 6, 3, 0]:
					if self % 10**e == 0:
						break
				s = (str(self // 10**e) + 'e' + str(e)) if e else str(self)

		else:
			num = float(self)
			base = 1000.0 if typ == 's' else 1024.0

			for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']:
				if num < base:
					break
				num /= base

			fmt = ',' + (prec or '.0') + 'f'
			s = format(num, fmt)
			if '.' in s:
				s = s.rstrip('0').rstrip('.')
			s += unit

		return s.rjust(int(width)) if width else s

class PPCol:
	"Pretty printer for a column within a table"
	@staticmethod
	def make_fmtval(ctype):
		"make format function based on type"
		return next(
			(fn for types, fn in [
				(HumanInt, lambda v: HumanInt.__format__(v, '.1h')),
				(int, lambda v: format(v, ',d')),
				((float, Decimal), lambda v: format(v, ',.2f')),
				(object, str),
			] if issubclass(ctype, types)),
		)

	@staticmethod
	def make_justify(ctype):
		"make justify function based on type"
		return str.rjust if issubclass(ctype, (int, float, Decimal, dt.date, dt.datetime, dt.time, dt.timedelta)) else str.ljust

	@staticmethod
	def create(col, infer_from=None):
		"create a new instance depedning on parameter type"
		if isinstance(col, PPCol): return col
		if isinstance(col, tuple): return PPCol(col[0], col[1] or next((type(v) for v in (infer_from or []) if v != None), None))
		if isinstance(col, str): return PPCol(col, next((type(v) for v in (infer_from or []) if v != None), None))
		return PPCol(col, str)

	def __init__(self, title, ctype=None, fmtval=None, justify=None, width=1):
		self.title = title or ''
		self.width = max(width, len(self.title))
		self.fmtval = fmtval or (self.make_fmtval(ctype) if ctype else str)
		self._justify = justify or (self.make_justify(ctype) if ctype else str.ljust)

	def justify(self, val):
		"justify value"
		return self._justify(val, self.width)

	def __str__(self):
		return f"{self.title}:{self.width}"

branch_styles = {
	'fancy': {'T': "├─ ", 'L': "└─ ", 'I': "│  ", ' ': "   "}, # uses Unicode codepoints
	'ascii': {'T': "|- ", 'L': "L_ ", 'I': "|  ", ' ': "   "}, # uses only ASCII characters
}
def treeiter(root, getch=lambda n: n.children, style='fancy'):
	"""
	returns an iterator that iterates in inpute iterator with pair (trunk, elem)
	where elem is element from the input iterator and,
	trunk is tree's current trunk at that element
	"""
	def extend(trunk, by):
		"extend the trunk by a new brach"
		return trunk.replace('L', ' ').replace('T', 'I') + by

	def lpos_iter(in_iter):
		"an iterator which returns tuple (lpos, item) where lpos is True if this is the last item from the original iterator"
		has_prev, prev = False, None
		for child in in_iter:
			if has_prev:
				yield False, prev
			has_prev, prev = True, child
		if has_prev:
			yield True, prev

	def walk(node, trunk):
		"Visits node and its children in order"
		yield (trunk, node)
		for is_last, child in lpos_iter(getch(node)):
			yield from walk(child, extend(trunk, 'L' if is_last else 'T'))

	def stylize(trunk):
		"stylize the trunk if style is not None"
		return trunk if style is None else ''.join(branch_styles[style][c] for c in trunk)

	for trunk, node in walk(root, ''):
		yield (stylize(trunk), node)

def formatted(rows, columns=None, none_value='', dash='-'):
	"return formatted rows. Inspired by https://bitbucket.org/astanin/python-formatted"

	table = [list(r) for r in zip(*rows)]  # transpose
	if not table and not columns:
		return
	if columns:
		if table:
			if len(columns) != len(table):
				raise ValueError('Number of columns in data must match column definitions')
			columns = [PPCol.create(c, v) for c, v in zip(columns, table)]
		else:
			columns = [PPCol.create(c) for c in columns]
	else:
		columns = [PPCol.create('', v) for v in table]

	# stage 1: transform table values to formatted string
	table = [[c.fmtval(v) if v != None else none_value for v in vals] for c, vals in zip(columns, table)]

	# adjust max width, if needed, before the second stage
	for col, w in zip(columns, [max(len(v) for v in vals) for vals in table]):
		if w > col.width:
			col.width = w

	# stage 2: justify table values
	table = [[c.justify(v) for v in vals] for c, vals in zip(columns, table)]

	if [c.title for c in columns if c.title]: # print column titles if at least one is non-blank
		yield [c.justify(c.title) for c in columns]
		if dash:
			yield [''.ljust(c.width, dash) for c in columns]

	yield from zip(*table) # transform table to rows

def tabulate(rows, columns=None, sep=' ', end='\n', none_value='', dash='-'):
	"format and return table as a string"
	return end.join(sep.join(row) for row in formatted(rows, columns, none_value=none_value, dash=dash))

def pprint(rows, columns=None, sep=' ', end='\n', none_value='', dash='-', file=None, flush=False):
	"print formatted tabular data"
	print(tabulate(rows, columns, sep=sep, end=end, none_value=none_value, dash=dash), file=file, flush=flush)
