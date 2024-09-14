

import xml.etree.ElementTree as ET

file_path = "config.xml"
def load_config_from_xml(KEY):
    tree = ET.parse(file_path)
    root = tree.getroot()
    VALUE = root.find('settings').find(KEY).text
    return VALUE


