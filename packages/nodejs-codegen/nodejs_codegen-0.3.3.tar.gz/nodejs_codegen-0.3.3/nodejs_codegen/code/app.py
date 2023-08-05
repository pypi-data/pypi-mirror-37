from codegenhelper import debug
import os
from code_engine import publish
from mapper_on_file import mapping

def get_resource_path(name):
    return os.path.join(os.path.split(__file__)[0], "..", name)

def gen(subscribe_name, data, output_path):
    publish(debug(get_resource_path('templates'), "gen:template_path"), \
            subscribe_name, \
            mapping(get_resource_path("mappers/%s.mapper" % subscribe_name), data),
            debug(output_path, 'gen:output_path')
            )
    
def run(data, output_path):
    gen("app", data, output_path)

