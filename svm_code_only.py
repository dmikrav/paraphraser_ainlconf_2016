import datetime
import time
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print st
#print antonym_get_page.compute_opposite_list_flag(['rose', 'fall'])

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

#print hashlib.md5(" In Kazakhstan there are no such problems, but in Russia.").hexdigest()
#sys.exit(0)
#print  ner("Returning from Syria Russians are concerned about employment in their homeland.", "Emergencies Ministry aircraft will take out the Russians from Syria destroyed. ")

# return the ROOT token
def loadroot(sen):
   for token in sen["sentences"][0]["basic-dependencies"]:
   	if (token["dep"] == "ROOT"):
		return sen["sentences"][0]["tokens"][int(token["dependent"])-1]

# input: two strings
# output: the cosine distance between them
def rootdist(string1, string2):
    str1md5 = hashlib.md5(string1).hexdigest()
    str2md5 = hashlib.md5(string2).hexdigest()
	  
    if (not os.path.exists("./json/"+str1md5+".json")):
	raise ValueError("file not found: "+string1)

    if (not os.path.exists("./json/"+str2md5+".json")):
        raise ValueError("file not found: "+string2)

    with open("./json/"+str1md5+".json") as data_file:
  	sen = json.load(data_file)
	root1 = loadroot(sen)
    with open("./json/"+str2md5+".json") as data_file:
	sen = json.load(data_file)
        root2 = loadroot(sen)
    return dist(root1["lemma"], root2["lemma"])

# ========================================================
def roots(sentence_1, sentence_2):
    str1md5 = hashlib.md5(sentence_1).hexdigest()
    str2md5 = hashlib.md5(sentence_2).hexdigest()
    flag = False
    if (not os.path.exists("./json/"+str1md5+".json")):
	#raise ValueError("file not found: "+sentence_1)
        print "file not found: "+sentence_1
        flag = True
    if (not os.path.exists("./json/"+str2md5+".json")):
        #raise ValueError("file not found: "+sentence_1)
        print "file not found: "+sentence_2
        flag = True
    if flag:
      return ["", ""]
    with open("./json/"+str1md5+".json") as data_file:
  	sen = json.load(data_file)
	root1 = loadroot(sen)
    with open("./json/"+str2md5+".json") as data_file:
	sen = json.load(data_file)
        root2 = loadroot(sen)
    return [root1["lemma"], root2["lemma"], str1md5+".json", str2md5+".json", sentence_1, sentence_2]

#**********************************************************
def get_word_net_similarity(root):
  #print "@@", root[0], root[1]
  try: 
    if root == None or len(root) != 6:
      return [0.12, 1.4, 0.2] #, 0.0, 0.0] #, 0.0, 0.0, 0.0]
    flag = False
    if len(wn.synsets(root[0])) == 0 or not is_there_part_of_speech('v', wn.synsets(root[0])):
      #print root[0]+';   ', root[4], '   ', root[2] 
      root = ['place', root[1]]
      flag = True
    if len(wn.synsets(root[1])) == 0 or not is_there_part_of_speech('v', wn.synsets(root[1])):
      #print root[1]+';   ', root[5], '   ',root[3]
      root = [root[0], 'place']
      flag = True
    if flag:
      #print "-" * 80
      return [0.12, 1.4, 0.2] #, 0.5, 0.5] #, 0.5, 0.5, 0.5]
    

    #print wn.synsets(root[0])
    s_1 = get_first_synset_part_of_speech('v', wn.synsets(root[0]))
    #print  wn.synsets(root[1])
    s_2 = get_first_synset_part_of_speech('v', wn.synsets(root[1]))
    res = [s_1.path_similarity(s_2),
           s_1.lch_similarity(s_2),
           s_1.wup_similarity(s_2)
           #s_1.res_similarity(s_2, brown_ic),
           #s_1.res_similarity(s_2, genesis_ic)
           #s_1.jcn_similarity(s_2, brown_ic),
           #s_1.jcn_similarity(s_2, genesis_ic),
           #s_1.lin_similarity(s_2, semcor_ic)
     ]
  except:
    #print len(root), root
    res = [0.12, 1.4, 0.2] #, 0.5, 0.5] #, 0.5, 0.5, 0.5]
  return res
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def is_there_part_of_speech(part_of_speech, synsets):
  n = len(synsets)
  for i in range(n):
    s = str(synsets[i])
    if s.find('.'+part_of_speech+'.') != -1:
      return True
  return False
#---------------------------------------------------------
def get_first_synset_part_of_speech(part_of_speech, synsets):
  n = len(synsets)
  for i in range(n):
    s = str(synsets[i])
    if s.find('.'+part_of_speech+'.') != -1:
      return synsets[i]
  return None
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def load_embeddings(fname):
    f = (line.split(" ",1)[1] for line in file(fname))
    vecs = np.loadtxt(f)
    words = [line.split(" ",1)[0] for line in file(fname)]
    return words,vecs

def dist(word1, word2):
    word1 = str(word1).lower()
    word2 = str(word2).lower()
    if (word1 in words and word2 in words):
    	return np.dot(vecs[words.index(word1)], vecs[words.index(word2)])
    else:
	return 0

def square(list):
  return [i ** 2 for i in list]

#clf = ensemble.RandomForestClassifier(n_estimators=20, max_features="auto")
clf = SVC(C=100.0, kernel='rbf')
#words,vecs = load_embeddings("./bow10.words")

#norms = la.norm(vecs, axis=1)
#nvecs = vecs / norms[:,np.newaxis]
#vecs = nvecs

classes_names = ["NON-paraphrase", "Near-paraphrase", "Precise-paraphrase"]

with open('dataset.json') as data_file:    
  data = json.load(data_file)
  
data_copy_task_1 = list(data)
data_copy_task_2 = data_copy_task_1
dataset_filtered_task_1 = data_copy_task_1
dataset_filtered_task_2 = data_copy_task_2

#for task_no in range(1):

task_no = 1
if task_no == 2:
  classes_ids = [[], []]
  #random.shuffle(data_copy)
  #print len(data_copy)
  #print "NON-paraphrase", len([a for a in data_copy if a["class"] == "NON-paraphrase"])
  #print "Precise-paraphrase", len([a for a in data_copy if a["class"] == "Precise-paraphrase"])
  #print "Near-paraphrase", len([a for a in data_copy if a["class"] == "Near-paraphrase"])
  
  for a in data_copy_task_2:
    #a["backup_class"] = a["class"]
    if a["class"] == classes_names[2]:
      a["class"] = classes_names[1]
  
  # filter new paraphrases
  #dataset_filtered = [a for a in data_copy if (a["class"] == "NON-paraphrase" or a["class"] == "Precise-paraphrase")]
  #dataset_filtered = [a for a in data_copy if (a["class"] == "NON-paraphrase" or a["class"] == "Precise-paraphrase" or (a["class"] == "Near-paraphrase"))] # and a["class"] = "Precise-paraphrase")]
  #print len(dataset_filtered)

  #train = [a["translations"]["google"]["features"].values()+square(a["translations"]["google"]["features"].values()) for a in dataset_filtered]
  #train = [a["translations"]["google"]["features"].values() for a in dataset_filtered]
  #for yy in range(6):
  #  sys.stdout = Logger("0_a_" + str(yy) + ".txt")
  #yy = 5
  train = [
          a["translations"]["google"]["features"].values()
        + a["translations"]["yandex"]["features"].values()
         
        + get_ner_score(a["translations"]["yandex"]["pair"][0], 
                        a["translations"]["yandex"]["pair"][1])
        
        + get_word_net_similarity(roots(a["translations"]["google"]["pair"][0], a["translations"]["google"]["pair"][1]))

        + get_word_net_similarity(roots(a["translations"]["yandex"]["pair"][0], a["translations"]["yandex"]["pair"][1]))
        + [a["translations"]["google"]["swoogle"]]
        + [a["translations"]["yandex"]["swoogle"]]
        
        # + [a["translations"]["yandex"]["antonym_bit"]]
        # get_ner_score(a["translations"]["google"]["pair"][0], a["translations"]["google"]["pair"][1])
  for a in dataset_filtered_task_2]
  #print train
  #train = [a["translations"]["google"]["features"].values()+a["translations"]["yandex"]["features"].values()+[rootdist(a["translations"]["yandex"]["pair"][0], a["translations"]["yandex"]["pair"][1])] for a in dataset_filtered]
  #train = [a["translations"]["yandex"]["features"].values() for a in dataset_filtered]

  classes = [a["class"] for a in dataset_filtered_task_2]

  #scores = cross_validation.cross_val_score(clf, train_float[0] + train_float[1], classes[0] + classes[1], cv=10)
  predicted = sklearn.cross_validation.cross_val_predict(clf, train, classes, cv=5, verbose=3)

  print "Accuracy:", metrics.accuracy_score(classes, predicted) 
  print "micro-F1:", metrics.f1_score(classes, predicted, average='micro', pos_label=None) 
  print "macro-F1:", metrics.f1_score(classes, predicted, average='macro', pos_label=None) 
  print metrics.confusion_matrix(classes, predicted)

  '''
  if task_no == 1:
    confusion_matrix = metrics.confusion_matrix(classes, predicted)
    print confusion_matrix
    non_paraphrases_wrong_count = confusion_matrix[0][1] + confusion_matrix[1][0]
    print non_paraphrases_wrong_count
    non_paraphrases_correct_count = confusion_matrix[0][0]
    print non_paraphrases_correct_count
  
  for x in range(N):
    if predicted[x] == classes_names[0]:
      classes_ids[0].append(dataset_filtered[x]['id'])
    if predicted[x] == classes_names[1]:
      classes_ids[1].append(dataset_filtered[x]['id'])
    
  '''
  """
  for x in range(7227):
    for y in range(3):
      if predicted[x] == classes_names[y]:
        classes_ids[y].append(dataset_filtered[x]['id'])
  """
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  print st
if task_no == 1:
    '''
    relevant_ids = classes_ids[1]
    data_task_no_1 = []
    for a in dataset_filtered:
      a['class'] = a['backup_class']
    data_task_no_1 = [a for a in dataset_filtered_task_1 if a['id'] in relevant_ids and a['class'] != classes_names[0]]
      #if a['id'] in relevant_ids and a['class'] != classes_names[0]:
      #  data_task_no_1 += a 
    #print data_task_no_1
      #[a for a in dataset_filtered if a['id'] in relevant_ids]
    '''
    classes = [a["class"] for a in dataset_filtered_task_1]
    train = [
          a["translations"]["google"]["features"].values()
        + a["translations"]["yandex"]["features"].values()
         
        + get_ner_score(a["translations"]["yandex"]["pair"][0], 
                        a["translations"]["yandex"]["pair"][1])
        
        + get_word_net_similarity(roots(a["translations"]["google"]["pair"][0], a["translations"]["google"]["pair"][1]))

        + get_word_net_similarity(roots(a["translations"]["yandex"]["pair"][0], a["translations"]["yandex"]["pair"][1]))
        + [a["translations"]["google"]["swoogle"]]
        + [a["translations"]["yandex"]["swoogle"]]
        
        # + [a["translations"]["yandex"]["antonym_bit"]]
        # get_ner_score(a["translations"]["google"]["pair"][0], a["translations"]["google"]["pair"][1])
    for a in dataset_filtered_task_1]

    predicted = sklearn.cross_validation.cross_val_predict(clf, train, classes, cv=5, verbose=3)
    '''
    non_paraphrases_correct_list = [classes_names[0]] * non_paraphrases_correct_count
    non_paraphrases_wrong_list   = [classes_names[1]] * non_paraphrases_wrong_count
    non_paraphrases_wrong_list_wrongly_put = [classes_names[0]] * non_paraphrases_wrong_count
    predicted = np.append(predicted, non_paraphrases_correct_list)
    classes += non_paraphrases_correct_list 
    predicted = np.append(predicted, non_paraphrases_wrong_list)
    classes += non_paraphrases_wrong_list_wrongly_put
    '''

    print "Accuracy:", metrics.accuracy_score(classes, predicted) 
    print "micro-F1:", metrics.f1_score(classes, predicted, average='micro', pos_label=None) 
    print "macro-F1:", metrics.f1_score(classes, predicted, average='macro', pos_label=None) 

    print metrics.confusion_matrix(classes, predicted)

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st
    
    #predicted += 
    #np.concatenate(predicted, charar)
    #np.concatenate(classes, charar)
    #predicted.append(classes_names[0])#.concatenate(charar)
    #classes.append(classes_names[0])#.concatenate(charar)
  
    """ 
  print "Accuracy:", metrics.accuracy_score(classes, predicted) 
  print "micro-F1:", metrics.f1_score(classes, predicted, average='micro', pos_label=None) 
  print "macro-F1:", metrics.f1_score(classes, predicted, average='macro', pos_label=None) 

  print metrics.confusion_matrix(classes, predicted)
  
  google_translated = [a["translations"]["google"]["pair"] for a in dataset_filtered]
  """
    
    for i in range(len(predicted)):
      if predicted[i] != classes[i] and classes[i] == classes_names[2]:
        print "=" * 80
        print "predicted:" , predicted[i] , ";  actual:" , classes[i] 
        print "-" * 80
        print(dataset_filtered_task_1[i]["id"])
        print(dataset_filtered_task_1[i]["source"][0].encode('utf8'))
        print(dataset_filtered_task_1[i]["source"][1].encode('utf8'))
        pprint(dataset_filtered_task_1[i]["translations"]["google"]) 
        pprint(dataset_filtered_task_1[i]["translations"]["yandex"])
        print "\n"
  
