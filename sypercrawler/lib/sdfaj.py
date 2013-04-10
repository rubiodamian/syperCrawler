'''asignacion!'''
import re
string = 'asdasdasd =eval __pjsapd__oa= eval func(arg1, arg2, arg3+arg4,"asd", asd[asd])'
#regex = re.compile("(?P<key>\w*?)\s*=\s*(?P<value>eval?)")
regex = re.compile("(?P<function>\w+)\s?\((?P<args>(.*(,\s?|[\+])?))\)")
r = regex.search(string)
r
print regex.match(string)

print r.groups()
#(u'asdad', u'eval')

# List the named dictionary objects found
print r.groupdict()
#{u'key': u'asdad', u'value': u'eval'}

# Run findall
print regex.findall(string)
#[(u'asdad', u'eval')]
