from math import log,ceil
import argparse
import csv

def classifier(data,spam_words,ham_words,total_words,prob_ham_mails,prob_spam_mails,total_spam_count,total_ham_count,alpha=1):
    res_prob_spam = 0.0
    res_prob_ham = 0.0
    for i in xrange(2,len(data),2):
        # if data[i] in spam_words:

        #calculating the conditional probabilty according to the formula mentioned in the report for the spam
        res_prob_spam += log((spam_words.get(data[i],0) + alpha)/float(total_spam_count + alpha*total_words))
        # print res_prob_spam
        # else:
        #     res_prob_spam *= 1.0
        # if data[i] in ham_words:

        #calculating the conditional probability according to the formula mentioned in the report for the ham mails
        res_prob_ham += log((ham_words.get(data[i],0) + alpha)/float(total_ham_count + alpha*total_words))
        # else:
        #     res_prob_ham *= 1.0

    #posterior probabiity of the ham mails
    res_prob_ham += log(prob_ham_mails)
    #posterior probability of the spam mails
    res_prob_spam += log(prob_spam_mails)
    # print(res_prob_ham)
    # print(res_prob_spam)
    return res_prob_spam >= res_prob_ham

def train(train_data,test_data,output_name,alpha=1):
    count = {}
    count['ham'] = 0
    count['spam'] = 0
    spam_words = {}
    total_spam_count = 0
    total_ham_count = 0
    ham_words = {}
    prob_spam = {}
    prob_ham = {}
    tot_mails = 0
    unique_words = []
    with open(train_data,'r') as input:
        for line in input:
            #counts the total number of emails
            tot_mails += 1
            data = line.split(' ')
            #counts the number of spam emails or ham emails
            count[data[1]] += 1
            if data[1] == 'spam':
                for i in xrange(2,len(data),2):
                    #counts the number of unique_words in all the training set
                    if data[i] not in unique_words:
                        unique_words.append(data[i])
                    #counts the number of times a word occurs in the spam mails only
                    spam_words[data[i]] = spam_words.get(data[i],0) + int(data[i+1])
                    #counts the total number of words in the spam email only
                    total_spam_count += int(data[i+1])
            else:
                for i in xrange(2,len(data),2):
                    #counts the number of unique words in the entire training data
                    if data[i] not in unique_words:
                        unique_words.append(data[i])
                    #counts the number of times a word occurs in ham mails only
                    ham_words[data[i]] = ham_words.get(data[i],0) + int(data[i+1])
                    #counts the total number of words in ham mails only
                    total_ham_count += int(data[i+1])

    total_words = len(unique_words)
    # print total_words, (len(spam_words) + len(ham_words))
    # print(total_words)

    #probability that the email is a spam
    prob_spam_mails = count['spam']/float(tot_mails)
    #probability that the email is a ham
    prob_ham_mails = count['ham']/float(tot_mails)
    # print(prob_ham_mails)
    # print(prob_spam_mails)

    true_positive = 0
    true_negative = 0
    false_negative = 0
    false_positive = 0
    output = open(output_name+".csv",'w')
    pred_output = csv.writer(output,dialect="excel",delimiter="\t",quoting=csv.QUOTE_ALL)
    row = []
    row.append("ID")
    row.append("spam/ham")
    pred_output.writerow(row)
    with open(test_data,'r') as test:
        for line in test:
            row = []
            data = line.split(' ')
            res = classifier(data,spam_words,ham_words,total_words,prob_ham_mails,prob_spam_mails,total_spam_count,total_ham_count,alpha)
            if res and data[1]=='spam':
                true_positive += 1
            if not res and data[1] == 'ham':
                true_negative += 1
            if res and data[1]=='ham':
                false_positive += 1
            if not res and data[1] == 'spam':
                false_negative += 1
            row.append(data[0])
            if res:
                row.append("Spam")
            else:
                row.append("Ham")
            pred_output.writerow(row)
    # print true_positive+false_positive
    total = true_negative + true_positive + false_negative + false_positive
    accuracy = (true_negative + true_positive)/float(total)
    precision = (true_positive)/float(true_positive + false_positive)
    recall = (true_positive)/float(true_positive + false_negative)
    f1_score = 2*precision*recall/float(precision + recall)
    print "Accuracy : "+str(ceil(accuracy*100)), "F1_score: "+str(round(f1_score*100,2))
    # print (pred_spam)/float(actual_spam)

    # print prob_spam_mails
    # print prob_ham_mails
    # print prob_spam
    # print prob_ham

def parse():
    parser = argparse.ArgumentParser(add_help=False, description="Spam Email filtering tool")
    parser.add_argument("-f1", help="Enter the file name of your train dataset")
    parser.add_argument("-f2", help="Enter the file name of your test dataset")
    parser.add_argument("-o", help="Enter the output file name for the predicted result")
    parser.add_argument("alpha", nargs="*", action="store", help="Enter the smoothig factor to increase the accuracy any number between 1 to 150")
    parser.add_argument('-h','-?','--h','-help','--help',action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.h:
    	parser.print_help()
    	sys.exit()
    return args.f1, args.f2, args.o, args.alpha

train_data, test_data, output_name, alpha = parse()
if len(alpha) == 0:
    train(train_data,test_data,output_name)
else:
    train(train_data,test_data,output_name,float(alpha[0]))
