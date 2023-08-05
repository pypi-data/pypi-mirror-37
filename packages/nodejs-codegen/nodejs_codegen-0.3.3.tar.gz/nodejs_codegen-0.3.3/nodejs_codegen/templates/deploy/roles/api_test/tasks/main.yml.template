---
{% for method in methods %}
- name: test for {{method}}
  uri:
    url: "{{'{{'}}{{name}}_test_url{{'}}'}}/act"
    method: POST
    body_format: json
    return_content: yes
    body: {
      "action": "{{method.name}}",
      "param": {}
    }
    register: {{method}}_result

- debug: var={{method}}_result.content
{% endfor %}

...