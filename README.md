Algorithm for the spam filter:    
1. Go through each of the mails in the train dataset and accordingly count the frequencies  of each word and store the count in either the spam_words dictionary or the ham_words  dictionary according to the category the mail belongs to, as given in the train dataset.
2. At the same time, maintain the count of the total number of words that have occurred in  all the spam mails of the train data and also all the ham mails of the training data. In our  code we represent them as the total_spam_count and total_ham_count respectively. 
3. Maintain the total number of emails present in the entire dataset. We indicate it as the  tot_mails. 
4. Calculate the probability of the mail being spam and the mail being ham. These are called  as the prior probabilities or the class probabilities.
5. When we give a new mail to the classifier function, it classifies the mail as either spam or  ham. The function takes the class probabilities, the spam_word dictionary, the ham_word  dictionary and the other parameters.
6. When then classifier receives the new set of features from the new mail, it calculates the  conditional probability of that word belonging to the spam mail or the ham mail  according to the formula:       P(spam/[word1, word2, word3, …]) = P(word1/spam)*P(word2/spam)*….       P(ham/[word1, word2, word3, …]) = P(word1/ham)*P(word2/ham)*…..       P(word1/spam) = (# word1 occurs in spam) / (# all words present in spam)       P(word1/ham) = (# word1 occurs in ham) / (# all words present in ham) 
7.  Now calculate the posterior probability for both the ham and the spam which is given by  the following formula  a. posterior probability = ((conditional Probability)*(prior probability) / (evidence))       
8.  If the posterior probability of spam >= ham then the email is classified as spam else it is  classified as ham.        


Results :    With the above algorithm we could achieve an accuracy of around 89% 
This accuracy can further be improved by using an additive smoothing factor called alpha. This  is because if a new word that is not present in out train data is encountered then the above  algorithm alone won't be able to handle it as it would return a zero probability thereby making  the entire conditional probability zero and so to avoid that we add a smoothing factor and so the  new conditional probability becomes  P(word1/spam) = (# word1 occurs in spam + alpha) / (# all words present in spam +   alpha* # of unique words in the  training set)    This increased the accuracy to 91% to 92% depending on the range of alpha we consider  If alpha is 1 then accuracy is 91%  If alpha is 100 to 150 then accuracy is 92 and beyond 150 it again falls down to 91% or lower.  If alpha < 1 then accuracy falls to 91% again.
The best parameter to try would be from 100 to 150 as the alpha.
Note: Place all the files in the same folder before running including the train and test file. 
Syntax to run the code:  python q2_classifier.py -f1 train -f2 test -o output 150   
here 150 is the value of alpha. 
If it is not mentioned then by default the algorithm will take it as  1. If you need to give any other value you can give it in place of 150 (the arguement next to  output).  
Accuracy of the algorithm has been calculated using the formula:  Accuracy = (true_positive + true_negative)/(false_positive + false_negative +  true_positive +  true_negative)
