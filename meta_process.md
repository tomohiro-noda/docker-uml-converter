```puml
start
:input_yml;
fork
:extract_service_1;
:convert_to_uml;
fork again
:extract_service_n;

:convert_to_uml;
end fork
:combine_uml;
:output_uml;
end
```
