import sys
from xml.parsers.xmlproc import xmlproc

executed_func = set()

def trace(frame, event, arg):
    global executed_func
    if event == 'call':
        try:
            if (frame.f_lineno, frame.f_code.co_name) not in executed_func:
                executed_func.add((frame.f_lineno, frame.f_code.co_name))
        except:
            pass
    return trace

if __name__ == '__main__':
    sys.settrace(trace)
    app = xmlproc.Application()
    p = xmlproc.XMLProcessor()
    try:
        p.parse_resource(sys.argv[1])
    except:
        pass

    file = open(sys.argv[2] + '.cov', 'w')
    for item in sorted(executed_func):
        file.write(', '.join(str(i) for i in item))
        file.write('\n')
    file.close()
