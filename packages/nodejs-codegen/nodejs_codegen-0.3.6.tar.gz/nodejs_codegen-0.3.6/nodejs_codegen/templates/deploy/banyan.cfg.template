{
  "name": "{{name}}",
  "dependencies": [
  {% for serv in dep_services %}{
     "project_name": "{{serv.name}}"
     }{% if not loop.last %},{% endif %}
  {% endfor %}
  ],
  "roles_seq": ["main", "api_test"],
  "predefined_variables": {
    "host": "130.71.32.2"
  }
}