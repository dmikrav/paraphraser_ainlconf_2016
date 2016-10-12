# -*- coding: utf-8 -*-
# encoding=utf8  
import sys, json, re
reload(sys)  
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    f = open("test_res.json")
    dict_main = json.load(f)
    f.close()
    f = open("test_res_only_final.json")
    dict_final = json.load(f)
    f.close()
    n = len(list(dict_main))
    n2 = len(list(dict_final))
    if n != n2:
      raise Exception("\n  n1 = " + str(n) + "; n2 = " + str(n2) + "\n\n   Quiting...\n\n")
      sys.exit()
    for i in range(n):
      dict_main[i]['source_acronym_resolved_final'] = dict_final[i]
    f = open("test_res_final.json", "w+")
    f.write(json.dumps(dict_main, sort_keys=True, indent=1, separators=(',', ': '), ensure_ascii=False))
    f.close()