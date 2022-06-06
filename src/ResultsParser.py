import glob
import scandir
from threading import Thread
import configparser as ConfigParser  # keep compytibility with python 2.7


class TestResultParser:
    def __init__(self, path, limit_number_of_file=-1, recursive=False):
        self.dizionario = {}
        self.errors = []
        PATH = path

        # read all file in folder and create a list
        list_of_f = []
        if not recursive:
            for f in glob.glob(PATH + "/*.txt"):
                list_of_f.append(f)
        elif recursive:
            for root, dirs, files in scandir.walk(PATH):
                for f in files:
                    if f.endswith(".txt"):
                        list_of_f.append(root + "\\" + f)

        # sort the list from the newer to older
        list_of_f.sort(reverse=True)

        # keep the first "n" files
        if limit_number_of_file != -1:
            list_of_f = list_of_f[:limit_number_of_file]


        thrds = []
        i = 1
        for f in list_of_f:
            t = Thread(target=self.reader, args=(f, i))
            thrds.append(t)
            i += 1
            # each 50 files, execute the threads
            if i % 50 == 0:
                # start the threads
                for t in thrds:
                    t.start()
                # wait until all threads are finished
                for t in thrds:
                    t.join()
                # clean up the list of threads
                del thrds[:]

        # check if there are remaining thread to start
        if thrds:
            # start the threads
            for t in thrds:
                t.start()
            # wait until all threads are finished
            for t in thrds:
                t.join()
            # clean up the list of threads
            del thrds[:]

    def reader(self, f, i):
        try:
            parser = ConfigParser.ConfigParser()
            parser.read(f)
            self.dizionario[i] = parser._sections
            self.dizionario[i]["GENERIC"]["path"] = f
        except Exception:
            self.errors.append(f)
            print("ERROR: error raised with TC: " + f)

    def get_dictionary(self):
        return self.dizionario, self.errors

    def count(self):
        return len(self.dizionario)
