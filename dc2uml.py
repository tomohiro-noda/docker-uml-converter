#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
input_filename = sys.argv[1]
output_filename = sys.argv[2]
components_define = 'services'
dependencies_define = 'depends_on'
networks_define = 'networks'
images_define = 'image'
ports_define = 'ports'
aliases_define = 'aliases'


def open_yml(filename):
    import yaml
    with open(filename, 'r') as f:
        data = yaml.load(f)
    return data


def _finditem(obj, key=components_define):
    if key in obj:
        return obj[key]
    for (k, v) in obj.items():
        if isinstance(v, dict):
            return _finditem(v, key)


def remove_restricted_str(target_str, remove_str):
    modified_str = '_'.join(target_str.split(remove_str))
    return modified_str


def make_dependencies_dict(data, services_name, key=components_define):
    dependencies_dict = {}
    for service in services_name:
        tmp = []
        depends = _finditem(data[key][service], dependencies_define)
        if isinstance(depends, list):
            for v in depends:
                if '-' in v:
                    tmp.append(remove_restricted_str(v, '-'))
                else:
                    tmp.append(v)
            dependencies_dict.update({service: tmp})
        else:
            pass
    return dependencies_dict


def make_images_dict(data, services_name, key=components_define):
    images_dict = {}
    for service in services_name:
        tmp = []
        for v in [_finditem(data[key][service], images_define)]:
            if '-' in v:
                tmp.append(remove_restricted_str(v, '-'))
            else:
                tmp.append(v)
        images_dict.update({service: tmp})
    return images_dict


def make_networks_dict(data, services_name, key=components_define):
    networks_dict = {}
    for service in services_name:
        networks = _finditem(data[key][service], networks_define).keys()
        if len(networks) > 1:
            for i in networks:
                if networks_dict.has_key(i):
                    networks_dict[i].append(service)
                else:
                    networks_dict.update({i: [service]})
        else:
            if networks_dict.has_key(networks[0]):
                networks_dict[networks[0]].append(service)
            else:
                networks_dict.update({networks[0]: [service]})
    return networks_dict


def make_components_dict(data, key=components_define):
    components_dict = data[key]
    return components_dict


def combine_dependencies_str(dependencies_dict):
    combined_dependencies_str = ''
    for (k, v) in dependencies_dict.items():
        if v is None:
            pass
        elif isinstance(v, list):
            for i in v:
                combined_dependencies_str = combined_dependencies_str \
                    + '  [' + k + ']' + ' --> ' + '[' + i + ']' + '\n'
        else:
            combined_dependencies_str = combined_dependencies_str \
                + '  [' + k + ']' + ' --> ' + '[' + v + ']' + '\n'
    return combined_dependencies_str


def combine_images_str(images_dict):
    combined_images_str = ''
    prefix = 'cloud ' + 'Docker_hub' + ' {\n'
    sufix = '}\n'
    for (k, v) in images_dict.items():
        if v is None:
            pass
        elif isinstance(v, list):
            for i in v:
                combined_images_str = combined_images_str + '  [' + k \
                    + ']' + ' --> ' + '[' + i + ']' + '\n'
        else:
            combined_images_str = combined_images_str + '  [' + k + ']' \
                + ' --> ' + '[' + v + ']' + '\n'
    combined_images_str = prefix + combined_images_str + sufix
    return combined_images_str


def make_components_str_dict(components_dict):
    components_str_dict = {}
    prefix = 'component '
    sufix = ']'
    for (k, v) in components_dict.items():
        tmp = prefix + k + ' [' + k + '''
---
'''
        tmp = _add_ports(tmp, v)
        tmp = _add_aliases(tmp, v)
        tmp = tmp + sufix
        components_str_dict.update({k: tmp})
    return components_str_dict


def _add_ports(target_str, content_dict):
    ports = _finditem(content_dict, ports_define)
    poarts_str = ''
    for i in ports:
        poarts_str = poarts_str + str(i) + ','
    added_str = target_str + ports_define + ':' + poarts_str + '\n'
    return added_str


def _add_aliases(target_str, content_dict):
    aliases = _finditem(content_dict[networks_define], aliases_define)
    aliases_str = ''
    for i in aliases:
        aliases_str = aliases_str + str(i) + ','
    added_str = target_str + aliases_define + ':' + aliases_str + '\n'
    return added_str


def make_networks_str(components_str_dict, networks_dict):
    networks_str_dict = {}
    networks_str = ''
    for (k, v) in networks_dict.items():
        if isinstance(v, list):
            for i in v:
                networks_str = networks_str + '  ' \
                    + components_str_dict[i] + '\n'
        else:
            networks_str = networks_str + '  ' + components_str_dict[v] \
                + '\n'
        prefix = 'package ' + k + ' {\n'
        sufix = '}\n'
        networks_str_dict.update({k: prefix + networks_str + sufix})
    return networks_str_dict


def combine_networks(networks_str_dict):
    combine_networks_str = ''
    for (k, v) in networks_str_dict.items():
        combined_networks_str = combine_networks_str + v
    return combined_networks_str


def combine_net_and_dep(combined_networks_str,
                        combined_dependencies_str, combined_images_str):
    return combined_networks_str + '\n' + combined_dependencies_str \
        + '\n' + combined_images_str


def combine_puml(combined_net_and_dep_str):
    prefix = '```puml\n'
    sufix = '```'
    combined_puml_str = prefix + combined_net_and_dep_str + sufix
    return combined_puml_str


def save_md(str):
    with open(output_filename, 'w') as f:
        f.write(str)


def main():
    data = open_yml(input_filename)
    components_name = _finditem(data).keys()
    components_name_mod = []
    for i in components_name:
        if '-' in i:
            modified_str = remove_restricted_str(i, '-')
            data[components_define][modified_str] = \
                data[components_define].pop(i)
            components_name_mod.append(modified_str)
        else:
            components_name_mod.append(i)
    dependencies_dict = make_dependencies_dict(data,
            components_name_mod)
    images_dict = make_images_dict(data, components_name_mod)
    networks_dict = make_networks_dict(data, components_name_mod)
    components_dict = make_components_dict(data)
    combined_dependencies_str = \
        combine_dependencies_str(dependencies_dict)
    combined_images_str = combine_images_str(images_dict)
    components_str_dict = make_components_str_dict(components_dict)
    networks_str_dict = make_networks_str(components_str_dict,
            networks_dict)
    combined_networks_str = combine_networks(networks_str_dict)
    combined_net_and_dep_str = \
        combine_net_and_dep(combined_networks_str,
                            combined_dependencies_str,
                            combined_images_str)
    combined_puml_str = combine_puml(combined_net_and_dep_str)
    save_md(combined_puml_str)


if __name__ == '__main__':
    main()
