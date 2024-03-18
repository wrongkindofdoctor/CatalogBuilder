import os
from intakebuilder import getinfo
import utils
import re


@utils.crawler.maker
class SyntheticDataCrawler:
    """
      SyntheticDataCrawler traverses directories of synthetic model data
      generated by the mdtf_test_data Python package
    """
    def __init__(self):
        print('SyntheticDataCrawler initialized')

    def crawl(self, projectdir: None, dict_filter: dict, logger):
        """
        Crawl through the local directory and run through the getInfo.. functions
        :param projectdir: base directory with the synthetic data files
        :param dict_filter: optional dictionary with values to include for each DRS component
        Synthetic data DRS: {Dataset Name (matches miptable attribute)}/
        {frequency}/{Dataset Name}.{variable name}.{frequency}.nc
        :return:listfiles which has a dictionary of all key/value pairs for each file to be added to the csv
        """
        if not projectdir:
            projectdir = os.path.dirname(os.path.realpath(__file__))
        listfiles = []
        pat = None
        if ("miptable" in dict_filter.keys()) & ("frequency" in dict_filter.keys()):
            pat = re.compile('({}/{}/)'.format(dict_filter["miptable"], dict_filter["frequency"]))
        elif "miptable" in dict_filter.keys():
            pat = re.compile('({}/)'.format(dict_filter["miptable"]))
        elif "frequency" in dict_filter.keys():
            pat = re.compile('({}/)'.format(dict_filter["frequency"]))
        orig_pat = pat
        for dirpath, dirs, files in os.walk(projectdir):
            # print(dirpath, dictFilter["source_prefix"])
            if dict_filter["source_prefix"] in dirpath:  # T ODO improved filtering
                searchpath = dirpath
                if orig_pat is None:
                    pat = dirpath  # we assume matching entire path
                #  print("Search filters applied", dictFilter["source_prefix"], "and", pat)
                if pat is not None:
                    m = re.search(pat, searchpath)
                    for filename in files:
                        logger.info(dirpath + "/" + filename)
                        dictInfo = {}
                        dictInfo = getinfo.getProject(projectdir, dictInfo)
                        # get info from filename
                        # print(filename)
                        filepath = os.path.join(dirpath,
                                                filename)
                        # the full path to the file
                        if not filename.endswith(".nc"):
                            logger.debug("File is not a netCDF file. Skipping", filepath)
                            continue
                        dictInfo["path"] = filepath
                        #                  print("Callin:g getinfo.getInfoFromFilename(filename, dictInfo)..")
                        dictInfo = getinfo.getInfoFromFilename(filename, dictInfo, logger)
                        #                  print("Calling getinfo.getInfoFromDRS(dirpath, projectdir, dictInfo)")
                        dictInfo = getinfo.getInfoFromDRS(dirpath, projectdir, dictInfo)
                        #                  print("Calling getinfo.getInfoFromGlobalAtts(filepath, dictInfo)")
                        #                  dictInfo = getinfo.getInfoFromGlobalAtts(filepath, dictInfo)
                        # eliminate bad DRS filenames spotted
                        list_bad_modellabel = ["", "piControl", "land-hist", "piClim-SO2", "abrupt-4xCO2", "hist-piAer",
                                               "hist-piNTCF", "piClim-ghg", "piClim-OC", "hist-GHG", "piClim-BC",
                                               "1pctCO2"]
                        if dictInfo["model"] in list_bad_modellabel:
                            logger.debug(
                                "Found experiment name in model column, skipping this possibly bad DRS filename",
                                dictInfo["experiment"], filepath)
                            continue
                        listfiles.append(dictInfo)
                        # print(listfiles)