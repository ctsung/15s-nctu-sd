from xml.parsers.xmlproc import xmlproc

def test(file):
    app = xmlproc.Application()
    p = xmlproc.XMLProcessor()

    try:
        p.parse_resource(file)
        return "PASS"
    except UnboundLocalError:
        return "FAIL"
    except:
        return "UNRESOLVED"
