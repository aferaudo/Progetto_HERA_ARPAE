import logging
from datetime import datetime
import os
import argparse

class DeleteAction(argparse.Action):
    def __call__(self,parser,namespace,values,option_string=None):
        did_delete = getattr(namespace,'delete',False)
        if did_delete == False:
            parser.error("enable delete option before specifying days!")
        else:
            setattr(namespace,self.dest,values)

def destroy_hera(file_list, days_ai, days_di, soft=False):
    """
    Methods that destroy too old files. 
    The age threshold can be set through the parameters days_ai and day_di
    If soft is enabled files are moved in a direcotory named "old"
    """
    now = datetime.now()
    counter = 0
    for file_name in file_list:
        if not "AI" in file_name and not "DI" in file_name:
            continue
        date_file = datetime.strptime(file_name[4:18], "%Y%m%d%H%M%S")
        day_difference = now - date_file
        
        if (day_difference.days > days_ai 
        and "AI" in file_name) or (day_difference.days > days_di 
        and "DI" in file_name):
            logging.info("Destroying %s...", "{}".format(file_name))
            counter += 1
            if soft:
                logging.info("Softly..")
                # Check if the directory "old" where to move file exists
                if not os.path.isdir("old"):
                    os.mkdir("old")
                # Moving the file
                os.rename(file_name, "old/{}".format(file_name))
            else:        
                os.remove(file_name)
    return counter