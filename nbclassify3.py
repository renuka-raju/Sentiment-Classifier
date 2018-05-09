from math import log
import sys
def main(file):
    outfile=open('nboutput.txt','w',encoding='utf-8')
    punct = '`!~;-:\'\\/"?><,.|{}()[]'
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'here', 'there',
                 'when', 'where', 'why', 'how', 's', 't', 've']
    whitespace = ' ' * len(punct)
    table = str.maketrans(punct, whitespace)
    devtextfile = open(file, encoding='utf-8')
    lines = devtextfile.readlines()
    modelfile=open('nbmodel.txt','r',encoding='utf-8')
    vocabsize=modelfile.readline()
    modelline=modelfile.readline()
    tags=[]
    prior={}

    while modelline != '\n':
        tagvalue = modelline.split(':')
        tag = tagvalue[0]
        value = tagvalue[1].strip()
        tags.append(tag)
        prior[tag] = float(value)
        modelline = modelfile.readline()

    modelline=modelfile.readline()
    wordtagprob={}
    while modelline !='\n':
        wordtag = modelline.split(':')[0]
        value = modelline.split(':')[1].strip()
        wordtagprob[wordtag]=float(value)
        modelline = modelfile.readline()

    modelline = modelfile.readline()
    tagwordcount = {}
    while modelline != '':
        wordtag = modelline.split(':')[0]
        value = modelline.split(':')[1]
        tagwordcount[wordtag] = float(value)
        modelline = modelfile.readline()

    for line in lines:
        bag = line.split(' ')
        i=1
        words=[]
        while i < len(bag):
            w = bag[i].lower().strip()
            w = w.replace("n't", " not")
            w = w.translate(table)
            tokens = w.split(' ')
            words = words+list(filter(None, tokens))
            i+=1
        #print(words)
        trueorfalse = ''
        maxprob = -float('inf')
        for tag in ['True','Fake']:
            joint = prior[tag]
            for word in words:
                if word not in stopwords:
                    if tag + ' ' + word in wordtagprob.keys():
                        prob = wordtagprob[tag + ' ' + word]
                    else:
                        prob = log(1 / (tagwordcount[tag] + int(vocabsize)))
                    joint = joint + prob
                #print(tag + ' ' + str(joint))
            maxprob = max(maxprob, joint)
            if maxprob == joint:
                trueorfalse = tag

        posOrNeg = ''
        maxprob = -float('inf')
        for tag in ['Neg','Pos']:
            joint = prior[tag]
            for word in words:
                if word not in stopwords:
                    if tag + ' ' + word in wordtagprob.keys():
                        prob = wordtagprob[tag + ' ' + word]
                    else:
                        prob = log(1 / (tagwordcount[tag] + int(vocabsize)))
                    joint = joint + prob
            maxprob = max(maxprob, joint)
            if maxprob == joint:
                posOrNeg = tag

        outfile.write(bag[0] + ' ' + trueorfalse+ ' ' +posOrNeg)
        outfile.write('\n')

if __name__=="__main__":
    #print(time.time())
    main(sys.argv[1])
