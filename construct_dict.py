import pandas as pd
import numpy as np
import re
import os
from bs4 import BeautifulSoup


def createItem(lemma: str, page: str, zh_def: str, ori_def: str, item_id=None, lemma_id=None):
    soup = BeautifulSoup(features="html.parser")

    # Create tags
    item_tag = soup.new_tag("div", attrs={'class': 'item'})
    lemma_tag = soup.new_tag("div", attrs={'class': 'lemma'})
    page_tag = soup.new_tag("span", attrs={'class': 'page'})
    zh_def_tag = soup.new_tag("p", attrs={'class': 'zh-def'})
    ori_def_tag = soup.new_tag("p", attrs={'class': 'ori-def'})
    # Structure html
    item_tag.append(lemma_tag)
    item_tag.append(page_tag)
    item_tag.append(zh_def_tag)
    item_tag.append(ori_def_tag)

    # Write data
    lemma_tag.string = lemma
    page_tag.string = page
    zh_def_tag.string = zh_def
    ori_def_tag.append(BeautifulSoup(ori_def, "html.parser"))
    if item_id:
        item_tag['id'] = str(item_id)
    if lemma_id:
        lemma_tag['id'] = str(lemma_id)

    return str(item_tag)

def import_from_gsheet():
    gids = ['679511153', '1931724449', '151044886', '1128079217', '1431072574', '866770763', '1207822401', '396391367', '1345694829', '939992016', '971568665', '1842077571']
    pages = ['妤蓁_13-41', '曉鈞_42-70', '容榕_71-99', '永賦_100-128', '庭瑋_129-157', '飛揚_158-186', '俊宏_187-215', '瑞恩_216-244', '凱弘_247-273', '晴方_274-302', '莊勻_303-331', '峻維_326-360']
    url = "https://docs.google.com/spreadsheets/d/186qohB4p9_ewDqggE547E92bxYTILKuSm26PWljVInk/export?format=csv&gid={gid}"
    dfs = []
    for gid, sheet in zip(gids, pages):
        df = pd.read_csv(url.format(gid=gid), dtype='str').dropna(subset=["詞條", "釋義"]).replace(np.nan, '')
        df['轉寫者'] = sheet
        dfs.append(df)
    merged_df = pd.concat(dfs, sort=False, ignore_index=True)
    
    # Strip whitespaces
    for col in merged_df.columns:
        merged_df[col] = pd.core.strings.str_strip(merged_df[col])
    return merged_df


def get_all_lemma(df, lemma_col='詞條'):
    all_lemma = set(df[lemma_col].values)
    all_lemma2 = list(all_lemma)
    for l in list(all_lemma):
        if '*' in l:
            all_lemma2.remove(l)
    return all_lemma2


def index_lemma_in_def(df, all_lemma, def_col='釋義'):
    indexed_defs = []
    pat = " (" + '|'.join(all_lemma) + ")[\.,;]? "
    for def_ in df[def_col].values:
        # Wrap <a> tag around lemma in definition
        replacement = ' <a class="idx" href="#">\g<1></a> '
        def_ = re.sub(pat, replacement, def_)
        
        # Add href in <a> tag
        tag = BeautifulSoup(def_, "html.parser")
        for a in tag.find_all('a', attrs={'class':'idx'}):
            a["href"] = '#' + a.text.lower() + '_1'
        def_ = str(tag)
        indexed_defs.append(def_)
    return indexed_defs

########------------------------ Main Function --------------------##########

def getDictItems():
    #--------------------- Get data from google sheets -------------------#
    merged_df = import_from_gsheet()
    #---------------- Index lemma mentioned in def ----------------#
    all_lemma = get_all_lemma(merged_df)
    merged_df['釋義'] = index_lemma_in_def(merged_df, all_lemma)


    #---------------- Convert pd to HTML file ---------------------#
    toc_id = []
    lemma_id = []
    dict_string = ''
    lemma = "1"
    lemma_counter = {}
    for idx, row in merged_df.iterrows():
        # Check change of alphabet
        lemma_str = row['詞條'].strip().lower().replace(' ', '')
        if lemma_str[0] != lemma[0].lower():
            alphabet = row['詞條'].strip()[0].lower()
            item_id = f"{alphabet}-first"
            if item_id in toc_id or item_id in ["*-first", "_-first"]:
                item_id = None
            else:
                toc_id.append(item_id)
        else:
            item_id = None
        # Write to HTML
        if lemma_str in lemma_counter.keys():
            lemma_counter[lemma_str] += 1
        else:
            lemma_counter[lemma_str] = 1
        lid = lemma_str + f"_{lemma_counter[lemma_str]}"
        item = createItem(row['詞條'].strip(), row['頁數'].strip(), row['中文'].strip(), row['釋義'].strip(), item_id=item_id, lemma_id=lid)
        dict_string += item
        # Record alphabet data for next loop
        lemma = row['詞條'].strip()
    # Write dict toc
    toc = ["<li><a href='#" + id_ + f"'>{id_[0].upper()}</a></li>" for id_ in toc_id]
    
    
    return dict_string, ''.join(toc)
    # Write html template
    #html = html_template.format(dictionary=dict_string,
    #                            toc=''.join(li))    
    #with open(html_file, 'w', encoding="utf-8") as f:
    #    f.write(html)




if __name__ == "__main__":
    main()
