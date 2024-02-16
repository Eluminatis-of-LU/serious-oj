import base64
import hashlib
import jinja2
import markupsafe
import mistune
import re
from urllib import parse

from vj4.util import options

markdown_parser = mistune.create_markdown(escape=True, hard_wrap=True, renderer='html', plugins=['table', 'url', 'math'])

FS_RE = re.compile(r'\(vijos\:\/\/fs\/([0-9a-f]{40,})\)')

def nl2br(text):
  markup = markupsafe.escape(text)
  return markupsafe.Markup('<br>'.join(markup.split('\n')))


def fs_replace(m):
  # TODO(twd2): reverse_url
  return '(' + options.cdn_prefix.rstrip('/') + '/fs/' + m.group(1) + ')'


def markdown(text):
  text = FS_RE.sub(fs_replace, text)
  return markupsafe.Markup(markdown_parser(text))


def gravatar_url(gravatar, size=200):
  # TODO: 'd' should be https://domain/img/avatar.png
  if gravatar:
    gravatar_hash = hashlib.md5(gravatar.lower().encode()).hexdigest()
  else:
    gravatar_hash = ''
  return ('//cn.gravatar.com/avatar/' + gravatar_hash + "?" +
          parse.urlencode({'d': 'mm', 's': str(size)}))


def paginate(page, num_pages):
  radius = 2
  if page > 1:
    yield 'first', 1
    yield 'previous', page - 1
  if page <= radius:
    first, last = 1, min(1 + radius * 2, num_pages)
  elif page >= num_pages - radius:
    first, last = max(1, num_pages - radius * 2), num_pages
  else:
    first, last = page - radius, page + radius
  if first > 1:
    yield 'ellipsis', 0
  for page0 in range(first, last + 1):
    if page0 != page:
      yield 'page', page0
    else:
      yield 'current', page
  if last < num_pages:
    yield 'ellipsis', 0
  if page < num_pages:
    yield 'next', page + 1
    yield 'last', num_pages


def format_size(size, base=1, ndigits=3):
  size *= base
  unit = 1024
  unit_names = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
  for unit_name in unit_names:
    if size < unit:
      return '{0} {1}'.format(round(size, ndigits=ndigits), unit_name)
    size /= unit
  return '{0} {1}'.format(round(size * unit, ndigits=ndigits), unit_names[-1])


def format_seconds(seconds):
  seconds = int(seconds)
  return '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)


def base64_encode(str):
  encoded = base64.b64encode(str.encode())
  return encoded.decode()


def dedupe(list):
  result = []
  result_set = set()
  for i in list:
    if i in result_set:
      continue
    result.append(i)
    result_set.add(i)
  return result

def format_memory_limit(str):
  memory_limit_kb = int(str)
  memory_limit_mb = round(memory_limit_kb / 1024, 2)
  return '{0} MB'.format(memory_limit_mb)

def format_time_limit(str):
  time_limit_ms = int(str)
  time_limit_s = round(time_limit_ms / 1000, 2)
  return '{0} s'.format(time_limit_s) 
  