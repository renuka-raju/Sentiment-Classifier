import sys
from math import log
def count(file):
    outfile=open('nbmodel.txt','w',encoding='utf-8')
    punct = '`!~;-:\'\\/"?><,.|{}()[]'
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that','these',
                 'those', 'am', 'is', 'are', 'was', 'were', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'here', 'there',
                 'when', 'where', 'why', 'how', 's', 't', 've']
    whitespace = ' ' * len(punct)
    table = str.maketrans(punct, whitespace)
    trainfile = open(file, newline='', encoding='utf-8')
    lines = trainfile.readlines()
    wordcount = {}
    tagcount = {}
    tagwordcount = {}
    vocab = ''
    for line in lines:
        bag = line.split(' ')
        tag1 = bag[1]
        tag2 = bag[2]
        if tagcount.get(tag1):
            tagcount[tag1] += 1
        else:
            tagcount[tag1] = 1
        if tagcount.get(tag2):
            tagcount[tag2] += 1
        else:
            tagcount[tag2] = 1

        if tag1 not in tagwordcount:
            tagwordcount[tag1] = 0
        if tag2 not in tagwordcount:
            tagwordcount[tag2]=0

        i = 3
        while i < len(bag):
            w = bag[i].lower().strip()
            w = w.replace("n't", " not")
            w = w.translate(table)
            words = w.split(' ')
            words = list(filter(None, words))
            for word in words:
                if word not in stopwords:
                    tagwordcount[tag1]+=1
                    tagwordcount[tag2]+=1
                    if word not in vocab:
                        vocab+=word+' '
                    tagword1=tag1+' '+word
                    tagword2=tag2+' '+word
                    if wordcount.get(tagword1):
                        wordcount[tagword1]+=1
                    else:
                        wordcount[tagword1]=1

                    if wordcount.get(tagword2):
                        wordcount[tagword2]+=1
                    else:
                        wordcount[tagword2]=1
            i+=1

    vocab.strip()
    vocabsize = len(vocab.split(' '))
    outfile.write(str(vocabsize))
    outfile.write('\n')
    return vocabsize,wordcount,tagcount,tagwordcount,len(lines),outfile

def probability(vocabsize,wordcount,tagcount,tagwordcount,total,outfile):
    prior={}
    for tag,count in tagcount.items():
        prior[tag]=(count/total)
        outfile.write(tag+':'+str(prior[tag]))
        outfile.write('\n')

    outfile.write('\n')
    wordtagprob={}
    sorted_wordcount = sorted(wordcount.items(), key=lambda x: (x[0],x[1]))
    for key,count in sorted_wordcount:
        wordtag=key.rsplit(' ',1)[0]
        wordtagprob[key]=log((count+1)/(tagwordcount[wordtag]+vocabsize))
        outfile.write(key+':'+str(wordtagprob[key]))
        outfile.write('\n')

    outfile.write('\n')
    for tag,wordcount in tagwordcount.items():
        outfile.write(tag+':'+str(wordcount))
        outfile.write('\n')

def main(arg):
    vocabsize, wordcount, tagcount, tagwordcount, total, outfile=count(arg)
    probability(vocabsize,wordcount,tagcount,tagwordcount,total,outfile)

if __name__=="__main__":
    #print(time.time())
    main(sys.argv[1])
