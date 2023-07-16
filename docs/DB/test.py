from yattag import Doc

doc, tag, text = Doc().tagtext()

with tag('html'):
    with tag('head'):
        with tag('title'):
            text('My HTML Document')
    with tag('body'):
        with tag('h1'):
            text('Hello, world!')
        with tag('p'):
            text('This is a simple HTML document generated using Python and yattag.')
        with tag('input'):
            text('enter your number')

html_document = doc.getvalue()

with open('output.html', 'w') as f:
    f.write(html_document)