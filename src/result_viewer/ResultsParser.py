import glob
import scandir
import configparser
import traceback
import os
import re
import logging
import datetime


def match_file_name(_string=""):
    if re.search("txt$", _string) and re.search(r"\d\d\d\d[-_]\d\d[-_]\d\d[-_]\d\d[-_]\d\d[-_]\d\d[-_]", _string):
        return True
    return False


class TestResultParser:
    def __init__(self, folder_path, limit_number_of_file=-1, recursive=False):
        self.dizionario = {}
        self.errors = []

        list_of_f = self._collect(folder_path, limit_number_of_file, recursive)
        self.parse(list_of_f=list_of_f)

    def parse(self, list_of_f=None):
        for idx, f in enumerate(list_of_f, start=1):
            self._read(f, idx)

    @staticmethod
    def _collect(folder_path, limit_number_of_file=-1, recursive=False):
        """
        collect all files in folder and create a list
        :return: List of files path
        """
        list_of_f = []
        if not recursive:
            for f in glob.glob(os.path.join(folder_path, "*")):
                if match_file_name(f):
                    list_of_f.append(f)
        elif recursive:
            for root, dirs, files in scandir.walk(folder_path):
                for f in files:
                    if match_file_name(f):
                        file_path = os.path.join(root, f)
                        list_of_f.append(file_path)

        # sort the list from the newer to older
        list_of_f.sort(reverse=True)

        # keep the first "n" files
        if limit_number_of_file != -1:
            list_of_f = list_of_f[:limit_number_of_file]

        return list_of_f

    def _read(self, f, idx):
        try:
            parser_ = configparser.ConfigParser()
            parser_.read(f)
            self.dizionario[idx] = parser_._sections
            self.dizionario[idx]["GENERIC"]["path"] = f
        except Exception:
            self.errors.append(f)
            logging.error(f"Issue found with test result: {f}\n{traceback.format_exc()}\n")

    def get_dictionary(self):
        return self.dizionario, self.errors

    def count(self):
        return len(self.dizionario)

    def metrics(self):
        metrics = {}
        _pass = 0
        fail = 0
        skip = 0
        other = 0
        for i in self.dizionario:
            if self.dizionario[i]["GENERIC"]["result"] == "OK":
                _pass += 1
            elif self.dizionario[i]["GENERIC"]["result"] == "NOT OK":
                fail += 1
            elif self.dizionario[i]["GENERIC"]["result"] == "NOT TESTED":
                skip += 1
            else:
                other += 1

        metrics["total"] = len(self.dizionario)
        metrics["pass"] = _pass
        metrics["fail"] = fail
        metrics["skip"] = skip
        metrics["other"] = other
        return metrics

    def is_checksum_valid(self):
        checksum_list = []
        for i in self.dizionario:
            checksum_list.append(self.dizionario[i]["ENVIRONMENT"]["checksum calibration and application"])

        if len(set(checksum_list)) > 1:
            return list(set(checksum_list))
        return 0

    def get_files(self):
        list_of_files_path = []
        for idx in self.dizionario:
            list_of_files_path.append(self.dizionario[idx]["GENERIC"]["path"])
        return list_of_files_path

    def get_testing_days(self):
        total_tc = len(self.dizionario)
        if total_tc < 1:
            raise Exception("No test found")

        dates = []
        for idx in self.dizionario:
            dates.append(datetime.datetime.strptime(self.dizionario[idx]["GENERIC"]["test execution date"], '%d/%m/%Y'))

        oldest_date = max(dates)
        youngest_date = min(dates)
        delta_date = oldest_date - youngest_date
        delta_date = delta_date.days
        # delta_date += 1
        return delta_date

    def are_comment_filled(self):
        raise NotImplementedError()

    def are_incident_number_filled(self):
        raise NotImplementedError()

    @staticmethod
    def open(self):
        raise NotImplementedError()

    @staticmethod
    def delete(self):
        raise NotImplementedError()

    @staticmethod
    def replace(self):
        raise NotImplementedError()
