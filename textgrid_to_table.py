import os
import locations

def make_command(filename, output_directory):
    filename = os.path.abspath(filename)
    output_directory = os.path.abspath(output_directory) + '/'
    name = filename.split('/')[-1].split('.')[0]
    output_filename = output_directory + name + '.csv'
    cmd = 'filename$ = "' + filename + '"\n'
    cmd += 'table_filename$ = "' + output_filename + '"\n'
    cmd += 'name$ = "' + name + '"\n'
    cmd += 'Read from file: filename$\n'
    cmd += 'Down to Table: "no", 6, "yes", "no"\n'
    cmd += 'Save as comma-separated file: table_filename$\n'
    cmd += 'selectObject: "TextGrid " + name$\n'
    cmd += 'plusObject: "Table " + name$\n'
    cmd += 'Remove\n'
    return cmd

def make_all_commands(filenames, output_directory, script_filename = ''):
    cmds = ''
    for filename in filenames:
        cmds += make_command(filename, output_directory)
    if script_filename:
        with open(script_filename, 'w') as f:
            f.write(cmds)
    return cmds

def make_coolest_tables():
    filenames = locations.fn_coolest_textgrids
    output_directory = locations.coolest_tables
    f = locations.coolest + 'coolest_tables.praat'
    make_all_commands(filenames, output_directory, f)
