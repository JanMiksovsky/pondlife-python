import re

# Regex patterns
rx_lt = re.compile(r'<')
rx_gt = re.compile(r'>')
rx_space = re.compile(r'[\t\r\uf8ff]')
rx_escape = re.compile(r'\\([\\\|`*_{}\[\]()#+\-~])')
rx_hr = re.compile(r'^([*\-=_] *){3,}$', re.MULTILINE)
rx_listjoin = re.compile(r'</(ol|ul)>\n\n<\1>')
rx_highlight = re.compile(r'(^|[^A-Za-z\d\\])(([*_])|(~)|(\^)|(--)|(\+\+)|`)(\2?)([^<]*?)\2\8(?!\2)(?=\W|_|$)', re.DOTALL)
rx_blockquote = re.compile(r'\n *&gt; *(.*?)(?=(\n|$){2})', re.DOTALL)
rx_list = re.compile(r'\n( *)(?:[*\-+]|((\d+)|([a-z])|[A-Z])[.)]) +(.*?)(?=(\n|$){2})', re.DOTALL)
rx_highlight = re.compile(r'(^|[^A-Za-z\d\\])(([*_])|(~)|(\^)|(--)|(\+\+)|`)(\2?)([^<]*?)\2\8(?!\2)(?=\W|_|$)', re.DOTALL)
rx_code = re.compile(r'\n((```|~~~).*\n?(.*?)\n?\2|((    .*?\n)+))', re.DOTALL)
rx_link = re.compile(r'((!?)\[(.*?)\]\((.*?)( ".*")?\)|\\([\\`*_{}\[\]()#+\-.!~]))')
rx_table = re.compile(r'\n(( *\|.*?\| *\n)+)', re.DOTALL)
rx_thead = re.compile(r'^.*\n( *\|( *\:?-+\:?-+\:? *\|)* *\n|)')
rx_row = re.compile(r'.*\n')
rx_cell = re.compile(r'\||(.*?[^\\])\|')
rx_heading = re.compile(r'(?=^|>|\n)([>\s]*?)(#{1,6}) (.*?)( #*)? *(?=\n|$)', re.MULTILINE)
rx_para = re.compile(r'(?=^|>|\n)\s*\n+([^<]+?)\n+\s*(?=\n|<|$)', re.DOTALL)
rx_stash = re.compile(r'-\d+\uf8ff')

def markdownToHtml(src):
	"""
	drawdown.js markdown-to-html processor by Adam Leggett, ported to Python
	"""
	stash = {}
	si = 0

	src = "\n" + src + "\n"

	src = rx_lt.sub("&lt;", src)
	src = rx_gt.sub("&gt;", src)
	src = rx_space.sub("  ", src)

	# blockquote
	src = blockquote(src)

	# horizontal rule
	src = rx_hr.sub("<hr/>", src)

	# list
	src = list_(src)
	src = rx_listjoin.sub("", src)

	# code
	def code_repl(match):
		nonlocal si
		p3 = match.group(3)
		p4 = match.group(4)
		code_content = p3 if p3 is not None else re.sub(r'^    ', '', p4 or '', flags=re.MULTILINE)
		stash[si] = element("pre", element("code", code_content))
		result = f"-{si}\uf8ff"
		si -= 1
		return result
	src = rx_code.sub(code_repl, src)

	# link or image
	def link_repl(match):
		nonlocal si
		p2 = match.group(2)
		p3 = match.group(3)
		p4 = match.group(4)
		p6 = match.group(6)
		if p4:
			if p2:
				html = f'<img src="{p4}" alt="{p3}"/>'
			else:
				html = f'<a href="{p4}">{unesc(highlight(p3))}</a>'
		else:
			html = p6 or ''
		stash[si] = html
		result = f"-{si}\uf8ff"
		si -= 1
		return result
	src = rx_link.sub(link_repl, src)

	# table
	def table_repl(match):
		table = match.group(1)
		sep_match = rx_thead.match(table)
		sep = sep_match.group(1) if sep_match else ''
		def row_repl(row):
			if row == sep:
				return ''
			def cell_repl(cell_match):
				ci = cell_match.lastindex
				cell = cell_match.group(1)
				tag = 'th' if sep and not ci else 'td'
				return element(tag, unesc(highlight(cell or "")))
			return element('tr', rx_cell.sub(cell_repl, row))
		table_html = rx_row.sub(lambda m: row_repl(m.group(0)), table)
		return "\n" + element("table", table_html)
	src = rx_table.sub(table_repl, src)

	# heading
	def heading_repl(match):
		p1 = match.group(2)
		p2 = match.group(3)
		return element(f"h{len(p1)}", unesc(highlight(p2)))
	src = rx_heading.sub(heading_repl, src)

	# paragraph
	def para_repl(match):
		content = match.group(1)
		return element("p", unesc(highlight(content)))
	src = rx_para.sub(para_repl, src)

	# stash
	def stash_repl(match):
		idx = int(match.group(0)[1:-1])
		return stash.get(idx, '')
	src = rx_stash.sub(stash_repl, src)

	return src.strip()

def blockquote(src):
	def repl(match):
		content = match.group(1)
		return element("blockquote", blockquote(highlight(re.sub(r'^ *&gt; *', '', content, flags=re.MULTILINE))))
	return rx_blockquote.sub(repl, src)

def element(tag, content):
	return f'<{tag}>{content}</{tag}>'

def highlight(src):
	def repl(match):
		_ = match.group(1)
		emp = match.group(3)
		sub = match.group(4)
		sup = match.group(5)
		small = match.group(6)
		big = match.group(7)
		code = match.group(8)
		p2 = match.group(9)
		content = match.group(10)
		if emp:
			tag = "strong" if p2 else "em"
		elif sub:
			tag = "s" if p2 else "sub"
		elif sup:
			tag = "sup"
		elif small:
			tag = "small"
		elif big:
			tag = "big"
		else:
			tag = "code"
		return _ + element(tag, highlight(content))
	return rx_highlight.sub(repl, src)

def list_(src):
	def repl(match):
		ind = match.group(1)
		ol = match.group(2)
		num = match.group(3)
		low = match.group(4)
		content = match.group(5)
		split_re = re.compile(r'\n ?' + re.escape(ind) + r'(?:(?:\d+|[a-zA-Z])[.)]|[*\-+]) +')
		items = [list_(item) for item in split_re.split(content)]
		entry = element("li", highlight("</li><li>".join(items)))
		if ol:
			start = num if num else str(int(ol, 36) - 9)
			style = "low" if low else "upp"
			return f'\n<ol start="{start}" style="list-style-type:{style}er-alpha">{entry}</ol>'
		else:
			return '\n' + element("ul", entry)
	return rx_list.sub(repl, src)

def unesc(str_):
	return rx_escape.sub(lambda m: m.group(1), str_)
