#to customize change ROI
#change pad list
#change name list
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
def make_df(file1):
    df=pd.read_csv(file1,skiprows=2,delim_whitespace=True,header=None)
    df.columns=['pos','sub','count']
    df_filtered=df[df.loc[:,'sub'].str.contains("A|T|G|C")]
    f=df_filtered.loc[:,'sub'].apply(lambda x : x.split("->")[1])
    df_filtered=df_filtered.assign(sub=f)
    global ROI
    ROI="GGAAGCGGCGGCGCTGACCGGGCTGGATCTGCGCCTGTTGGCCCCGAAAGCCTGCTGGCCGGAAGAGAGCCTGGTGGCGGAGTGCAGCGCGCTGGCG" ####CHANGE
    df_wide=df_filtered.pivot(index='pos', columns='sub', values='count')
    df_wide=df_wide.reindex(range(len(ROI)))
    df_wide=df_wide.fillna(value=0)
    ROI_lis=list(ROI)
    df_wide["roi"]=ROI_lis
    
    return df_wide

def extract_nodes(file_name):
    f=open(file_name)
    lines=f.readlines()
    line=lines[1].split()
    
    nodes=int(line[0])
    return nodes

def make_df_lis(pad_lis,name_lis,gene):
    total_lis=[]
    for i in range(len(pad_lis)):
        file_name="exoutput/"+gene+pad_lis[i]+"_3"
        #print(file_name)
        nodes=extract_nodes(file_name)
        df_0=make_df(file_name)
        df_0.loc[df_0.roi == 'C',['A','T']] = 0
        df_0.loc[df_0.roi == 'G',['A','T']] = 0
        sum_column=pd.DataFrame(df_0.sum(axis=0))
        sum_column=sum_column.drop(['roi'])
        total= int(sum_column.sum(axis=0))
        total=total/nodes
        total=total/len(ROI)
        total=total/113
        total_lis.append(total)
    return total_lis

def filter_sub(df, nuc1,nuc2,sample):
    df_sub=df.loc[df['roi'] == nuc1]
    df_sub=df_sub.loc[:, nuc2:nuc2]
    df_sub=df_sub.rename(index=str, columns={nuc2:sample})
    
    return df_sub

def single_sub(pad_lis,name_lis,gene):
    df_lis=[]
    for i in range(len(pad_lis)):
        file_name="exoutput/"+gene+pad_lis[i]+"_3"
        nodes=extract_nodes(file_name)
        df_i=make_df(file_name)
        df_C_A=filter_sub(df_i,'C','A',name_lis[i])
        df_C_A=df_C_A/nodes
        df_lis.append(df_C_A)
    merge= pd.concat(df_lis, axis=1)
    sums=pd.DataFrame(merge.sum(axis=0)) 
    
    fig=sums.plot(kind='bar',figsize=(10,5),title="C->A Frequency",color="black",legend=None)

gene="argF"
pad_lis=["11","31","22","13"] #CHANGE
name_lis=['WT','mfd','CTD','uvrD'] #CHANGE
totals= make_df_lis(pad_lis,name_lis,gene) 
print(totals)
y_pos=np.arange(len(name_lis))
sns.set_style('whitegrid')
sns.barplot(x=name_lis,y=totals,color='grey',linewidth=2.5,edgecolor=".2")
#plt.xticks(y_pos,name_lis)
plt.ylabel("Mutations per nucleotide generation")
sns.plt.savefig('MDS_test.pdf',transparent=True)
plt.show()

