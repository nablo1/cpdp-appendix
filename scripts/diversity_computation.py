import csv
import random
import pandas as pd
import glob
import os

# ORDER of projects bb, bs, mb, ms, lb, ls, ub, us
projects = [["activiti_BB.csv","stroom_BB.csv","jbpm_BB.csv","facebooksdk_BB.csv","spark_BB.csv"],
            ["modernmt_BS.csv","seedstack_BS.csv","tessera_BS.csv","qlexpress_BS.csv","sudachi_BS.csv"],
            ["antennapod_MB.csv","osmdroid_MB.csv","zxing_MB.csv","exoplayer_MB.csv","mindustry_MB.csv"],
            ["vinyl_MS.csv","phonograph_MS.csv","javacv_MS.csv","gsyvideoplayer_MS.csv","metadata_MS.csv"],
            ["rxjava_LB.csv","blaze_LB.csv","flowable_LB.csv","daqeclipse_LB.csv","ebean_LB.csv"],
            ["googleauth_LS.csv","jmock_LS.csv","yue_LS.csv","thumbnailator_LS.csv","springdock_ls.csv"],
            ["jabref_UB.csv","commons_UB.csv","k9_UB.csv","talon_UB.csv","sentinel_UB.csv"],
            ["dependencycheck_US.csv","agrona_US.csv","snowflake_US.csv","androidmaps_US.csv","pipeline_US.csv"]]

for x in range (8):
    random.shuffle(projects[x])

key_dict = {"big-business":0, "small-business":1, "big-multimedia": 2, "small-multimedia":3, "big-library":4, "small-library":5, "big-utility":6, "small-utility":7}
csv_dict = {"BB":0, "SB":1, "BM": 2, "SM":3, "BL":4, "SL":5, "BU":6, "SU":7}

domains = ['business','multimedia','library','utility']
sizes = ['big','small']

combinations = [[["big","business"],["big","utility"],["small","multimedia"],["small","library"]],
                [["big","business"],["big","multimedia"],["small","library"],["small","utility"]],
                [["big","business"],["big","library"],["small","multimedia"],["small","utility"]],
                [["big","utility"],["big","multimedia"],["small","business"],["small","library"]],
                [["big","utility"],["big","library"],["small","multimedia"],["small","business"]],
                [["big","library"],["big","multimedia"],["small","business"],["small","utility"]]]

w, h = 4, 8
dsets = [[0 for x in range(w)] for y in range(h)]

def choose(bucket):
    ret = bucket.pop(bucket.index(random.choice(bucket)))
    return ret

def flatten(t):
    return [item for sublist in t for item in sublist]

def place(bucket, list_index, project_index):
    dsets[list_index][project_index] = choose(bucket)


testing = [choose(projects[0]),choose(projects[1]),choose(projects[2]),choose(projects[3]),choose(projects[4]),choose(projects[5]),choose(projects[6]),choose(projects[7])]

print("Testing set includes:", testing)
print("---- TESTING SET SELECTED ----")

combination_list = []

while len(combinations) < 8:
    
    curr_combination = []
    while len(curr_combination) < 4:
        curr_dom = random.choice(domains)
        curr_sz = random.choice(sizes)

        if [curr_sz,curr_dom] not in curr_combination and flatten(curr_combination).count(curr_sz) != 2 and flatten(combinations).count([curr_sz, curr_dom]) < 4:
            curr_combination.append([curr_sz,curr_dom])

    if curr_combination not in combinations:
        combinations.append(curr_combination)

for c in combinations:
    print(c)

print("---- combination_list SELECTED ---- ")

ticker = 0

for i in combinations:
    index = 0

    for x in i:
        size = x[0]
        domain = x[1]
        key = size + "-" + domain
        place(projects[key_dict[key]], ticker, index)
        index += 1
    
    ticker += 1

for p in dsets:
    print(p)

print("---- PLACED PROJECTS IN SETS ----")

os.chdir('cpdp-appendix/data')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

for x in range(8):
    print("diverse-",x, end="-")
    concatfiles = []
    for f in all_filenames:
        #combine all files in the list

        if f in dsets[x]:
            print(f, end=";")
            concatfiles.append(f)
            
    combined_csv = pd.concat([pd.read_csv(c) for c in concatfiles])
    #export to csv        
    combined_csv.to_csv("../results/diverse"+str(x+1)+".csv", index=False, encoding='utf-8-sig')        
    print()

# ORDER of projects bb, bs, mb, ms, lb, ls, ub, us
projects = [["activiti_BB.csv","stroom_BB.csv","jbpm_BB.csv","facebooksdk_BB.csv","spark_BB.csv"],
            ["modernmt_BS.csv","seedstack_BS.csv","tessera_BS.csv","qlexpress_BS.csv","sudachi_BS.csv"],
            ["antennapod_MB.csv","osmdroid_MB.csv","zxing_MB.csv","exoplayer_MB.csv","mindustry_MB.csv"],
            ["vinyl_MS.csv","phonograph_MS.csv","javacv_MS.csv","gsyvideoplayer_MS.csv","metadata_MS.csv"],
            ["rxjava_LB.csv","blaze_LB.csv","flowable_LB.csv","daqeclipse_LB.csv","ebean_LB.csv"],
            ["googleauth_LS.csv","jmock_LS.csv","yue_LS.csv","thumbnailator_LS.csv","springdock_ls.csv"],
            ["jabref_UB.csv","commons_UB.csv","k9_UB.csv","talon_UB.csv","sentinel_UB.csv"],
            ["dependencycheck_US.csv","agrona_US.csv","snowflake_US.csv","androidmaps_US.csv","pipeline_US.csv"]]

for x in range(8):
    print("non-diverse-",x, end="-")
    nondiverse = []
    for f in all_filenames:
        #combine all files in the list
        if f in projects[x]:
            print(f, end=";")
            nondiverse.append(f)
            
    combined_csv = pd.concat([pd.read_csv(c) for c in nondiverse])
    #export to csv        
    newFile = list(key_dict.keys())[list(key_dict.values()).index(x)] + '_non-diverse_combined'
    combined_csv.to_csv("../results/nondiverse_"+newFile+".csv", index=False, encoding='utf-8-sig')        
    print()