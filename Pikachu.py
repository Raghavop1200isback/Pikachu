#!/usr/bin/env python3
import argparse
import re
import sys
from urllib.parse import urlparse

try:
    from signal import signal, SIGPIPE, SIG_DFL
    signal(SIGPIPE, SIG_DFL)
except ImportError:
    pass

def clean_nargs(args):
    """Cleans nargs to prevent user errors"""
    if not args:
        return []
    new_args = []
    if len(args) == 1:
        if "," in args[0]:
            new_args = [arg.lower() for arg in args[0].strip().split(',')]
        elif " " in args[0]:
            new_args = [arg.lower() for arg in args[0].split(' ')]
        else:
            new_args.append(args[0].lower())
    else:
        for arg in args:
            cleaner = clean_nargs([arg])
            if cleaner:
                new_args.extend(cleaner)
            else:
                new_args.append(arg)
    return list(set(filter(None, new_args)))

def params_to_dict(params):
    """Converts query string to dict"""
    the_dict = {}
    if params:
        for pair in params.split('&'):
            parts = pair.split('=')
            try:
                the_dict[parts[0]] = parts[1]
            except IndexError:
                pass
    return the_dict

def dict_to_params(params):
    """Converts dict of params to query string"""
    stringed = [name + '=' + value for name, value in params.items()]
    return '?' + '&'.join(stringed)

def compare_params(og_params, new_params):
    """Checks if new_params contain a param that doesn't exist in og_params"""
    og_set = set([])
    for each in og_params:
        for key in each.keys():
            og_set.add(key)
    return set(new_params.keys()) - og_set

def has_ext(path, params, meta):
    """Returns True if url has an extension"""
    if '.' not in path.split('/')[-1]:
        return False, False
    return True, path.lower().endswith(tuple(meta['ext_list']))

def no_ext(path, params, meta):
    """Returns True if url has no extension"""
    has_ext, _ = check_ext(path, [])
    return not has_ext

def has_params(path, params, meta):
    """Returns True if url has parameters"""
    return len(params) > 0

def no_params(path, params, meta):
    """Returns True if url has no parameters"""
    return len(params) == 0

def whitelisted(path, params, meta):
    """Returns True if url has no extension or has a whitelisted extension"""
    has_ext, is_ext = check_ext(path, meta['ext_list'])
    return is_ext or (not meta['strict'] and not has_ext)

def blacklisted(path, params, meta):
    """Returns True if url has no extension or doesn't have a blacklisted extension"""
    has_ext, is_ext = check_ext(path, meta['ext_list'])
    return not is_ext or (not meta['strict'] and not has_ext)

def remove_content(path, params, meta):
    """Checks if a path is likely to contain human written content e.g. a blog
    Returns False if it is
    """
    for part in path.split('/'):
        if part.count('-') > 3:
            return False
    return False if re_content.search(path) else True

def has_vuln_param(path, params, meta):
    """Checks if a url has a vulnerable parameter"""
    for param in params:
        if param in meta['vuln_params']:
            return True

def check_ext(path, ext_list):
    """Checks if a URL path has an extension from the given list"""
    if '.' not in path.split('/')[-1]:
        return False, False
    return True, path.lower().endswith(tuple(ext_list))

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='file containing urls', dest='input_file')
parser.add_argument('-o', help='output file', dest='output_file')
parser.add_argument('-w', '--whitelist', help='only keep these extensions and extensionless urls', dest='whitelist', nargs='+')
parser.add_argument('-b', '--blacklist', help='remove these extensions', dest='blacklist', nargs='+')
parser.add_argument('-f', '--filters', help='additional filters, read docs', dest='filters', nargs='+')
args = parser.parse_args()

filters = clean_nargs(args.filters)
active_filters = ['removecontent']

if not args.whitelist or "allexts" in filters:
    active_filters.append('blacklist')
if args.whitelist:
    active_filters.append('whitelist')

active_filters.extend(filters)

if 'keepcontent' in active_filters:
    active_filters.remove('removecontent')
active_filters.remove('keepcontent')

urlmap = {}
params_seen = []
patterns_seen = []

re_content = re.compile(r'(post|blog)s?|docs|support/|/(\d{4}|pages?)/\d+/')
re_int = re.compile(r'/\d+([?/]|$)')

ext_list = clean_nargs(args.blacklist) if args.blacklist else ('css', 'png', 'jpg', 'jpeg', 'svg',
                                                               'ico', 'webp', 'scss', 'tif', 'tiff', 'ttf', 'otf',
                                                               'woff', 'woff2', 'gif', 'pdf', 'bmp', 'eot', 'mp3',
                                                               'mp4', 'avi')

vuln_params = ('file', 'document', 'folder', 'root', 'path', 'pg', 'style', 'pdf', 'template', 'php_path', 'doc',
               'page', 'name', 'cat', 'dir', 'action', 'board', 'date', 'detail', 'download', 'prefix', 'include',
               'inc', 'locate', 'show', 'site', 'type', 'view', 'content', 'layout', 'mod', 'conf', 'daemon',
               'upload', 'log', 'ip', 'cli', 'cmd', 'exec', 'command', 'execute', 'ping', 'query', 'jump', 'code',
               'reg', 'do', 'func', 'arg', 'option', 'load', 'process', 'step', 'read', 'function', 'req', 'feature',
               'exe', 'module', 'payload', 'run', 'print', 'callback', 'checkout', 'checkout_url', 'continue', 'data',
               'dest', 'destination', 'domain', 'feed', 'file_name', 'file_url', 'folder_url', 'forward', 'from_url',
               'go', 'goto', 'host', 'html', 'image_url', 'img_url', 'load_file', 'load_url', 'login_url', 'logout',
               'navigation', 'next', 'next_page', 'Open', 'out', 'page_url', 'port', 'redir', 'redirect',
               'redirect_to', 'redirect_uri', 'redirect_url', 'reference', 'return', 'return_path', 'return_to',
               'returnTo', 'return_url', 'rt', 'rurl', 'target', 'to', 'uri', 'url', 'val', 'validate', 'window', 'q', 's', 'search', 'lang', 'keyword', 'keywords', 'year', 'email', 'p', 'jsonp',
'api_key', 'api', 'password', 'emailto', 'token', 'username', 'csrf_token', 'unsubscribe_token', 'id', 'item', 'page_id',
'month', 'immagine', 'list_type', 'terms', 'categoryid', 'key', 'l', 'begindate', 'enddate', 'select', 'report', 'role',
'update', 'user', 'sort', 'where', 'params', 'row', 'table', 'from', 'sel', 'results', 'sleep', 'fetch', 'order', 'column',
'field', 'delete', 'string', 'number', 'filter', 'access', 'admin', 'dbg', 'debug', 'edit', 'grant', 'test', 'alter', 'clone',
'create', 'disable', 'enable', 'make', 'modify', 'rename', 'reset', 'shell', 'toggle', 'adm', 'cfg', 'open', 'img', 'filename',
'preview', 'activity')

if args.whitelist:
    ext_list = clean_nargs(args.whitelist)

def create_pattern(path):
    """Creates patterns for urls with integers in them"""
    new_parts = []
    for part in re.escape(path).split('/'):
        if part.isdigit():
            new_parts.append('\\d+')
        else:
            new_parts.append(part)
    return '/'.join(new_parts)

def pattern_exists(pattern):
    """Checks if an int pattern exists"""
    for i, seen_pattern in enumerate(patterns_seen):
        if pattern in seen_pattern:
            patterns_seen[i] = pattern
            return True
        elif seen_pattern in pattern:
            return True
    return False

def matches_patterns(path):
    """Checks if the url matches any of the int patterns"""
    for pattern in patterns_seen:
        if re.search(pattern, path):
            return True
    return False

def is_new_param(params):
    """Checks if there's an unseen param within given params"""
    for param in params:
        if param in params_seen:
            return False
    return True

def apply_filters(path, params):
    """Apply filters to a url
    Returns True if the url should be kept
    """
    filter_map = {
        'hasext': has_ext,
        'noext': no_ext,
        'hasparams': has_params,
        'noparams': no_params,
        'removecontent': remove_content,
        'blacklist': blacklisted,
        'whitelist': whitelisted,
        'vuln': has_vuln_param,
    }
    results = []
    meta = {
        'strict': True if ('hasext' or 'noext') in filters else False,
        'ext_list': ext_list,
        'vuln_params': vuln_params,
    }
    for filter in active_filters:
        if filter in filter_map:
            if not filter_map[filter](path, params, meta):
                return False
    return True

def process_url(url):
    """Processes a url"""
    host = url.scheme + '://' + url.netloc
    if host not in urlmap:
        urlmap[host] = {}
    path, params = url.path, params_to_dict(url.query)
    has_new_param = False if not params else is_new_param(params.keys())
    new_params = [param for param in params.keys() if param not in params_seen]
    params_seen.extend(new_params)
    if (not params or has_new_param) and re_int.search(path):
        pattern = create_pattern(path)
        if not pattern_exists(pattern):
            patterns_seen.append(pattern)
    elif matches_patterns(path):
        return
    keep_url = apply_filters(path, params)
    if keep_url:
        if path not in urlmap[host]:
            urlmap[host][path] = [params] if params else []
        elif has_new_param or compare_params(urlmap[host][path], params):
            urlmap[host][path].append(params)

def main():
    input_stream = open(args.input_file, 'r') if args.input_file else None
    if not input_stream:
        if not sys.stdin.isatty():
            input_stream = sys.stdin
    if not input_stream:
        print('[ERROR] No input file or stdin.', file=sys.stderr)
        exit(1)
    for line in input_stream:
        cleanline = line.strip() if 'keepslash' in filters else line.strip().rstrip('/')
        parsed_url = urlparse(cleanline)
        if parsed_url.netloc:
            process_url(parsed_url)
    og_stdout = sys.stdout
    sys.stdout = open(args.output_file, 'a+') if args.output_file else sys.stdout
    for host, value in urlmap.items():
        for path, params in value.items():
            if params:
                for param in params:
                    print(host + path + dict_to_params(param))
            else:
                print(host + path)

if __name__ == "__main__":
    main()
