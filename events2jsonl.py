import os
import sys
import json
import pyevt
import pyevtx
import logging
import argparse
import xmltodict

logging.basicConfig(
    level=logging.DEBUG
)

FORCE_ARRAY = (
    'Data',
    'Binary',
)

def GetOptions():
    usage = "{}\n\n" \
            "Parse Windows Event files and output records in the JSONL format." \
            .format(
                os.path.basename(sys.argv[0])
            )
    
    options = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(usage)
    )
    
    options.add_argument(
        '-s',
        '--source',
        dest='source',
        action="store",
        type=unicode,
        required=True,
        help='The source (file or folder)'
    )
    
    return options

def IsEventLog(file_path):
    """Check if file is event log. Currently only checking by extention.
    
    Params:
        file_path: the name of the file to check
    Returns:
        bool
    """
    if (file_path.lower().endswith('.evtx') or
            file_path.lower().endswith('.evt')):
        return True
    
    return False

def ProcessFolder(folder_path):
    """Process a folder recursively
    
    Params:
        folder_path: The folder to recursively look through.
    """
    for root, subdirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root,file)
            if IsEventLog(file_path):
                ProcessEventFile(file_path)

def ProcessEventFile(file_path):
    """Process an event log file.
    
    Params:
        file_path (str|unicode): Location of the eventlog
    """
    if file_path.lower().endswith('.evtx'):
        evtx_file = pyevtx.file()
        evtx_file.open(file_path)
        ProcessEventLog(evtx_file,file_path)
    elif file_path.lower().endswith('.evt'):
        evt_file = pyevt.file()
        evt_file.open(file_path)
        ProcessEventLog(evt_file,file_path)
    else:
        raise Exception("File not processed (needs .evtx or .evt extention): {}".format(
            file_path
        ))

def ProcessEventLog(eventlog,source_name):
    """Process an eventlog.
    
    Params:
        eventlog (pyevt.file|pyevtx.file) - The eventlog file handle
        source_name (str|unicode): The name of the source file
    """
    logging.info("processing {}".format(source_name))
    
    info = {
        '_source': source_name
    }
    
    if eventlog.number_of_records > 0:
        for i in range(0,len(eventlog.records)):
            try:
                record = eventlog.records[i]
            except Exception as error:
                logging.error(u"Error: {} at records index {}".format(
                    unicode(error), i
                ))
                continue
            
            try:
                xml_string = record.get_xml_string()
            except Exception as error:
                logging.error(u"Error: {} at records index {}".format(
                    unicode(error), i
                ))
                continue
            
            try:
                xml_dict = Xml2Dict(xml_string)
            except Exception as error:
                logging.error(u"Error: {} at records index {}".format(
                    unicode(error), i
                ))
                continue
            
            ProcessRecord(xml_dict,metadata=info)
            
    if eventlog.number_of_recovered_records > 0:
        for i in range(len(eventlog.recovered_records)):
            try:
                record = eventlog.recovered_records[i]
            except Exception as error:
                logging.debug(u"Error: {} at recovered_records index {}".format(
                    unicode(error), i
                ))
                continue
            
            try:
                xml_string = record.get_xml_string()
            except Exception as error:
                logging.error(u"Error: {} at records index {}".format(
                    unicode(error), i
                ))
                continue
            
            try:
                xml_dict = Xml2Dict(xml_string)
            except Exception as error:
                logging.error(u"Error: {} at records index {}".format(
                    unicode(error), i
                ))
                continue
            
            ProcessRecord(xml_dict,metadata=info)
    
def Xml2Dict(xml_string):
    """Convert a xml string into a dictionary.
    
    Params:
        xml_string (str|unicode) - The XML string
    Returns:
        (dict) - The dictionary representing the XML
    """
    xml_string = xml_string.strip(b'\0')
    xml_dict = xmltodict.parse(
        xml_string,
        force_list=FORCE_ARRAY,
        attr_prefix=''
    )['Event']
    return xml_dict

def ProcessRecord(xml_dict,metadata=None):
    """Process the xml dictionary of the event record.
    
    Params:
        xml_dict (dict) - The dictionary representing the event record
        metadata (dict|None) - Additional information to be added to the record
    """
    if metadata:
        xml_dict.update(metadata)
    json_str = json.dumps(xml_dict)
    print(u"{}".format(json_str))

def Main():
    arguements = GetOptions()
    options = arguements.parse_args()
    
    if os.path.isfile(options.source):
        ProcessEventFile(options.source)
    elif os.path.isdir(options.source):
        ProcessFolder(options.source)
    else:
        raise Exception("Unknown source: {}".format(options.source))

if __name__ == '__main__':
    Main()