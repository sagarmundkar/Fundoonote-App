from django_elasticsearch_dsl import Index, DocType, fields

from .index import note_index, html_strip
from .models import Note
from elasticsearch_dsl.connections import connections

# creating elastic search connection
connections.create_connection(hosts=['localhost'])

# getting connection of elasticsearch
connections.get_connection().cluster.health()

# defining note index
note = Index('note')
@note_index.doc_type
class NoteDocument(DocType):
    """
    Using decorator create the notedocument class
    which describe the fields of note model
    """
    title = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )
    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    color = fields.StringField(
       analyzer=html_strip,
     fields={
         'raw': fields.StringField(analyzer='keyword'),
     }
     )
    reminder = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )

    # defining the meta class
    class Meta(object):
        model = Note
