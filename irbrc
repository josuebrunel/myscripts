require 'json'
require 'irb/completion'

def json_get_data(filename)
    return JSON.parse(File.read(filename))
end
