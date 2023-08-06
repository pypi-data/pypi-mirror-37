from flask import Blueprint

blueprint = Blueprint('preview', __name__)


@blueprint.route('/')
def home():
    import io
    import os
    from flask import current_app, render_template, render_template_string, request, Markup
    from .title import extract_title
    from .images import fix_images

    config = current_app.config

    try:
        with io.open(config['filename'], 'r', encoding='utf-8') as mkdfile:
            markdown = mkdfile.read()
    except UnicodeDecodeError:
        with io.open(config['filename'], 'r', encoding='cp1252') as mkdfile:
            markdown = mkdfile.read()

    title = extract_title(markdown)
    markdown = fix_images(markdown, 'images/')

    style = request.args.get('style')
    if style is None:
        style = 'default'

    talk_no_suffix, _suffix = os.path.splitext(config['filename'])
    own_css_file = talk_no_suffix + '.css'
    own_css = ''  # by default no own css
    if os.path.isfile(own_css_file):
        with io.open(own_css_file, 'r') as css_file:
            own_css = css_file.read()
    own_css = Markup(own_css)  # disable autoescaping
    # use own javascript, if available
    own_js_file = talk_no_suffix + '.js'
    own_javascript = ''
    if os.path.isfile(own_js_file):
        with io.open(own_js_file, 'r') as js_file:
            own_javascript = js_file.read()
    # use custom configuration for the rendering engine, if available
    own_conf_file = talk_no_suffix + '.conf'
    own_conf = ''
    if os.path.isfile(own_conf_file):
        with io.open(own_conf_file, 'r') as conf_file:
            for line in conf_file.readlines():
                own_conf += line.replace('\n', ',\n')
            own_conf = own_conf.rstrip('\n')

    return render_template('render.html',
                           title=title,
                           markdown=markdown,
                           style=style,
                           own_css=own_css,
                           own_javascript=own_javascript,
                           own_conf=own_conf,
                           engine=config['engine'])


@blueprint.route('/images/<path:path>')
def serve_image(path):
    from flask import send_from_directory, current_app
    config = current_app.config
    return send_from_directory(config['imagedir'], path)


@blueprint.errorhandler(404)
def page_not_found(e):
    from flask import render_template
    return render_template('404.html'), 404
