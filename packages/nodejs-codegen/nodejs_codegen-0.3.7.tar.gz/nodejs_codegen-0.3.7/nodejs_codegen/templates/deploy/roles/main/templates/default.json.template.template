{
    "port": {{'{{'}}{{ name }}_port{{'}}'}} {% if dep_services %},
{% for service in dep_services %}    "{{service.name}}": "{{'{{'}}{{service.name}}{{'}}'}}",
    "{{service.name}}_port": "{{'{{'}}{{service.name}}_port{{'}}'}}"{%if not loop.last %},{% endif %}
{% endfor %}{% endif %}
}