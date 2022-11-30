import pandas as pd

# from pyxDamerauLevenshtein import damerau_levenshtein_distance


relevant = ['AL', 'AR', 'FL', 'GA', 'KY', 'LA', 'MD',
            'MS', 'MI', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA']


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1+1):
        d[(i, -1)] = i+1
    for j in range(-1, lenstr2+1):
        d[(-1, j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i-1, j)] + 1,  # deletion
                d[(i, j-1)] + 1,  # insertion
                d[(i-1, j-1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i-2, j-2] + cost)  # transposition
    return d[lenstr1-1, lenstr2-1]


def spellCheck(word):
    print("running spell check")
    county_df = pd.read_excel('data\county_names.xlsx')
    county_list = county_df[county_df['state'].isin(relevant)]
    county_list = county_df['county']
    county_set = set(county_list)

    budget = 2
    n = len(word)
    if n < 3:
        budget = 0
    elif 3 <= n < 6:
        budget = 1
    if budget and word.upper() not in county_set:
        for keyword in county_list:
            if damerau_levenshtein_distance(word.lower(), keyword.lower()) <= budget:
                # print("corrected " + keyword)
                return keyword.title()

    return word


def fixCounties():
    # print("running fixcounties")
    schools_df = pd.read_excel('rosenwald.xlsx', nrows=100)

    for i in range(len(schools_df.index)):
        schools_df['County'][i] = spellCheck(schools_df['County'][i])
    # schools_df['County'].transform(lambda x: spellCheck(x))
    # for x in schools_df['County']:
    #     print(spellCheck(x))
    schools_df.to_excel("output.xlsx")
    print("finished!")
