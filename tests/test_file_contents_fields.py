from tweetkeywordmapper.core import data
from tweetkeywordmapper.core import constants as cons

ws = cons.workspace
default_file = cons.default_file

file, file_ext = data.get_user_file(default_file)
contents, fields = data.get_file_contents_fields(file, file_ext)

print(contents)
print(fields)