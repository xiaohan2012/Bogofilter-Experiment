import os
trn_samp_ind_fp='../trec05p-1/spam25/'
with open('stat.dat','w') as stat_f:
    os.chdir(trn_samp_ind_fp)
    counter=0
    with open('index','r') as f:
        for l in f.readlines():
            counter+=1
            is_spam = '-s' if l.split()[0]=='spam' else '-n'
            mail_path = l.split()[1]

            cmd = 'bogofilter -M %s -I %s' %(is_spam,mail_path)
            os.system(cmd)

            if counter >10000:
                break

            if counter % 100 == 0:
                out = os.popen('du ~/.bogofilter/wordlist.db')
                stat_f.write('%s,%s\n' %(counter,out.readline().split()[0]))
