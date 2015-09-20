__author__ = 'raghu'

import math

#----------------Opening the train file
with open('train') as train_file:
    #-------------Initializing the total_count,spam count and ham count
    total_count = 0
    spam_count = 0
    ham_count = 0
    #---------Initializing dict to store spam words and ham words abd the count of each of those words
    spam_words_count = {}
    ham_words_count = {}
    spam_word_count = 0
    ham_word_count = 0
    total_word_count = 0
    #----------------checking if the email id is spam or ham and adding the words respectively in the dict and increasing the words count and individual word count
    for line in train_file:
        tokens = line.split(" ")
        total_count += 1
        for word, word_count in zip(tokens[2::2],tokens[3::2]):
            total_word_count += 1
        if tokens[1] == 'spam':
            spam_count += 1
            for word, word_count in zip(tokens[2::2],tokens[3::2]):
                spam_word_count += 1
                if word in spam_words_count:
                    spam_words_count[word] += int(word_count)
                else:
                    spam_words_count[word] = 0
                # print(word,int(word_count))
        else:
            for word, word_count in zip(tokens[2::2],tokens[3::2]):
                ham_word_count += 1
                if word in ham_words_count:
                    ham_words_count[word] += int(word_count)
                else:
                    ham_words_count[word] = 0
                # print(word,int(word_count))

    #---------------total probability of all spam words and ham words
    spam_prob = float(spam_count)/total_count
    ham_count = total_count - spam_count
    ham_prob = 1 - spam_prob

    print(spam_prob, ham_prob)
    #
    # print(spam_words_count)
    #
    # print(spam_word_count)
    # print(ham_word_count + spam_word_count)
    # print(total_word_count)

    #----------probability of each spam and ham word occuring in the email
    ham_words_prob = {}
    for key,value in ham_words_count.iteritems():
        ham_words_prob[key] = float(value)/ham_word_count

    spam_words_prob = {}
    spamcity_word = {}
    spamcity_word_new = {}
    for word,count in spam_words_count.iteritems():
        spam_words_prob[word] = float(count)/spam_word_count
        spamcity_word[word] = spam_words_prob[word] * spam_prob / (spam_words_prob[word] * spam_prob + ham_words_prob[word] * ham_prob)
        # spamcity_word_new[word] = (3 * spam_prob + float(count) * spamcity_word[word])/(3 + count)
    print(spam_words_prob)
    print(spamcity_word)

    # ham_words_prob = {}
    # for key,value in ham_words_count.iteritems():
    #     ham_words_prob[key] = float(value)/ham_word_count
    # print(ham_words_prob)


#----------finding the spam and ham in the test file
with open('test','r') as test_file:
    # try:
    spam_correct = 0
    actual_spam = 0
    actual_ham = 0
    ham_correct = 0
    mail_count = 0
    for line in test_file:
        mail_count += 1
        tokens = line.split(" ")
        log_expr = 0
        for word, word_count in zip(tokens[2::2],tokens[3::2]):
            if word in spamcity_word and spamcity_word[word] > 0:
                log_expr += (math.log(1 - spamcity_word[word]) - math.log(spamcity_word[word]))
            else:
                pass
            # if word in spamcity_word_new and spamcity_word_new[word] > 0:
            #     log_expr += (math.log(1 - spamcity_word_new[word]) - math.log(spamcity_word_new[word]))
            # else:
            #     log_expr += (math.log(1 - spam_prob) - math.log(spam_prob))

        spam_prob_mail = 1/(1 + math.e ** log_expr)
        #------------if the probability of spam is greater than 0.5 categorize it as spam else ham
        #------------if test answer matches our answer increase count of correctly recognized spam or ham respectively
        if tokens[1] == 'spam':
            actual_spam += 1
        elif tokens[1] == 'ham':
            actual_ham += 1

        if spam_prob_mail >= 0.5 and tokens[1] == 'spam':
            spam_correct += 1

        if spam_prob_mail < 0.5 and tokens[1] == 'ham':
            ham_correct += 1

        print(spam_prob_mail)
    print(spam_correct + ham_correct)
    print(actual_spam,actual_ham)
    print('spam correct' ,spam_correct ,'ham correct', ham_correct, "out of", mail_count)
    # except:
    #     print("exception occured:")