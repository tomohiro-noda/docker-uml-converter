#!/usr/bin/python
# -*- coding: utf-8 -*-


def finditem(obj, key):
    if key in obj:
        return obj[key]
    for (k, v) in obj.items():
        if isinstance(v, dict):
            return finditem(v, key)



# input_yml
def open_yml(filename):
    import yaml
    with open(filename, 'r') as f:
        dict = yaml.load(f)
    return dict




# pre-process_yml
def remove_restricted_str(data_dict, before, after):
    data_str=str(data_dict)
    if before in data_str:
        modified_str = after.join(data_str.split(before))
        modified_dict=eval(modified_str)
    return modified_dict


# service:depends_on
def extract_service_depends_on(data_dict):
    ret = {}
    for (k,v) in data_dict.items():
        tmp = []
        items = finditem(v, 'depends_on')
        if isinstance(items, list):
            for i in items:
                tmp.append(i)
            ret.update({k: tmp})
        else:
            pass
    return ret


def convert_service_depends_on_to_uml(data_dict):
    ret = ''
    for (k, v) in data_dict.items():
        if v is None:
            pass
        elif isinstance(v, list):
            for i in v:
                ret = ret \
                    + '[' + k + ']' + ' --> ' + '[' + i + ']' + '\n'
        else:
            ret = ret \
                + '[' + k + ']' + ' --> ' + '[' + v + ']' + '\n'
    return ret



# service:image
def extract_service_image(data_dict):
    ret = {}
    for (k,v) in data_dict.items():
        tmp = []
        for i in [finditem(v, 'image')]:
            tmp.append(i)
        ret.update({k: tmp})
    return ret


def convert_service_image_to_uml(data_dict):
    ret = ''
    prefix = 'cloud ' + 'Repository' + ' {\n'
    sufix = '}\n'
    for (k, v) in data_dict.items():
        if v is None:
            pass
        elif isinstance(v, list):
            for i in v:
                ret = ret + '  [' + k \
                    + ']' + ' --> ' + '[' + i + ']' + '\n'
        else:
            ret = ret + '  [' + k + ']' \
                + ' --> ' + '[' + v + ']' + '\n'
    ret = prefix + ret + sufix
    return ret


# service:networks
def extract_service_networks(data_dict):
    ret = {}
    for (k,v) in data_dict.items():
        networks = finditem(data_dict, 'networks').keys()
        if len(networks) > 1:
            for i in networks:
                if ret.has_key(i):
                    ret[i].append(k)
                else:
                    ret.update({i: [k]})
        else:
            if ret.has_key(networks[0]):
                ret[networks[0]].append(k)
            else:
                ret.update({networks[0]: [k]})
    return ret



def convert_service_networks_to_uml(data_dict):
    return data_dict


# service:services
def extract_service_services(data_dict):
    return data_dict


def convert_service_services_to_uml(data_dict):
    ret = {}
    prefix = 'component '
    sufix = '  ]'
    for (k, v) in data_dict.items():
        tmp = prefix + k + ' [' + k + '''
  ---
'''
        tmp = add_ports(tmp, v)
        tmp = add_aliases(tmp, v)
        tmp = tmp + sufix
        ret.update({k: tmp})
    return ret


def add_ports(uml, data_dict):
    ports_define = 'ports'
    ports = finditem(data_dict, ports_define)
    poarts_str = ''
    for i in ports:
        poarts_str = poarts_str + str(i) + ','
    added_str = uml + '  ' + ports_define + ':' + poarts_str + '\n'
    return added_str


def add_aliases(uml, data_dict):
    aliases_define='aliases'
    aliases = finditem(data_dict['networks'], aliases_define)# must modify
    aliases_str = ''
    for i in aliases:
        aliases_str = aliases_str + str(i) + ','
    added_str = uml + '  ' + aliases_define + ':' + aliases_str + '\n'
    return added_str


# combine_uml
def combine_network_component_uml(networks_dict,services_dict):
    ret = {}
    networks_str = ''
    for (k, v) in networks_dict.items():
        if isinstance(v, list):
            for i in v:
                networks_str = networks_str + '  ' \
                    + services_dict[i] + '\n'
        else:
            networks_str = networks_str + '  ' + services_dict[v] \
                + '\n'
        prefix = 'package ' + k + ' {\n'
        sufix = '}\n'
        ret.update({k: prefix + networks_str + sufix})
    return ret


def combine_networks_uml(networks_uml_dict):
    ret = ''
    for (k, v) in networks_uml_dict.items():
        ret = ret + v
    return ret


def combine_uml(networks_uml,
                        depends_on_uml, image_uml):
    return networks_uml + '\n' + depends_on_uml \
        + '\n' + image_uml



def combine_puml_with_atom_md(raw_uml):
    prefix = '```puml\n'
    sufix = '```'
    return prefix + raw_uml + sufix


# output_uml
def save_md(uml,output_filename):
    with open(output_filename, 'w') as f:
        f.write(uml)


def main():
    import sys
    #----
    # input
    #----
    data_dict = open_yml(sys.argv[1])
    #----
    # pre-process
    #----
    data_dict_preprocessed=remove_restricted_str(data_dict,"-","_")
    #data_dict_preprocessed=data_dict
    #----
    # process depends_on
    #----
    print(data_dict_preprocessed)
    depends_on_data_dict = extract_service_depends_on(data_dict_preprocessed['services'])
    depends_on_uml=convert_service_depends_on_to_uml(depends_on_data_dict)
    #----
    # process image
    #----
    image_data_dict = extract_service_image(data_dict_preprocessed['services'])
    image_uml=convert_service_image_to_uml(image_data_dict)
    #----
    # process networks
    #----
    networks_data_dict = extract_service_networks(data_dict_preprocessed['services'])
    #networks_uml=convert_service_networks_to_uml(networks_data_dict)
    #----
    # process services
    #----
    #services_data_dict = extract_service_services(data_dict_preprocessed['services'])
    services_uml=convert_service_services_to_uml(data_dict_preprocessed['services'])
    #----
    # comEbine_uml
    #----
    networks_uml_dict=combine_network_component_uml(networks_data_dict,services_uml)
    networks_uml=combine_networks_uml(networks_uml_dict)
    raw_uml=combine_uml(networks_uml,depends_on_uml,image_uml)
    uml=combine_puml_with_atom_md(raw_uml)
    #----
    # output_uml
    #----
    save_md(uml,sys.argv[2])


if __name__ == '__main__':
    main()
