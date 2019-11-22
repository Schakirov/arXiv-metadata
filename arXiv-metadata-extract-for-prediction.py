## When month goes to august,  need change line:
## currID.find('1907')

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


keywords = ['state-of-the-art', 'state of the art', 'github', 'source code', 'bert', 'gpt', 'alphazero']
bad_keywords = ['medic', 'clinic', 'patient', 'diseas', 'random forest', 'k-mean', 'svm', 'kernel', 'bandit', 'boltzmann', 
                'magnetic resonance', 'theor', 'gaussi', 'mammogra', 'diagnos', 'patholog', 'adversarial att', 
                'bayes', 'recommendat', 'named entity']
good_authors = ['Bengio, Yoshua', 'Quoc', 'Vinyals', 'Salakhutdinov', 'Freitas', 'Kyunghyun',
                  'Hinton', 'Schmidhuber', 'Ng, Andr', 'LeCun', 'Hassabis', 'Goodfellow',
                  'Oord, A', 'Pascanu, R', 'Lillicrap', 'Nøkland', 'Sutskever', 'Yuille', 'Zisserman, A', 
                  'Sukhbaatar', 'Joulin, A', 'Ranzato, Ma', 'Simonyan, Ka', 'Malik, J', 'Fei-Fei, Li']
also_good_authors = ['']
good_subjects = ['cs:CL', 'cs:NE', 'cs:RO']
subjects_to_follow = {'Computer Science - Robotics' : 'cs:RO', 'Computer Science - Sound' : 'cs:SD', 
                      'Computer Science - Artificial Intelligence' : 'cs:AI', 
                      'Computer Science - Neural and Evolutionary Computing' : 'cs:NE', 
                      'Statistics - Machine Learning' : 'stat:ML', 'Computer Science - Machine Learning' : 'cs:ML', 
                      'Computer Science - Emerging Technologies' : 'cs:ET', 
                      'Computer Science - Computation and Language' : 'cs:CL', 
                      'Computer Science - Computer Vision and Pattern Recognition' : 'cs:CV'}                  
f = open("arXiv-meta-block4 -- 2017-19 all.xml", "r")
## fW = open("arxiv-meta-block-4better2.html", "w+")
articles = {}
a = f.read()
indBeg = 0;   indEnd = 0
while indBeg > -1:
    indBeg = a.find('<record>', indEnd)
    indEnd = a.find('</record>', indBeg)
    b = a[indBeg:indEnd] ## current record ab. some article    
    i1 = b.find('<identifier>')
    i2 = b.find('</identifier>')
    identifier = b[i1+26:i2]  ## 26 = len("<identifier>oai:arXiv.org:")
    ## fW.write("<a href='http://arxiv.org/pdf/" + identifier + ".pdf'>" + identifier + "</a></br>\n")
    articles[identifier] = {}
    articles[identifier]['if-good'] = 0
    
    i1 = b.find('<dc:title>')
    i2 = b.find('</dc:title>')
    title = b[i1+10:i2]
    ## fW.write("<b>" + title + "</b></br>\n")
    articles[identifier]['title'] = title
    
    ## fW.write("Authors: ")
    i1 = 0;   i2 = 0
    creators = []
    while i1 > -1:
        i1 = b.find('<dc:creator>', i2)
        i2 = b.find('</dc:creator>', i1)
        if i2 > -1:
            creator = b[i1+12:i2]
            ## fW.write(creator + ", &nbsp&nbsp")
            creators.append(creator)
    articles[identifier]['creators'] = creators
    
    i1 = 0;   i2 = 0
    articles[identifier]['subjects-to-follow'] = 0
    articles[identifier]['subject'] = '('
    while i1 > -1:
        i1 = b.find('<dc:subject>', i2)
        i2 = b.find('</dc:subject>', i1)
        if i2 > -1:
            subject = b[i1+12:i2]
            if subject in subjects_to_follow:
                articles[identifier]['subjects-to-follow'] = 1
                articles[identifier]['subject'] += subjects_to_follow[subject] + ", "  ## brief name
    articles[identifier]['subject'] = articles[identifier]['subject'][:-2] + ")"
    for good_subject in good_subjects:
        if articles[identifier]['subject'].find(good_subject) > -1:
            articles[identifier]['if-good'] += 0.1
    
    i1 = b.find('<dc:description>')
    i2 = b.find('</dc:description>')
    description = b[i1+16:i2]
    description = description.replace('\\n'," ")
    for keyword in keywords:
        if description.lower().find(keyword.lower()) > -1:
            red_idx = description.lower().find(keyword.lower())
            description = description[:red_idx] + '<font color="red">' + description[red_idx: red_idx + len(keyword)] \
            + '</font>' + description[red_idx + len(keyword) :]
            articles[identifier]['if-good'] += 1
    for keyword in bad_keywords:
        if description.lower().find(keyword.lower()) > -1:
            red_idx = description.lower().find(keyword.lower())
            description = description[:red_idx] + '<font color="blue">' + description[red_idx: red_idx + len(keyword)] \
            + '</font>' + description[red_idx + len(keyword) :]
            articles[identifier]['if-good'] -= 0.5
    ## fW.write(description + "</br></br>\n\n")
    articles[identifier]['description'] = description
    articles[identifier]['if-good'] -= 0.0001 * len(description)


### THE ONLY CHANGES APPLIED TO WHAT'S BELOW THIS LINE:    (and also "fW" commented in several other lines)
import pickle
import re
import numpy as np
import random
work_dir = '/media/1Tb/test/del/'

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

qual = load_obj(work_dir + 'qual.pkl')

articlesData = {}
for key in articles.keys():
    currID = str(key)
    if currID not in articles.keys():
        print(currID + ' has not been found in articles')
        continue
    articlesData[currID] = {}
    if currID not in qual.keys():
        if random.randint(0,100) > 70:
            articlesData[currID]['label'] = 0
        else:
            del articlesData[currID]
            continue  ## 125 000  overall articles,  from which just ~3500 are in the conspect
    else:
        articlesData[currID]['label'] = qual[key]
    subj_list =  ['cs:RO', 'cs:SD', 'cs:AI', 'cs:NE', 'stat:ML', 'cs:ML',  'cs:ET',  'cs:CL',  'cs:CV']
    articlesData[currID]['subject-labels'] = [0] * len(subj_list)
    for i in range(len(subj_list)):
        if articles[currID]['subject'].find( subj_list[i] ) > -1 :
            articlesData[currID]['subject-labels'][i] = 1
    articlesData[currID]['creators'] = articles[currID]['creators']
    articlesData[currID]['content'] = articles[currID]['title'] + ' ' + articles[currID]['description'] 
    articlesData[currID]['content'] = re.sub('<[^>]*>', '', articlesData[currID]['content'])   ## to clear all alike   <font color...> etc
    ## articlesData[currID]['content'] = re.sub('\((cs.[^)]+)\)', r"\1", articlesData[currID]['content'])   ## to clear () from  (cs.CL)

# del articles ## to save memory...  we need "articles" no more

all_creators = {}
for key in articlesData.keys():
    if 'creators' in articlesData[key].keys():
        for k in articlesData[key]['creators']:
            if k not in all_creators.keys():
                all_creators[k] = {}
                all_creators[k]['num'] = 1
            else:
                all_creators[k]['num'] += 1
    else:
        print("article ", str(key), "has no creators")

x_sorted = sorted(all_creators.items(), key=lambda x: x[1]['num'], reverse=True)
x_sorted = x_sorted[:50]
oft_creators = []
for x in x_sorted:
    oft_creators.append(x[0])

for key in articlesData.keys():
    articlesData[key]['author-labels'] = [0] * len(oft_creators)
    for creator in articlesData[key]['creators']:
        if creator in oft_creators:
            articlesData[key]['author-labels'][  oft_creators.index(creator)  ] = 1

################  BEGIN of Calculation of  word frequencies  in standard english
d = {}
with open(work_dir + "word_frequency_common.txt") as f:
    for line in f:
       (key, val) = line.split()
       d[key] = int(val)

total = 0
for key in d.keys():
    total += d[key]

for key in d.keys():
    d[key] = d[key] / total

f.close()
################  END of Calculation of  word frequencies  in standard english
################  BEGIN of Calculation of  word frequencies  in articles content
f = {}
for key in articlesData.keys():
    curr = re.split('[^a-zA-Z]', articlesData[key]['content'].lower())
    for cu in curr:
        if cu not in f.keys():
            f[cu] = 1
        else:
            f[cu] += 1

del f['']
total = 0
for key in f.keys():
    total += f[key]

for key in f.keys():
    f[key] = f[key] / total

################  END of Calculation of  word frequencies  in articles content
################  BEGIN of    Let's find which words are  ML-specific
ml = []
for key in f.keys():
    if f[key] > 2e-5:
        if key not in d.keys():
            ml.append(key)
        else:
            if f[key] / d[key] > 30:
                ml.append(key)

ml = ['github']

################  END of    Let's find which words are  ML-specific
for key in articlesData.keys():
    articlesData[key]['content-labels'] = [0] * len(ml)
    curr = re.split('[^a-z\-A-Z]', articlesData[key]['content'].lower())
    for cu in curr:
        if cu in ml:
            articlesData[key]['content-labels'][  ml.index(cu)  ] = 1

eqA = [];   eqC = [];   i=0;
for key in articlesData.keys():
    eqA.append(     articlesData[key]['subject-labels'] + articlesData[key]['author-labels'] + articlesData[key]['content-labels']  + [1]   )
    eqC.append(     articlesData[key]['label']     )

#for i in range(len(eqC)):
#    eqC[i] = eqC[i] > 1

save_obj({'eqA': eqA, 'eqC': eqC}, 'articles_data.pkl')

p = np.random.permutation(len(eqC))
eqA = np.array(eqA);    eqC = np.array(eqC);
eqA = eqA[p];           eqC = eqC[p];

ans = np.linalg.lstsq(eqA[0:2000], eqC[0:2000], rcond=None)

print("oft_creators = ", oft_creators)
print("ml = ", ml)
print("len(ml) = ", len(ml))
print("len(oft_creators) = ", len(oft_creators))

err = 0
for i in range(2000, len(eqC)):
    err += (np.dot(eqA[i], ans[0]) - eqC[i])**2

print("ТЕСТ -- Средний квадрат ошибки на фитировании = ", err / (len(eqC) - 2000) )
err = 0
for i in range(2000, len(eqC)):
    err += (np.mean(eqC[2000:]) - eqC[i])**2

print("ТЕСТ -- Средний квадрат ошибки бейслайна среднего значения (вычисл по TEST) = ", err / (len(eqC) - 2000) )

err = 0
for i in range(2000, len(eqC)):
    err += (np.mean(eqC[:2000]) - eqC[i])**2

print("ТЕСТ -- Средний квадрат ошибки бейслайна среднего значения (вычисл по TRAIN) = ", err / (len(eqC) - 2000) )

err = 0
for i in range(2000):
    err += (np.dot(eqA[i], ans[0]) - eqC[i])**2

print("TRAIN -- Средний квадрат ошибки на фитировании = ", err/2000 )
err = 0
for i in range(2000):
    err += (np.mean(eqC[:2000]) - eqC[i])**2

print("TRAIN -- Средний квадрат ошибки бейслайна среднего значения = ", err/2000 )
print(ans)


save_obj(articlesData, work_dir + 'articlesData.pkl')

## fW.close()

