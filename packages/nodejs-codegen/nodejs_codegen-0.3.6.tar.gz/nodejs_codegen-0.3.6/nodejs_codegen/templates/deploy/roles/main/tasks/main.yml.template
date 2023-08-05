---
- name: init deploy folder
  file:
    path: "{{'{{'}} deploy_root {{'}}'}}"
    state: directory

- name: copy files to deploy folder
  synchronize:
    src: "./src/"
    dest: "{{'{{'}}deploy_root{{'}}'}}"
    
- name: "configure {{ name }}"
  template:
    src: default.json.template
    dest: "{{'{{'}}deploy_root{{'}}'}}/config/default.json"


- name: "deploy {{ '{{' }} {{ name }} {{ '}}' }} for debug"
  docker_container:
    name: "{{'{{'}} {{ name }} {{'}}'}}"
    image: "node:6.10.3"
    working_dir: "/var/app"
    volumes:
      - "{{'{{'}}deploy_root{{'}}'}}:/var/app:Z"
    ports:
      - "{{'{{'}} {{ name }}_port {{'}}'}}:{{'{{'}} {{ name }}_port {{'}}'}}"
{% if dep_services is not none %} 
    links:
{% for service in dep_services %}      - "{{'{{'}}{{service.name}}{{'}}'}}:{{'{{'}}{{service.name}}{{'}}'}}"
{% endfor %}      
{% endif %}      
    restart: yes
    recreate: yes
    state: started
    entrypoint: "node app.js"
  when: {{ name }}_debug=="true"

- Name: "deploy {{'{{'}} {{ name }} {{'}}'}} for integration"
  docker_container:
    name: "{{'{{'}} {{ name }} {{'}}'}}"
    image: "node:6.10.3"
    working_dir: "/var/app"
    volumes:
      - "{{'{{'}}deploy_root{{'}}'}}:/var/app:Z"
    exposed: "{{'{{'}} {{ name }}_port{{'}}'}}"
{% if dep_services is not none %} 
    links:
{% for service in dep_services %}      - "{{'{{'}}{{service.name}}{{'}}'}}:{{'{{'}}{{service.name}}{{'}}'}}"
{% endfor %}      
{% endif %}      
    restart: yes
    recreate: yes
    state: started
    entrypoint: "node app.js"
  when: {{ name }}_debug=="false"



...
