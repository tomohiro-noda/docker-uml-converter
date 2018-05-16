# docker-uml-converter
Convert docker-compose.yml to plantuml with atom:markdown-preview-enhanced using python

## Supported service settings
Must define service settings below in docker-compose.yml
- Docker-compose v3
  - services
  - depends_on
  - networks
  - image
  - ports
  - aliases

## Supported uml tools
- Plantuml
  - component diagram

## Install requirements
- Ubuntu 16.04
```
$ apt-get install -y atom && \
  apm install markdown-preview-enhanced && \
  apt-get install -y plantuml
```

## Usage
```
$ python dc2uml.py fullpath/inputfile.yml fullpath/outputfile.md
```
## Examples
- See [example](examples/output.md)

## Development plans
- Refactoring
- Support
  - Exception cases
  - Other service settings
  - Dockerfile
  - Other plantuml diagrams
  - Other text-based uml tools
- Monolithic to microservices

## License
MIT
