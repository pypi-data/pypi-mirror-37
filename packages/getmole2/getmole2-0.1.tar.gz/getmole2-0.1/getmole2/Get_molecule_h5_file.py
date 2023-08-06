#### extract qname with coordiantes
import pdb
#pdb.set_trace()
from collections import defaultdict
import pickle
import sys
import pysam
import time
import os

from argparse import ArgumentParser

parser = ArgumentParser(description="Generate h5 file with variants:")
parser.add_argument('--bam_file','-bam',help="input sorted bam file")
parser.add_argument('--vcf_file','-vcf',help="input vcf file")
parser.add_argument('--output_file_prefix','-o',help="output filename")
parser.add_argument('--chr_start','-start',type=int,help="chromosome start from", default=1)
parser.add_argument('--chr_end','-end',type=int,help="chromosome end by", default=22)
parser.add_argument('--mbq','-bq',type=int,help="minimum base quality to consider a base for haplotype fragment, default 13", default=13)
parser.add_argument('--mmq','-mq',type=int,help="minimum read mapping quality to consider a read for phasing, default 20", default=20)
parser.add_argument('--boundary','-b',type=int,help="boundary(bp) to split two fragments with the same barcode", default=20)
#parser.add_argument('--out_dir','-o_dir', help="Directory to store outputs", default='results_/')

args = parser.parse_args()


def flatten(listoflist):
    flat_list = []
    for alist in listoflist:
        for val in alist:
            flat_list.append(val)
    return flat_list


def save_variant_dict(vcf_file,mbq_threshold):
    f = open(vcf_file,"r")
    variant_dict =  defaultdict(list)
    for line in f:
        data = line.rsplit()
        if data[0][:2] != "##" and data[0][:2] != "#C":
            try:
                qual = float(data[5])
                chr_num = int(data[0][3:])
                pos = int(data[1]) - 1
                ref = data[3]
                alt = data[4]
                GT = data[9].split(":")[0]
                if (GT == "0/1"  or GT == "1/0") and len(ref) == 1 and len(alt) == 1 and qual >= mbq_threshold:
                    variant_dict[(chr_num,pos)] = [ref,alt,GT]
            except:
                if data[0] == "chrX":
                    chr_num = "X"
                qual = float(data[5])
                pos = int(data[1]) - 1
                ref = data[3]
                alt = data[4]
                GT = data[9].split(":")[0]
                if (GT == "0/1"  or GT == "1/0") and len(ref) == 1 and len(alt) == 1 and qual >= mbq_threshold:
                    variant_dict[(chr_num,pos)] = [ref,alt,GT]


    
    pickle.dump(variant_dict, open("variant_dict_heterozygous.p", "wb"))
    return variant_dict     


def get_match_num(cigar):
    used_num = ""
    cumu_num = 0
    for i in range(len(cigar)):
        cur_num = cigar[i]
        try:
            first_num = int(cur_num)
            used_num += cur_num
        except ValueError:
            if cur_num != "M":
                cumu_num += int(used_num)
                used_num = ""
            else:
                match_num = int(used_num)
                break
    return (cumu_num,match_num)


def get_match_num_revised(cigar):
    cigar_len = len(cigar)
    cigar_list = []
    num_string = ""
    for i in range(cigar_len):
        letter = cigar[i]
        if letter.isalpha():
            cigar_list.append(num_string)
            num_string = ""
            cigar_list.append(letter)
        else:
            num_string += letter

    indices = [i for i, x in enumerate(cigar_list) if x == "M"]
    cumu_num = 0
    cumu_start = 0
    cumu_num_list = []
    cumu_start_list = []
    match_num_list = []
    for idx in indices:
        match_num = int(cigar_list[idx - 1])
        match_num_list.append(match_num)
        for i in range(0,idx,1):
            parameter = cigar_list[i+1]
            if parameter in ["M", "S", "H", "I"]:
                cumu_num += int(cigar_list[i])
            if parameter in ["M", "D"]:
                cumu_start += int(cigar_list[i])

        cumu_num_list.append(cumu_num-match_num)
        cumu_start_list.append(cumu_start-match_num)
        cumu_num = 0
        cumu_start = 0

    return (cumu_num_list,cumu_start_list,match_num_list)


def check_read_hp(hp,barcode):
    if len(set(hp)) == 1:
        hp_use = True
        hp_flag = hp[0]
    else:
        count0 = hp.count("0")
        count1 = hp.count("1")
        if count0 >= 4*count1:
            hp_use = True
            hp_flag = "0"
        elif count1 >= 4*count0:
            hp_use = True
            hp_flag = "1"
        else:
            hp_use = False
            hp_flag = "none"
            #print(barcode)
    return (hp_use,hp_flag)


def get_mole_variant(chr_num,mole_dict_3,mole_dict_4,mole_dict_5,barcode):
    mole_variant = defaultdict(list)
    for qname,cigar_all in mole_dict_5[barcode].items():
        #print(cigar_all)
        for ii in range(len(mole_dict_5[barcode][qname])):
            cigar = cigar_all[ii]
            if cigar != None:
                curr_string =  mole_dict_4[barcode][qname][ii]
                cumu_num, match_num = get_match_num(cigar)
                start_locus = int(mole_dict_3[barcode][qname][ii])
                match_string = curr_string[cumu_num:cumu_num+match_num]
                end_locus = len(match_string) - 1
                for jj in range(0,end_locus-1):
                    idx_j = jj + start_locus - 1
                    val = variant_dict[(chr_num,idx_j)]
                    if val != []:
                        ref = val[0]
                        alt = val[1]
                        GT = val[2]
                        match_str = match_string[jj:jj+len(ref)]
                        if match_str == ref:
                            mole_variant[idx_j].append("0")
                        elif match_str == alt:
                            mole_variant[idx_j].append("1")

    return mole_variant


def get_mole_variant_revised(chr_num,mole_dict_3,mole_dict_4,mole_dict_5,barcode):
    mole_variant = defaultdict(list)
    for qname,cigar_all in mole_dict_5[barcode].items():
        #print(cigar_all)
        for ii in range(len(mole_dict_5[barcode][qname])):
            cigar = cigar_all[ii]
            if cigar != None:
                curr_string =  mole_dict_4[barcode][qname][ii]
                cumu_num_list,cumu_start_list, match_num_list = get_match_num_revised(cigar)
                for kk in range(len(cumu_num_list)):
                    cumu_num = cumu_num_list[kk]
                    cumu_start = cumu_start_list[kk]
                    match_num = match_num_list[kk]
                    start_locus = int(mole_dict_3[barcode][qname][ii]) + cumu_start
                    match_string = curr_string[cumu_num:cumu_num+match_num]
                    end_locus = len(match_string) - 1
                    for jj in range(0,end_locus-1):
                        idx_j = jj + start_locus - 1
                        val = variant_dict[(chr_num,idx_j)]
                        if val != []:
                            ref = val[0]
                            alt = val[1]
                            GT = val[2]
                            match_str = match_string[jj:jj+len(ref)]
                            if match_str == ref:
                                mole_variant[idx_j].append("0")
                                #if kk > 0:
                                    #print("use here", ref, alt, match_str,match_num, match_num_list[0])
                            elif match_str == alt:
                                mole_variant[idx_j].append("1")
                                #if kk > 0:
                                    #print("use here", ref, alt, match_str,match_num, match_num_list[0])
                            #else:
                                #if kk > 0:
                                    #print("wrong here",ref,alt,match_str)

    return mole_variant


def save_pickle_file(dict1,fname):
    for value in dict1:
        dict1[value] = dict(dict1[value])
    my_dict = dict(dict1)
    with open(fname, "wb") as f:
        pickle.dump(my_dict,f) 


def process_sorted_bam(bam_file,output_file,qname_file,qname_pos_file,variant_dict,threshold_start,threshold_end,boundary,mmq_threshold):
    #qname_pos = defaultdict(int)
    qname_pos = defaultdict(list)
    mole_qname_dict = defaultdict(lambda: defaultdict(list))
    sam_file = pysam.AlignmentFile(bam_file, "rb")
    threshold_pairs = 2
    fw= open(output_file,"w")
    mole_dict = defaultdict(list)
    mole_dict_2 = defaultdict(lambda: defaultdict(list))
    mole_dict_3 = defaultdict(lambda: defaultdict(list))
    mole_dict_4 = defaultdict(lambda: defaultdict(list))   # read string
    mole_dict_5 = defaultdict(lambda: defaultdict(list))   # cigar
    curr = 0
    count_mole = 1
    chr_begin = threshold_start
    if threshold_start == 23:
        use_chr_num = "chrX"
    else:
        use_chr_num = "chr" + str(threshold_start)

    for read in sam_file.fetch(use_chr_num):
        #print(curr)
        curr += 1
        raw_chr_num = read.reference_name
        #if raw_chr_num == "chrX":
            #break
        if use_chr_num == "chrX":
            chr_num = "X"
        else:
            chr_num = int(read.reference_name[3:])
        #print(chr_num)
        tags = read.get_tags()
        barcode_field = [s for s in tags if "BX" in s]
        mq = read.mapping_quality
        if barcode_field != [] and mq >= mmq_threshold:
            barcode =  barcode_field[0][1].split("-")[0]
            start_pos = read.pos + 1   # use "1" coordinate
            qname = read.qname
            if read.is_read1:
                read_pair = 1
            elif read.is_read2:
                read_pair = 2
            #qname_pos[(qname,read_pair)] = start_pos
            qname_pos[qname].append(start_pos)
            if len(mole_dict[barcode]) == 0:
                mole_dict[barcode].append(start_pos) 
                mole_dict_2[barcode][qname].append(read_pair)
                mole_dict_3[barcode][qname].append(start_pos) 
                mole_dict_4[barcode][qname].append(read.seq) 
                mole_dict_5[barcode][qname].append(read.cigarstring) 
            elif len(mole_dict[barcode]) > 0:
                dist = start_pos - mole_dict[barcode][-1]
                if dist < boundary:   
                    mole_dict[barcode].append(start_pos) 
                    mole_dict_2[barcode][qname].append(read_pair)
                    mole_dict_3[barcode][qname].append(start_pos)
                    mole_dict_4[barcode][qname].append(read.seq)
                    mole_dict_5[barcode][qname].append(read.cigarstring)
                else:
                    count_del = 0
                    for key,value in mole_dict_2[barcode].items():
                        if len(value) == 1:
                            count_del += 1

                    all_pos = mole_dict_3[barcode].values()
                    num_of_pairs = len(all_pos) - count_del

                    if num_of_pairs >= threshold_pairs :  # 2 pairs
                        poss = flatten(all_pos)
                        start_ = min(poss)
                        end_ = max(poss)
                        mole_len = end_ - start_  + 150
                        mole_qname_dict[count_mole] = mole_dict_2[barcode].copy()
                        mole_variant = get_mole_variant_revised(chr_num,mole_dict_3,mole_dict_4,mole_dict_5,barcode)
                        if mole_variant == {}:
                            fw.writelines(str(chr_num) + "\t" + str(start_) + "\t" + str(end_) + "\t" + str(mole_len) + "\t" + str(len(poss)) + "\t" + str(barcode) + "\t" + str(count_mole) + "\n")
                        else:
                            fw.writelines(str(chr_num) + "\t" + str(start_) + "\t" + str(end_) + "\t" + str(mole_len) + "\t" + str(len(poss)) + "\t" + str(barcode) + "\t" + str(count_mole) + "\t")
                            count_var = 0
                            for locus_start, hp in mole_variant.items():
                                hp_use, hp_flag = check_read_hp(hp,barcode)
                                if count_var == len(mole_variant) - 1:
                                    if hp_use:
                                        fw.writelines(str(locus_start) + ":" + hp_flag + "\n")
                                        #count_1 += 1
                                    else:
                                        fw.writelines("\n")
                                        #count_2 += 1
                                else:
                                    if hp_use:
                                        fw.writelines(str(locus_start) + ":" + hp_flag + "\t")
                                        #count_1 += 1
                                    #else:
                                        #count_2 += 1
                                count_var += 1

                        mole_dict[barcode] = [] 
                        mole_dict_2[barcode] = defaultdict(list)
                        mole_dict_3[barcode] = defaultdict(list) 
                        mole_dict_4[barcode] = defaultdict(list) 
                        mole_dict_5[barcode] = defaultdict(list) 
                        mole_dict[barcode].append(start_pos)
                        mole_dict_2[barcode][qname].append(read_pair)
                        mole_dict_3[barcode][qname].append(start_pos)
                        mole_dict_4[barcode][qname].append(read.seq)
                        mole_dict_5[barcode][qname].append(read.cigarstring)
                        count_mole += 1
                    else:
                        mole_dict[barcode] = []
                        mole_dict_2[barcode] = defaultdict(list)
                        mole_dict_3[barcode] = defaultdict(list)
                        mole_dict_4[barcode] = defaultdict(list)
                        mole_dict_5[barcode] = defaultdict(list)
                        mole_dict[barcode].append(start_pos)
                        mole_dict_2[barcode][qname].append(read_pair)
                        mole_dict_3[barcode][qname].append(start_pos)
                        mole_dict_4[barcode][qname].append(read.seq)
                        mole_dict_5[barcode][qname].append(read.cigarstring)


    if threshold_end == 23:
        chr_num = "X"
    else:
        chr_num = threshold_end
    for barcode,value in mole_dict.items():
        if len(value) > 0:
            count_del = 0
            for qname,num_reads in mole_dict_2[barcode].items():
                if len(num_reads) == 1:
                    count_del += 1

            all_pos = mole_dict_3[barcode].values()
            num_of_pairs = len(all_pos) - count_del
            if num_of_pairs >= threshold_pairs : # 2 pairs
                poss = flatten(all_pos)
                start_ = min(poss)
                end_ = max(poss)
                mole_len = end_ - start_  + 150
                mole_qname_dict[count_mole] = mole_dict_2[barcode].copy()
                mole_variant = get_mole_variant_revised(chr_num,mole_dict_3,mole_dict_4,mole_dict_5,barcode)
                if mole_variant == {}:
                    fw.writelines(str(chr_num) + "\t" + str(start_) + "\t" + str(end_) + "\t" + str(mole_len) + "\t" + str(len(poss)) + "\t" + str(barcode) + "\t" + str(count_mole) + "\n")
                else:
                    fw.writelines(str(chr_num) + "\t" + str(start_) + "\t" + str(end_) + "\t" + str(mole_len) + "\t" + str(len(poss)) + "\t" + str(barcode) + "\t" + str(count_mole) + "\t")
                    count_var = 0
                    for locus_start, hp in mole_variant.items():
                        hp_use, hp_flag = check_read_hp(hp,barcode)
                        if count_var == len(mole_variant) - 1:
                            if hp_use:
                                fw.writelines(str(locus_start) + ":" + hp[0] + "\n")
                                #count_1 += 1
                            else:
                                fw.writelines("\n")
                                #count_2 += 1
                        else:
                            if hp_use:
                                fw.writelines(str(locus_start) + ":" + hp[0] + "\t")
                                #count_1 += 1
                            #else:
                                #count_2 += 1
                        count_var += 1

                count_mole += 1

    
    fw.close()
    sam_file.close()
    save_pickle_file(mole_qname_dict,qname_file)
    pickle.dump(qname_pos,open(qname_pos_file,"wb"))
    mole_qname_dict.clear()
    qname_pos.clear()

    #print("count results:")
    #print(count_1, count_2)





if __name__ == "__main__":
    if len(sys.argv) == 1:
        os.system("python Get_molecule_h5_file.py -h")
    else:
        bam_file = args.bam_file
        vcf_file = args.vcf_file
        mbq_threshold = args.mbq
        mmq_threshold = args.mmq
        boundary = args.boundary
        output_file_prefix = args.output_file_prefix
        #variant_dict = pickle.load(open("variant_dict_heterozygous.p", "rb"))
        variant_dict = save_variant_dict(vcf_file,mbq_threshold)
        chr_start = int(args.chr_start)
        chr_end = int(args.chr_end)
        for chr_num in range(chr_start,chr_end+1):
            h5_file = output_file_prefix + "_chr" + str(chr_num)
            h5_qname_file = output_file_prefix + "_chr" + str(chr_num) + "_qname.p"
            h5_qname_pos_file = output_file_prefix + "_chr" + str(chr_num) + "_qname_pos.p"
            process_sorted_bam(bam_file,h5_file,h5_qname_file,h5_qname_pos_file,variant_dict,chr_num,chr_num,boundary,mmq_threshold)

