import re
#import pickle

#STATS_FILE = "stats.pickle"
LOG_FILE = "main.log"

class StatsHandler(object):
    def __init__(self):
        self.execute()
        
    def execute(self):
        self.stats = {}
        self.line_number = 0
        self.pattern = re.compile(r"(?<!404) GET\s(.*?)\s\((.*)\)")
        self.log_file = [line.strip() for line in open(LOG_FILE)]
        self.compute_log()
    def compute_log(self):
        try:
            for line in self.log_file[self.line_number:]:
                m = self.pattern.search(line)
                if m is not None:
                    if m.group(1) in self.stats.keys():
                        if m.group(2) in self.stats[m.group(1)].keys():
                            self.stats[m.group(1)][m.group(2)] += 1
                        else:
                            self.stats[m.group(1)][m.group(2)] = 1
                            
                    else:
                        self.stats[m.group(1)] = {m.group(2):1}
                self.line_number += 1
        except Exception as e:
            print(e)
            print(self.line_number)
            raise Exception

def test():
    s = StatsHandler()

if __name__ == "__main__":
    from timeit import timeit, repeat
    s = StatsHandler()
    print(repeat("test()", setup="from __main__ import test", number = 1, repeat = 10))
    #print(Timer(timer=s.execute).repeat(5,1))
#    def load_status():
#        with open(STATUS_FILE, "rb") as f:
#            return pickle.load(f)
#
#    def dump_status(status):
#        with open(STATUS_FILE, "wb") as f:
#            pickle.dump(status, f, pickle.HIGHEST_PROTOCOL)



