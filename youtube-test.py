import pandas as pd

df = pd.read_csv("C:\\users\\exper\\documents\\python_test\\youtube-ing.csv")

result = df.head(10)
result = df[5:20].head()
result = df.columns
result = df.columns
df.drop(['thumbnail_link','comments_disabled','ratings_disabled','video_error_or_removed','description'],axis=1, inplace=True)

result = df

# result = df['likes'].mean()
# print(result)
# result = df['dislikes'].mean()
# result = df.head(50)[['title','likes','dislikes']]
# result =           df[(df["views"].max())==df['views']] [["title","views"]]
# result = df.sort_values("views", ascending=False).head(10) [["title","views"]]
# likesList = list(df['likes'])
# dislikesList = list(df['dislikes'])

def oranal(dataset):
    likesList = list(dataset["likes"])
    dislikesList = list(dataset["dislikes"])
    liste= list(zip(likesList,dislikesList))#tuple list
    oranListesi=[]
    for likes, dislikes in liste:
        if (likes + dislikes) == 0:
            oranListesi.append(0)
        else:
            oranListesi.append(likes/(likes+dislikes))
    return oranListesi

    print(liste)

df['beğeni_oranı'] = oranal(df)
print(df.sort_values('beğeni_oranı', ascending=False).head(50)[['title','beğeni_oranı']])


#print(result)