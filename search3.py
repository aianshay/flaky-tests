import pandas as pd
import subprocess as sb
import sh
import logging


def get_row_class(dataset_row):
    class_name = dataset_row.class_
    class_name = class_name.split(".")
    class_name = class_name[-1]
    return class_name


def get_class_name_from_path(path_):
    name_found = path_.split("/")
    name_found = name_found[-1].split(".")[0]
    return name_found


def get_superclass(subclass_path):
    try:
        command = get_class_name_from_path(subclass_path) + ' extends'
        header = sh.grep(sh.cat(subclass_path.rstrip()), command)
        header = header.split(" ")
        superclass = header[header.index('extends') + 1]
        return superclass
    except sh.ErrorReturnCode_1:
        return 0


def find_class(class_name):
    class_name += '.java'
    find_result = sb.check_output('find . -iname ' + class_name, shell=True)
    find_result = find_result.decode('utf-8')
    return find_result


def search_method(class_path_, method_):
    logging.warning(f'Class path: {class_path_}')
    try:
        found_method = sh.grep(sh.cat(class_path_.rstrip()), method_)
        logging.warning(f'Method found! \n {found_method.__str__()}')
        return 1
    except sh.ErrorReturnCode_1:
        logging.warning('Missing method, searching on superclass...')
        superclass = get_superclass(class_path_.rstrip())

        if superclass:
            superclass_path = find_class(superclass)
            if superclass_path:
                logging.warning(f'Target superclass: {superclass}')
                return search_method(superclass_path, method_)
            else:
                logging.warning(f'Can´t find superclass {superclass}.')
                return 0
        else:
            logging.warning(f"{class_} does not has superclass.")
            return 0


logging.basicConfig(filename='searcher.log', format='%(message)s', level=logging.WARNING)
dataset = pd.read_csv('dataset.csv')
found = []
total_rows = dataset.shape[0]

for row in dataset.itertuples():
    print(f'Analysing row {str(row.Index + 1)}/{total_rows}.')
    git_command = 'git reset --hard ' + row.sha
    git_cmd_error = sb.call(git_command, shell=True)
    
    if git_cmd_error == 0:
        logging.warning(git_command + ' SUCCESS!')
    else:
        logging.warning(git_command + ' FAILED!')
    
    class_ = get_row_class(row)
    logging.warning(f'Target class: {class_}    ')

    path = find_class(class_)
    class_qty = path.count('./')
    method = row.method

    logging.warning(f'{class_qty} class(es) found')
    logging.warning(f'Target method: {method}')

    paths = path.split('./')
    count = 0
    for class_path in paths[1:]:
        count += search_method(class_path, method)

    found.append(count)
        
dataset['Found'] = found
dataset.to_csv('dataset.csv', index=False)
logging.warning(f"{sum(dataset['Found'])} method(s) found (~{sum(dataset['Found'])*100/total_rows}%).\n"
                f"{sum(dataset['Found'] == 0)} method(s) missing.")
logging.warning('Dataset updated with results.')
