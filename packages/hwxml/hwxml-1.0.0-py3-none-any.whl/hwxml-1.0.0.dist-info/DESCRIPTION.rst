# hwxml
Parse Happy Wheels XML Leveldata!

# Usage:
    import hwxml
    xml = open("xml.txt", "r").read()
    parsed = hwxml.xml.xml(xml).parse()

    shapes = parsed.shapes
    print(shapes[0].coordinates)


