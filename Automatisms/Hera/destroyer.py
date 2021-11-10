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

def destroy_hera(file_list, days_ai, days_di):
    now = datetime.now()
    for file_name in file_list:
        if not "AI" in file_name and not "DI" in file_name:
            continue
        date_file = datetime.strptime(file_name[4:18], "%Y%m%d%H%M%S")
        day_difference = now - date_file
        
        if (day_difference.days > days_ai 
        and "AI" in file_name) or (day_difference.days > days_di 
        and "DI" in file_name):
            logging.info("Destroying %s...", "{}".format(file_name))
            os.remove(file_name)