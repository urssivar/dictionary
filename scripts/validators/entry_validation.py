#!/usr/bin/env python3


def validate_entry(yaml_data):
    return 'id' in yaml_data and 'headword' in yaml_data and 'definitions' in yaml_data
