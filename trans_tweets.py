from googletrans import Translator
import pandas as pd
from nltk.tokenize import word_tokenize

tokenizer = RegexpTokenizer(r'\w+')
tweets_df = pd.read_csv('/Users/salonibhogale/scraped_tweets_file.csv') #edit to location of the extracted Tweets file
translator = Translator()
translated_tweets=[]
for i in range(0, len(tweets_df)):
    try:
        t = tweets_df.iloc[i]['text']
        trans = translator.translate(t)
        translated_tweets.append(trans.text)
        print(i)
    except:
        print("Error Occured",i)
        translated_tweets.append("error in translation")
        continue

t1 = pd.Series(translated_tweets)
tweets_df['translated_tweets']=t1.values

tweets_df = pd.read_csv('/Users/salonibhogale/PycharmProjects/IR_Twitter/translated_tweets_final.csv')
final_text=[]

#to check if certain tweets had an error in translation, whether they can be translated word-wise
for i in range(0,len(tweets_df)):
    t_test = tweets_df.iloc[i]['translated_tweets']
    l_test = tweets_df.iloc[i]['language']
    if t_test == "error in translation" and l_test != 'en':
        q1 = tweets_df.iloc[i]['text']
        q2 = word_tokenize(q1)
        l1 = []
        for j in range(0,len(q2)):
            try:
                temp = translator.translate(q2[j])
                l1.append(temp.text)
            except:
                l1.append("")
        f_text = ' '.join(l1)
        final_text.append(f_text)
    else:
        final_text.append("found_earlier")
    print(i)

final_text = pd.Series(final_text)
tweets_df['word_translations']=final_text.values
tweets_df.to_csv('final_translation_tweets.csv',',')

#creating a column to store the final text of the tweets
final_column=[0]*len(tweets_df)
for i in range(0, len(tweets_df)):
    lang = tweets_df.iloc[i]['language']
    trans_tweets=tweets_df.iloc[i]['translated_tweets']
    word_trans = tweets_df.iloc[i]['word_translations']
    if lang == 'en':
        final_column[i]=tweets_df.iloc[i]['text']
    elif trans_tweets != 'error in translation':
       final_column[i]=trans_tweets
    elif word_trans != 'found_earlier':
        final_column[i]=word_trans

final_column = pd.Series(final_column)
tweets_df['final_column']=final_column.values

#final cleaning & searching for relevant terms
f2=[]
for i in range(0,len(tweets_df)):
    txt = tweets_df.iloc[i]['final_column']
    if type(txt).__name__ == 'str':
        s = str.replace(txt,',','').lower()
        f2.append(s)
    else:
        f2.append('NA')

f2 = pd.Series(f2)
tweets_df['final_tweets']=f2.values

#to check how many are NaN in the dataset
is_nan=[]
for i in range(0,len(tweets_df)):
    txt = tweets_df.iloc[i]['language']
    if type(txt).__name__ == 'float':
        if math.isnan(txt)==True:
            is_nan.append(i)

final_tweets=tweets_df[['Unnamed: 0', 'user', 'favorite_count', 'source', 'text','in_reply_to_screen_name', 'is_retweet', 'created_at', 'retweet_count','id_str', 'language', 'translated_tweets', 'word_translations', 'final_final_column']]
final_tweets2=tweets_df[['user', 'favorite_count', 'source', 'text','in_reply_to_screen_name', 'is_retweet', 'created_at', 'retweet_count','id_str', 'language', 'final_tweets']]

final_tweets2.to_csv(filename.csv,',') #edit this

t = final_tweets2

rem_list=[0]*len(t)
for i in range(0,len(t)):
    t1 = t.iloc[i]['final_tweets']
    if type(t1).__name__ == 'float':
        if math.isnan(t1)==True:
            rem_list[i]=1

rem_list = pd.Series(rem_list)
t['remove_list']=rem_list.values

final_col = []
for i in range(0,len(t2)):
    txt = t2.iloc[i]['final_tweets']
    final_col.append(txt.lower())

final_col = pd.Series(final_col)
t2['final_col']=final_col.values
t2.to_csv('cleaned_tweets.csv',',') #put your filename here
