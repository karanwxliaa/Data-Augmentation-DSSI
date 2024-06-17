#author: Di Lu
# -*- coding: utf-8 -*-                                                                                                  
import argparse
import sqlite3 as lite
import os
import json

def langid_extract(source_language, target_language, panlex_dir):
    source_langid = 10280  # default ID for Kinyarwanda
    target_langid = 341  # default ID for English
    wiktionary_file = os.path.join(panlex_dir, 'langvar.json')
    with open(wiktionary_file) as f:
        lines = f.read()
    json_lines = json.loads(lines)
    for line in json_lines:
        if line['lang_code'] == source_language and line['var_code'] == 0:
            source_langid = str(line['id'])
        if line['lang_code'] == target_language and line['var_code'] == 0:
            target_langid = str(line['id'])
    return source_langid, target_langid

def extract_bilingual_lexicon(source_language, target_language, source_langid, target_langid, output_directory, sql_database):
    con = lite.connect(sql_database)

    with con:
        print('loading expression file')

        ll = {}
        hl = {}
        expr_dic = {}
        mention_dic = {}
        cur = con.cursor()
        cur.execute("SELECT * FROM Exprs")
        while True:
            row = cur.fetchone()
            if row is None:
                break
            expr_id = row[1]
            lang_id = row[2]
            term = row[3]
            expr_dic[expr_id] = lang_id
            if lang_id == source_langid:
                ll[expr_id] = term
            elif lang_id == target_langid:
                hl[expr_id] = term
        print('step 2')
        cur.execute("SELECT * FROM Denotations")
        while True:
            row = cur.fetchone()
            if row is None:
                break
            meaning_id = row[2]
            ex_id = row[3]
            if expr_dic[ex_id] == source_langid:
                if meaning_id in mention_dic:
                    mention_dic[meaning_id][0].append(ex_id)
                else:
                    mention_dic[meaning_id] = [[ex_id], []]
            elif expr_dic[ex_id] == target_langid:
                if meaning_id in mention_dic:
                    mention_dic[meaning_id][1].append(ex_id)
                else:
                    mention_dic[meaning_id] = [[], [ex_id]]

        with open(os.path.join(output_directory, f'{source_language}_{target_language}_lexicon.txt'), 'w', encoding='utf-8') as f_out:
            mm = 0
            print('step 3')
            for key, onepair in mention_dic.items():
                t1 = []
                t2 = []
                for one_1 in onepair[0]:
                    t1.append(ll[one_1])
                for one_1 in onepair[1]:
                    t2.append(hl[one_1])
                if t1 and t2:
                    mm += 1
                    for ile in t1:
                        for hle in t2:
                            f_out.write(f'{ile}\t{hle}\n')
        print(mm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracting bi-lingual lexicon from Panlex')
    parser.add_argument('--source_language', default='kin', help='identify the 3-digit language code for source language')
    parser.add_argument('--target_language', default='eng', help='identify the 3-digit language code for target language')
    parser.add_argument('--output_directory', default='data/lexicons/', help='identify the path of the folder to save the extracted lexicon')
    parser.add_argument('--panlex_dir', default='data/', help='path of folder for original Panlex json files')
    parser.add_argument('--sql_database', default='data/panlex.db', help='path of processed sqlite database of panlex')
    args = parser.parse_args()
    if not os.path.exists(args.output_directory):
        os.mkdir(args.output_directory)

    # retrieve the language variation code from Panlex database
    source_langid, target_langid = langid_extract(args.source_language, args.target_language, args.panlex_dir)
    if source_langid is None:
        print("Error: incorrect source language code")
    if target_langid is None:
        print("Error: incorrect target language code")
    else:
        assert source_langid is not None and target_langid is not None
        print(f"Extracting {args.source_language}_{source_langid} -- {args.target_language}_{target_langid} lexicon")
        extract_bilingual_lexicon(args.source_language, args.target_language, source_langid, target_langid, args.output_directory, args.sql_database)
    print("Extraction completed")
