from __future__ import unicode_literals

import regex as re

prefixes = '''
,
"
(
[
{
*
<
$
£
“
'
``
`
#
#US$
C$
A$
a-
‘
....
...
'''

suffixes = '''
,
\"
\)
\]
\}
\*
\!
\?
%
\$
>
:
;
'
”
''
's
'S
’s
’S
’
\.\.
\.\.\.
\.\.\.\.
(?<=[a-z0-9)\]"'%\)])\.
(?<=[0-9])km
'''

infixes = '''
\.\.\.+
(?<=[a-z])\.(?=[A-Z])
(?<=[a-zA-Z])-(?=[a-zA-z])
(?<=[a-zA-Z])--(?=[a-zA-z])
(?<=[0-9])-(?=[0-9])
(?<=[A-Za-z]),(?=[A-Za-z])
'''


def get_prefix_regex():
    entries = prefixes.strip().split('\n')
    expression = '|'.join(['^' + re.escape(piece) for piece in entries if piece.strip()])
    return re.compile(expression)


def get_suffix_regex():
    entries = suffixes.strip().split('\n')
    expression = '|'.join([piece + '$' for piece in entries if piece.strip()])
    return re.compile(expression)


def get_infix_regex():
    entries = infixes.strip().split('\n')
    expression = '|'.join([piece for piece in entries if piece.strip()])
    return re.compile(expression)
