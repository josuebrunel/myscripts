require 'json'
require 'yaml'
require 'irb/completion'

# JSON
def json_get_data(filename)
    return JSON.parse(File.read(filename))
end

def json_write_data(filename, data)
    return File.write(filename, data.to_json)
end

# YAML
def yaml_get_data(filename)
   return YAML::load_file(filename)
end

def yaml_write_data(filename, data)
    return File.write(filename, data.to_yaml)
end
