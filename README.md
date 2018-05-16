# docker-uml-converter
Convert docker-compose.yml to plantuml with atom:markdown-preview-enhanced using python

## Purpose
- Simplicity
  - Easy to develop
- Frexibility
  - Function based microservices
    - Porting to serverless systems


## Supported service settings
Must define service settings below in docker-compose.yml
- Correspondence table

| Docker-compose v3 | Plantuml component diagram      |
|:------------------|:--------------------------------|
| services          | components                      |
| depends_on        | links                           |
| networks          | package                         |
| image             | component in cloud              |
| ports             | ports properties in component   |
| aliases           | aliases properties in component |



## Install requirements
- Ubuntu 16.04
```
$ apt-get update && \
  apt-get install -y atom && \
  apm install markdown-preview-enhanced && \
  apt-get install -y plantuml && \
  apt-get install python-pip && \
  pip install pyyaml
```

## Usage
- Command
```
$ python dc2uml.py fullpath/inputfile.yml fullpath/outputfile.md
```



## Examples
- See [output.md](examples/output.md)
![example](examples/output.jpeg)

## Future works
- Refactoring
- Support
  - Exception cases
  - Other service settings
  - Dockerfile
  - Other plantuml diagrams
  - Other text-based uml tools
  - Offical plantuml format
  - Redefine correspondence
- Monolithic to microservices


## Related works
- compose_plantuml
  - https://github.com/funkwerk/compose_plantuml

## License
MIT
