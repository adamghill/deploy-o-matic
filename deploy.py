import sys, os, shutil

# Config settings
restart_apache_cmd = 'apache2/bin/restart'
staging_root = 'staging/htdocs/'
production_root = 'production/htdocs/'
files_to_ignore = []
extensions_to_ignore = ['.pyc']


def sizeof_fmt(num):
  for x in ['bytes','KB','MB','GB','TB']:
    if num < 1024.0:
      return "%3.3f%s" % (num, x)
    num /= 1024.0

files_to_copy = {}

for root, dir, files in os.walk(staging_root):
  for file in files:
    if file not in files_to_ignore and os.path.splitext(file)[1] not in extensions_to_ignore:
      staging_filename = os.path.join(root, file)
      production_filename = staging_filename.replace(staging_root, production_root)

      if not os.path.exists(production_filename) or os.path.getsize(staging_filename) != os.path.getsize(production_filename):
        if os.path.exists(production_filename):
          print file + ' is ' + sizeof_fmt(os.path.getsize(staging_filename)) + ' on staging, but ' + sizeof_fmt(os.path.getsize(production_filename)) + ' on production'
          #print os.system('diff ' + staging_filename + ' ' + production_filename)
        else:
          print file + ' not found on production'

        files_to_copy[staging_filename] = production_filename

print ''
print 'Total number of files to update: ' + str(len(files_to_copy))
print 'd to diff, Y to copy, Enter to skip, x to exit'

for staging_filename in files_to_copy:
  print ''
  production_filename =  files_to_copy[staging_filename]
  
  question = 'Copy ' + os.path.basename(staging_filename) + ' to ' + production_filename  + '? '
  if os.path.exists(production_filename):
    question = 'Overwrite ' + production_filename  + '? '
  
  input = raw_input(question)

  if input.lower() == 'x':
    sys.exit()

  if input.lower() == 'd':
    if os.path.exists(production_filename):
      print os.system('diff ' + staging_filename + ' ' + production_filename)
      input = raw_input(question)
    else:
      print 'No file on production to diff against'

  if input == 'Y':
    print 'Copying ' + staging_filename + ' to ' + production_filename
    shutil.copy2(staging_filename, production_filename)

input = raw_input('Restart Apache? ')

if input == 'Y':
  os.system(restart_apache_cmd)
