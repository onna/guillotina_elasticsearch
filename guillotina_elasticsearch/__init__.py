# -*- coding: utf-8 -*-
from guillotina import configure


app_settings = {
    "elasticsearch": {
        "bulk_size": 50,
        "index_name_prefix": "plone-",
        "connection_settings": {
            "endpoints": [],
            "sniffer_timeout": 0.5
        },
        "index": {},
        "mapping_overrides": {
            "*": {}
        }
    }
}


def includeme(root):
    configure.scan('guillotina_elasticsearch.api')
    configure.scan('guillotina_elasticsearch.utility')
