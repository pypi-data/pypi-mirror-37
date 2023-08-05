# encoding: utf-8

import StringIO
import os
import uuid
import datetime

from lxml import etree as etree_


def document_export_xml(document, validate_schema=True):
    """

    :param document: <DocumentoCedible>
    :param validate_schema: Validate schema?
    :return:
    """

    document.Documento.ID = 'DOC_{}'.format(str(uuid.uuid4()))
    document.Documento.TmstFirma = datetime.datetime.now()

    string_buffer = StringIO.StringIO()
    document.export(string_buffer, 0, pretty_print=True)

    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../schemas/DocumentoCedible_v10.xsd')
    schema_file = open(schema_path, 'r')
    schema_root = etree_.parse(schema_file)
    schema = etree_.XMLSchema(schema_root)

    xml_str = string_buffer.getvalue()
    xml_to_validate = xml_str.replace('<SiiDte:DocumentoCedible>',
                                      '<SiiDte:DocumentoCedible version="1.0" xmlns:SiiDte="http://www.sii.cl/SiiDte">')

    if validate_schema:
        try:
            doc = etree_.parse(StringIO.StringIO(xml_to_validate))
            schema.assertValid(doc)
        except etree_.DocumentInvalid as ex:
            no_throw = len(ex.args) == 1 and 'Signature' in ex.args[0]
            if not no_throw:
                raise Exception(str(ex))

    return xml_to_validate.replace('SiiDte:', '')

