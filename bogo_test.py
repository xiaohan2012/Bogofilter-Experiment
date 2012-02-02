import os
import random

category='full'


trn_samp_ind_fp='../trec05p-1/%s/' %(category)

#test result code
C_TP=2
C_TN=1
C_US=0
C_FN=-1
C_FP=-2
DEBUG_FLAG = True 
def debug(msg='this is debug info'):
    if DEBUG_FLAG: 
        try:
            print str(msg)
        except:
            print '-----Exception occurred------'

def train(is_spam,mail_path,wl_path='/home/xiaohan/.bogofilter'):
    cmd = 'bogofilter -M %s -I %s -d %s' %(is_spam,mail_path,wl_path)
    debug(cmd)
    os.system(cmd)

def get_test_result(is_spam,mail_path,wl_path='/home/xiaohan/.bogofilter'):
    """if guess right,return True;then return False"""
    cmd='bogofilter -t -d %s < %s' %(wl_path,mail_path)
    debug(cmd)
    is_spam = 'S' if is_spam == 'spam' else 'H'
    guess_res = os.popen(cmd).read().split()[0]

    debug('guess %s,actual %s' %(guess_res,is_spam))
    if guess_res == 'U':#unsure
        debug('unsure 0')
        debug()
        return C_US
    else:
        if is_spam == 'S' and is_spam == guess_res:#true positive
            debug('true positive,2')
            return C_TP 
        elif is_spam == 'H' and is_spam == guess_res:#true negative 
            debug('true negative,1')
            return C_TN 
        elif is_spam == 'H' and is_spam != guess_res:#false positive
            debug('false positive,2')
            return C_FP
        elif is_spam == 'S' and is_spam != guess_res:#false negative
            debug('false negative, -1')
            return C_FN
        else:
            raise
if os.path.exists('/home/xiaohan/.bogofilter/wordlist.db'):
    os.remove('/home/xiaohan/.bogofilter/wordlist.db')

with open('crit_stat.dat','w') as stat_f:
    os.chdir(trn_samp_ind_fp)#change dir
    
    #test config
    trn_max_smp_cnt = 10000
    trn_intvl = 100
    iter_cnt = trn_max_smp_cnt / trn_intvl
    tst_samp_cnt_ratio = 0.5
    counter = 0
    for intvl_ind in xrange(1,iter_cnt+1):
        total_set = set(open('index').readlines())
        debug('\ntotal set count %d' %(len(total_set)))

        trn_cnt = intvl_ind * trn_intvl#get train sample count
        trn_set = random.sample(total_set,trn_cnt)#get train set
        total_set -= set(trn_set)#remove train set from total set

        debug('total set count %d' %(len(total_set)))
        debug('train set count %d' %(len(trn_set)))

        tst_cnt = int(trn_cnt * tst_samp_cnt_ratio)#get test sample count
        tst_set = random.sample(total_set,tst_cnt)#get test set
        total_set -= set(tst_set)#remove test set from total set

        debug('total set count %d' %(len(total_set)))
        debug('test set count %d' %(len(tst_set)))

        #start training
        for trn_samp in trn_set:
            is_spam = '-s' if trn_samp.split()[0]=='spam' else '-n'
            mail_path = trn_samp.split()[1]
            train(is_spam,mail_path,wl_path='/home/xiaohan/.bogofilter/%d_of_%d' %(trn_cnt,trn_max_smp_cnt))

        #start testing
        _dict = {}
        _dict[C_TP] = 0
        _dict[C_TN] = 0
        _dict[C_FN] = 0
        _dict[C_FP] = 0
        _dict[C_US] = 0

        for tst_samp in tst_set:
            is_spam,mail_path = tst_samp.split()
            _dict[get_test_result(is_spam,mail_path,wl_path='/home/xiaohan/.bogofilter/%d_of_%d' %(trn_cnt,trn_max_smp_cnt))] += 1
        
        debug(_dict)

        stat_f.write('%d'.rjust(10) %trn_cnt)
        for code in range(2,-3,-1):
            stat_f.write('%d'.rjust(10) %_dict[code])
        
        stat_f.write('\n')
           
