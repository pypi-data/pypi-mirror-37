import pretty_output, os, yaml

from collections import OrderedDict
from packaging import version

from kooki.tools import read_file

from .jars import search_file, search_jar, jar_dependencies
from .exception import MissingTemplate, MissingMetadata, MissingJar
from .exception import MissingContent, KookiException, KookiOutdated
from .metadata import Metadata, parse_metadata
from .common import apply_template, export_to
from .extension import Extension, Caller
from ..version import __version__

output = []


def output_search_start():
    global output
    output = []


def output_search(path, fullpath):
    if fullpath:
        output.append({'name': path, 'status': '[found]', 'path': fullpath})
    else:
        output.append({'name': path, 'status': ('[missing]', 'red'), 'path': ''})


def output_search_finish():
    pretty_output.infos(output, [('name', 'blue'), ('status', 'green'), ('path', 'cyan')])


def process_document(document, step=lambda *args, **kwargs: None):
    # jars
    step('jars')
    load_jars(document)

    # version
    check_kooki_version(document.version)

    # template
    step('template')
    template_path, template_extension = load_template(document)
    document.extension = template_extension
    template = Extension(document, template_path)

    # metadata
    step('metadata')
    load_metadata(document)

    # process
    step('processor')
    document_content = template()
    output = apply_template(document.output, document.metadata)
    output_path = os.path.join(document.context, output.replace('\n', ''))
    Caller.clean()

    # output
    step('output')
    absolute_file_path = export_to(output_path, template_extension, document_content)
    pretty_output._print_colored('export to ', 'blue', '')
    pretty_output._print_colored(absolute_file_path, 'cyan')

    # toppings
    step('toppings')
    import subprocess
    os.environ['KOOKI_CONTEXT'] = document.context
    os.environ['KOOKI_EXPORT_FILE'] = absolute_file_path
    for topping in document.toppings:
        pretty_output._print_colored('execute ', 'blue', '')
        pretty_output._print_colored(topping, 'cyan')
        subprocess.call(topping, shell=True)
        pretty_output._print_colored('finish ', 'blue', '')
        pretty_output._print_colored(topping, 'cyan')


def check_kooki_version(kooki_version_needed):
    if version.parse(__version__) < version.parse(kooki_version_needed):
        raise KookiOutdated(__version__, kooki_version_needed)


def load_template(document):
    output_search_start()
    file_full_path = search_file(document, document.template)
    output_search(document.template, file_full_path)
    if file_full_path:
        file_read = read_file(file_full_path)
        document.template = file_read
        output_search_finish()
    else:
        output_search_finish()
        raise MissingTemplate(document.jars, document.template)

    _, template_extension = os.path.splitext(file_full_path)
    return file_full_path, template_extension


def print_extension(extensions, prefix=''):
    extensions_name = list(extensions.keys())
    extensions_name.sort()
    if prefix != '':
        prefix += '.'
    for extension_name in extensions_name:
        extension = extensions[extension_name]
        if isinstance(extension, dict):
            print_extension(extension, extension_name)
        else:
            output_search('{}{}'.format(prefix, extension_name), extension.path)


def load_jars(document):
    full_path_jars = []
    output_search_start()
    for jar in document.jars:
        load_jar_dependencie(full_path_jars, jar)
        jar_full_path = search_jar(jar)
        if jar_full_path:
            output_search(jar, jar_full_path)
            full_path_jars.append(jar_full_path)
        else:
            output_search_finish()
            raise MissingJar(jar)
    document.jars = full_path_jars
    output_search_finish()


def load_jar_dependencie(full_path_jars, jar):
    dependencies = jar_dependencies(jar)
    for dependencie in dependencies:
        load_jar_dependencie(full_path_jars, dependencie)
        jar_full_path = search_jar(dependencie)
        if jar_full_path:
            output_search(dependencie, jar_full_path)
            full_path_jars.append(jar_full_path)
        else:
            output_search_finish()
            raise MissingJar(jar)


def load_metadata(document):
    metadata_full_path = {}
    output_search_start()
    for metadata in document.metadata:
        file_full_path = search_file(document, metadata)
        output_search(metadata, file_full_path)
        if file_full_path:
            file_read = read_file(file_full_path)
            metadata_full_path[file_full_path] = file_read
        else:
            output_search_finish()
            raise MissingMetadata(document.jars, metadata)
    document.metadata = metadata_full_path
    output_search_finish()
    document.metadata = parse_metadata(document.metadata)

    pretty_output.debug_on()
    pretty_output.colored(yaml.dump(document.metadata, default_flow_style=False), 'white', 'on_yellow')
    pretty_output.debug_off()


def print_metadata(metadata, prefix=''):
    matadata_keys = list(metadata.keys())
    matadata_keys.sort()
    if prefix != '':
        prefix += '.'
    for matadata_key in matadata_keys:
        element = metadata[matadata_key]
        if isinstance(element, dict):
            print_metadata(element, matadata_key)
        else:
            output_search('{}{}'.format(prefix, matadata_key), '')
