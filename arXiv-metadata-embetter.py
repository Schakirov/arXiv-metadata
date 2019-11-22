## When month changes,  change these two lines:    (no other changes needed):
curr_month = '1911'
prev_month = '1910'

keywords = ['state-of-the-art', 'state of the art', 'github', 'source code', 'alphazero']
bad_keywords = ['medic', 'clinic', 'patient', 'diseas', 'disorder', 'random forest', 'k-mean', 'svm', 'kernel', 'bandit', 'boltzmann', 
                'magnetic resonance', 'theor', 'gaussi', 'mammogra', 'diagnos', 'patholog', 'adversarial att', 
                'bayes', 'recommendat', 'named entity', 'anatomy', 'lidar', 'high-energy', 're-identification']
lp_keywords = {'speech recognition': -0.3, 'speaker recognition': -0.7, 'speech separation': -0.4, 'segmentation': -0.25, 'reverberat': -0.2, 'point cloud': -0.2, 'knn': -0.2, 
               'regression': -0.2, 'Object Detection': -0.3, 'black-box attack': -0.4, 'nearest neighbo': -0.4, 'SQL': -0.5, 'emotion': -0.4, 
               'android': -0.2, 'malware': -0.3, 'molecule': -0.25, 'knowledge graph': -0.15, 'fake news': -0.5, 'super-resolution': -0.5, 'outlier': -0.5,
               'tracker': -0.25, ' face ': -0.3, ' facial ': -0.3, 'clustering': -0.5, 'anomal': -0.25, 'parsing': -0.4, 'parser': -0.3,
               'e-commerce': -0.5, 'speech enhancement': -0.5, 'fmri': -0.4, 'post-editing': -0.4, 'reservoir': -0.3, 'voice separat': -0.4, ' eeg ': -0.5, ' mri ': -0.4, 
               'bengali': -0.4, 'hindi': -0.4, 'japanese': -0.4, 'vietnamese': -0.4, 'chinese': -0.2, 'restaurant': -0.5, 
               'image denoising': -0.3, 'economic': -0.4, ' POS ': -0.5,  'tracking': -0.35, ' NER ': -0.5, 'sentiment': -0.5, 
               'tomography': -0.4, 'hmdb-51': -0.3, 'interpret': -0.2, 'authorship': -0.2, ' mobile ': -0.15, 'hieroglyph': -0.4, 'weather': -0.3, 'market': - 0.3, 
               ' music ': -0.3, 'ecg': -0.5, 'histolog': -0.5, 'fpga': -0.25, 'federated': -0.2, ' nba ': -0.8, 'climate': -0.2, 'style': -0.2, 
               'cancer': -0.2, 'genetic': -0.2, 'lightweight': -0.2, 'surveillance': -0.4, 'summarization': -0.3, 'privacy': -0.5, 'private': -0.3, 'low-resource': -0.25, 
               'pedestrian': -0.5, 'financ': -0.4, 'competitive': -0.15, 'spoof': -0.3, 
               'customer': -0.6}
hp_keywords = {'reinforcement learning': 0.25, 'curriculum learning': 0.1, 'general intelligence': 0.25, 'general artificial' : 0.25, 'general ai': 0.25,
               'lifelong': 0.2, 'MuJoCo': 0.1, 'hierarchical': 0.2, 'zero-shot': 0.2, 'one-shot': 0.15, 'few-shot': 0.2, 
               'sparse reward': 0.3, 'publicly available': 0.3, 'architecture search': 0.3, 'sample efficien': 0.4, 
               'google': 0.3, 'brain': 0.25, 'curiosity': 0.2, 'human-level': 0.3, ' bert ':0.25, ' gpt': 0.25, 
               'video generation': 0.3, 'http': 0.1, 'russia': 0.3, 'outperform': 0.2, 
               'real-world': 0.15, 'real world': 0.15}
good_authors = ['Bengio, Yoshua', 'Quoc', 'Vinyals', 'Salakhutdinov', 'Freitas', 'Kyunghyun',
                  'Hinton', 'Schmidhuber', 'Ng, Andr', 'LeCun', 'Hassabis', 'Goodfellow', 'Lee, Honglak', 
                  'Oord, A', 'Pascanu, R', 'Lillicrap', 'Nøkland', 'Sutskever', 'Yuille', 'Zisserman, A', 'Weston, Jason', 
                  'Sukhbaatar', 'Joulin, A', 'Ranzato, Ma', 'Simonyan, Ka', 'Malik, J', 'Fei-Fei, Li', 'Zaremba, W', 'Levine, Sergey']
also_good_authors = ['']
good_subjects = ['cs:CL', 'cs:NE', 'cs:RO']
subjects_to_follow = {'Computer Science - Robotics' : 'cs:RO', 'Computer Science - Sound' : 'cs:SD', 
                      'Computer Science - Artificial Intelligence' : 'cs:AI', 
                      'Computer Science - Neural and Evolutionary Computing' : 'cs:NE', 
                      'Statistics - Machine Learning' : 'stat:ML', 'Computer Science - Machine Learning' : 'cs:ML', 
                      'Computer Science - Emerging Technologies' : 'cs:ET', 
                      'Computer Science - Computation and Language' : 'cs:CL', 
                      'Computer Science - Computer Vision and Pattern Recognition' : 'cs:CV'}                  
f = open("arXiv-articles.xml", "r")
fW = open("arXiv-articles.html", "w+")
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
    creators = ''
    while i1 > -1:
        i1 = b.find('<dc:creator>', i2)
        i2 = b.find('</dc:creator>', i1)
        if i2 > -1:
            creator = b[i1+12:i2]
            ## fW.write(creator + ", &nbsp&nbsp")
            creators += ", " + creator
    ## fW.write("</br>\n")
    for good_author in good_authors:
        if creators.lower().find(good_author.lower()) > -1:
            # gives false positives on many "...ng A..."  like "Cheung Ang"
            #if creators.find(good_author) > -1:
            red_idx = creators.lower().find(good_author.lower())
            creators = creators[:red_idx] + '<font color="red">' + creators[red_idx: red_idx + len(good_author)] \
            + '</font>' + creators[red_idx + len(good_author) :]
            #creators = creators.replace(good_author, '<font color="red">' + good_author + '</font>')
            articles[identifier]['if-good'] += 10
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
    for keyword in lp_keywords.keys():
        if description.lower().find(keyword.lower()) > -1:
            red_idx = description.lower().find(keyword.lower())
            lp_color = hex(    min(190, int(abs(lp_keywords[keyword]) * 1000))    )[2:]   ## 0.5 as ~255
            lp_color = '#' + lp_color + '00' + lp_color
            description = description[:red_idx] + '<font color="' + lp_color + '">' + description[red_idx: red_idx + len(keyword)] \
            + '</font>' + description[red_idx + len(keyword) :]
            articles[identifier]['if-good'] += lp_keywords[keyword]
    for keyword in hp_keywords.keys():
        if description.lower().find(keyword.lower()) > -1:
            red_idx = description.lower().find(keyword.lower())
            hp_color = hex(    min(190, int(abs(hp_keywords[keyword]) * 1000))    )[2:]   ## 0.5 as ~255
            hp_color = '#00' + hp_color + '00'
            description = description[:red_idx] + '<font color="' + hp_color + '">' + description[red_idx: red_idx + len(keyword)] \
            + '</font>' + description[red_idx + len(keyword) :]
            articles[identifier]['if-good'] += hp_keywords[keyword]
    ## fW.write(description + "</br></br>\n\n")
    articles[identifier]['description'] = description
    articles[identifier]['if-good'] -= 0.0001 * len(description)

nummer = 1
for currID in sorted(articles, key=lambda x: (articles[x]['if-good']), reverse=True):
    if (articles[currID]['subjects-to-follow'] == 1) and ((currID.find(prev_month) > -1) or (currID.find(curr_month) > -1)):
        fW.write("<a href='http://arxiv.org/pdf/" + currID + ".pdf'>" + currID + "</a> &nbsp&nbsp ")
        fW.write(articles[currID]['subject'])
        fW.write(" &nbsp&nbsp " + "{:.4f}".format(articles[currID]['if-good']) + "баллов, №" + str(nummer) + "</br>\n")
        fW.write("<b>" + articles[currID]['title'] + "</b></br>\n")
        fW.write("Authors: " + articles[currID]['creators'] + "</br>\n")
        fW.write(articles[currID]['description'] + "</br></br>\n\n")
        nummer += 1

f.close()
fW.close()

