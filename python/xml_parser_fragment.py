#! /usr/bin/env python2
# coding: UTF-8

import os
import glob
import re
import xml.etree.cElementTree as ET
import logging

xn = "genericNrm.xsd"
es = "TongSpecificAttributes.16.08.xsd"
 

def convert_oss_files(xml_path, csv_file_path):
    csv_path = os.path.abspath(csv_file_path)
    node_list = parse_xml_files(xml_path)


def parse_xml_files(xml_path):
    node_list = []
    xml_path = os.path.abspath(xml_path)
    if os.path.isdir(xml_path):
        xml_files = glob.glob(xml_path + "/*.xml")
        for xml in xml_files:
            node_list.extend(xml_to_node_list(xml))
    else:
        fileName, fileExtension = os.path.splitext(xml_path)
        if fileExtension == ".xml":
            node_list.extend(xml_to_node_list(xml_path))

    logging.info("Total get %s node for %s" % (len(node_list), xml_path))
    return node_list


def xml_to_node_list(xml_file):
    node_list = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # get ES namespace value
        for elem in root.getiterator():
            match=re.search("\{TongSpecificAttributes\W", elem.tag)
            if match:
                es_str = elem.tag
                global es
                es = es_str[1 :es_str.index("}")]
                break

        market = ""
        enb_elements = root.findall('.//{%s}MeContext' % xn)
        for elem in enb_elements:
            node_name = elem.attrib['id']
            if node_name == "":
                logging.error("Ignore one configData, because MeContext element id is empty")
                continue
            node_obj = parser_node(elem, node_name, market)

            try:
                node_obj.validate_params()
            except Exception, e:
                logging.error("Ignore node:%s, because %s" % (node_name, e))
                continue

            print_node_obj(node_obj)
            node_list.append(node_obj)
    except Exception, e:
        logging.error("Fail to parse xml file %s, because: %s" % (xml_file, e))
    return node_list


def parser_node(node_element, node_name, market):
    ....
    return node_obj


def get_filter_value(ori_str, filter, symbol):
    if ori_str == "":
        return ""
    start_index = ori_str.index(filter + symbol)
    if start_index != -1:
        offset = len(filter) + len(symbol)
        result = ori_str[start_index + offset:len(ori_str)]
        return result
    else:
        return ""



def get_element_list_by_datatype(node_root, vs_datatype):
    # return VsDataContainer node
    #return node_root.findall(".//*[{%s}vsDataType='%s']/.." % (xn, vs_datatype)) #python 2.7 can use this code directly
    element_list = []
    data_container_list = node_root.findall(".//{%s}VsDataContainer" % xn)
    for data_container in data_container_list:
        data_type = data_container.find("./{%s}attributes/{%s}vsDataType" %(xn,xn))
        if data_type.text == vs_datatype:
            element_list.append(data_container)
    return element_list


def get_es_element(es_element, element_name):
    if es_element is None:
        return None
    return es_element.find('.//{%s}%s' % (es, element_name))


def get_es_elements(es_element, element_name):
    if es_element is None:
        return None
    return es_element.findall('.//{%s}%s' % (es, element_name))


def get_es_element_value(es_element, element_name):
    if es_element is None:
        return ""
    elem = es_element.find('.//{%s}%s' % (es, element_name))
    if elem is not None:
        return elem.text if elem.text is not None else ""
    else:
        return ""



import time

if __name__ == '__main__':
    cur = time.time()
    LOG_FILENAME = 'example.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

    #parse_xml_files("/dev/bmc/bmc-backend/cdi2/cdi2/VERIZON_BULK_EXPORT1.xml")
    convert_oss_files("/dev/bmc/bmc-backend/cdi2/cdi2/Report_20160222_141107.xml","/dev/bmc/bmc-backend/cdi2/cdi2/bulk.csv")
    cost = time.time() - cur
    print 'cost:', cost
