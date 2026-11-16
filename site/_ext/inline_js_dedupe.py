"""Stop Sphinx 7.4 from writing extension inline scripts twice on every page.

Extensions that add an inline script after the builder starts (sphinx-thebe's
THEBE_JS_URL config, sphinx-togglebutton's selector) reach the builder as
filename None, and prepare_writing() adds them again as filename ''. The two
copies do not compare equal, so both are written, and the second
`const THEBE_JS_URL` throws a SyntaxError in the browser. jupyter-book 1.x pins
sphinx~=7.0, so the upstream fix is not available here.
"""
from sphinx.builders.html._assets import _JavaScript


def normalize_inline_js(app, env):
    files = getattr(app.builder, '_js_files', None)
    if files is None:
        return
    normalized = []
    for js in files:
        if js.filename is None:
            js = _JavaScript('', priority=js.priority, **js.attributes)
        if js not in normalized:
            normalized.append(js)
    files[:] = normalized


def setup(app):
    app.connect('env-updated', normalize_inline_js)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
