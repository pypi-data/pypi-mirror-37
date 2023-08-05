from .check import check_config_format
from .document import Document


def parse_document_rules(config):
    check_config_format(config)
    if 'kooki' in config:
        return parse_multi_documents(config)
    else:
        return parse_mono_document(config)


def parse_mono_document(config):
    document = Document(config)
    return document


def parse_multi_documents(config):
    documents = {}
    for document_name, document_config in config['kooki'].items():

        if 'default' in config:
            if document_config:
                if 'output' not in config['default'] and 'output' not in document_config:
                    document_config['output'] = document_name
                if 'context' not in config['default'] and 'context' not in document_config:
                    document_config['context'] = document_name
            else:
                document_config = {}
                document_config['output'] = document_name
                document_config['context'] = document_name
            document = Document(config['default'], document_config)

        else:
            if document_config:
                if 'output' not in document_config:
                    document_config['output'] = document_name
                if 'context' not in document_config:
                    document_config['context'] = document_name
            else:
                document_config = {}
                document_config['output'] = document_name
                document_config['context'] = document_name
            document = Document(document_config)

        documents[document_name] = document
    return documents
