import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

data_folder = os.path.join("..", "data")

def plot_distribution(dist_df, title, ax, kind='bar', show_pct=True):
    """
    Plot distribution as a bargraph
    If dropna==false, highlight NaNs
    Print percentage of each value in distribution
    """
    ax = dist_df.plot(
        kind=kind, 
        title=title,
        ax=ax)
    
    # highlight NaNs if not dropped
    try:
        ax.patches[dist_df.index.get_loc(None)].set_facecolor('red')
    except Exception as e:
        pass
    
    if show_pct:
        normalized_dist_df = dist_df.div(dist_df.values.sum())
        pct_dist = np.multiply(list(normalized_dist_df), 100)
        for i, val in enumerate(dist_df):
            ax.text(i, val + (0.01 * val), str('%.2f %%' % pct_dist[i]))  

def choose_race(name, lastname_race_df):
    """
    given a name (with no spaces), randomly choose a race given the probabilities
    in the the name-to-likelihood mapping provided in lastname_race_df
    """
    races = ['white', 'black', 'asian', 'aian', 'mix', 'hispanic']
    probabilities = lastname_race_df.loc[lastname_race_df['lastname']==name, races].values[0]
    # normalize so that probabilities add to 1
    probabilities /= probabilities.sum()
    return np.random.choice(races, p=probabilities)

def get_race_dist_of_lastname():
    # read in data
    lastname_race_df = pd.read_json(os.path.join(data_folder, 'lastnames.json'))

    # set columns to first row 
    lastname_race_df.columns = [
        'lastname', 
        'rank', 
        'count', 
        'white', 
        'asian', 
        'mix', 
        'aian', 
        'black', 
        'hispanic']

    # skip first and last rows
    lastname_race_df = lastname_race_df.iloc[1:-1]

    # drop unwanted columns
    lastname_race_df = lastname_race_df.drop(['rank', 'count'], axis=1)

    # lowercase names
    lastname_race_df['lastname'] = lastname_race_df['lastname'].str.lower()

    # transform race percentage to a probability
    races = ['white', 'black', 'asian', 'aian', 'mix', 'hispanic']
    lastname_race_df[races] = lastname_race_df[races].replace({'(S)': 0}).apply(lambda x: pd.to_numeric(x)/100)
    
    return lastname_race_df


def get_race_from_full_name(name, lastname_race_df):
    """
    starting from the end, check the word against the lastname_race_df to see that it 
    exist. If so, choose a race using the 'choose_race' function, otherwise, check the
    next word.
    Example:
        "Millie Bobby Brown"
        --> choose race for 'Brown'
        --> if not found, choose race for 'Bobby'
        --> if not found, choose race for 'Millie'
    """
    if name is None or len(name) <= 1:
        return None

    split_array = name.rsplit(' ', 1)
    last = split_array[-1]
    remaining = None

    if len(split_array) > 1:
        remaining = split_array[0]
        
    try:
        return choose_race(last, lastname_race_df)
    except Exception as e:
        return get_race_from_full_name(remaining, lastname_race_df)
    
def get_is_not_entity_from_full_name(name):
    """
    iterates through the name and checks for a set of rules that identify that
    the name belongs to an entity (as opposed to an artist)
    Rules:
        - if the name is suffixed with a comma ',' (ex. "hats incredible, inc., braintree, ma")
        - if the name contians "inc.", "co.", "corp.", "ltd."
        - if the name contains "for", "the", "of"
        - if the name contains "furniture", "design", "company", "apparel", "product", "corporation", "office", "studio", 
        
    Example:
        "Toyota Corp." --> True
        "Cai Guo Qiang" --> False
    """
    is_entity_contains_list = [
        'inc.', 'co.', 'corp.', 'ltd.',
        'furniture', 'design', 'company', 'apparel', 'product', 
        'corporation', 'office', 'studio'
    ]
    is_entity_equals_list = ['the', 'for', 'of']
    
    if name is None or len(name) <= 1:
        return None
    
    split_array = name.rsplit(' ')
    for word in split_array:
        
        # check if word is in is_entity_list
        for w in is_entity_contains_list:
            if w in word:
                return False
            
        # check if word is 'the', 'for', or 'of'
        if any(word in w for w in is_entity_equals_list):
            return False
            
        # check if word ends with ','
        if word[-1] == ',':
            return False
    
    return True

def split_rows(_df):
    """
    transform rows that look like:
    
    | constituent_id | artist_name              | nationality        | gender        |
    | -------------- | ------------------------ | ------------------ | ------------- |
    | 1234, 2345     | Cai Guo Qiang, Duchamp   | (Chinese) (French) | (Male) (Male) |
    
    into this:
    
    | constituent_id | artist_name              | nationality        | gender        |
    | -------------- | ------------------------ | ------------------ | ------------- |
    | 1234           | cai guo qiang            | chinese            | male          |
    | 2345           | duchamp                  | french             | male          |
    
    """

    def split_row(row, row_accumulator):
        c_ids = str(row['constituent_id']).split(', ')
        artists = str(row['artist_name']).split(', ')
        nationalities = str(row['nationality']).split(' ')
        gender = str(row['gender']).split(' ')
        
        # if we can split the name successfully
        if len(c_ids) == len(artists):
            for i, val in enumerate(c_ids):
                if c_ids[i] != 'nan':
                    new_row = [c_ids[i], artists[i].lower(), nationalities[i].lower(), gender[i].lower()]
                    row_accumulator.append(new_row)
            
    new_rows = []
    _df.apply(lambda row: split_row(row, new_rows), axis=1)
    col_list = ['constituent_id', 'artist_name', 'nationality', 'gender']
    return pd.DataFrame(new_rows, columns=col_list).drop_duplicates()

def join_race_and_gender(c_id_string, artist_df):
    """
    takes in a string of c_id(s), ex: "8210" or "8210, 5670"
    returns a total count of male, female, white, black, asian, aian, mix, hispanic
    """
    male = 0
    female = 0
    white = 0
    black = 0
    asian = 0
    aian = 0
    mix = 0
    hispanic = 0
    
    if type(c_id_string) != str: # this means that it is a 'nan' 
        return None, None
    
    c_ids = str(c_id_string).split(', ')
    for c_id in c_ids:
        artist_row = artist_df[artist_df['constituent_id']==c_id]
        if len(artist_row) == 0:
            pass
        
        try:
            gender = artist_row['gender'].iloc[0]
            if gender == 'male':
                male += 1
            elif gender == 'female':
                female += 1
            else: 
                pass
        except Exception:
            pass
        
        try:
            race = artist_row['race'].iloc[0]
            if race == 'white':
                white += 1
            elif race == 'black':
                black += 1
            elif race == 'asian':
                asian += 1
            elif race == 'aian':
                aian += 1
            elif race == 'mix':
                mix += 1
            elif race == 'hispanic':
                hispanic += 1
            else:
                pass
        except Exception:
            pass
    
    return male, female, white, black, asian, aian, mix, hispanic

def plot_acquisition_by_year(artwork_df, ax, features, color_list, title, pct=False):
    
    # drop rows where date_acquired is null
    artwork_with_date_df = artwork_df[artwork_df['date_acquired'].notnull()]

    # get the year YYYY of each acquired date where YYYY >= 1800
    artwork_with_date_df['date_acquired'] = artwork_with_date_df['date_acquired']\
        .map(lambda x: int(str(x)[:4]) if int(str(x)[:4]) >= 1800 else None)

    # drop rows where date_acquired is null
    artwork_with_date_df = artwork_with_date_df[artwork_df['date_acquired'].notnull()]
    
    # create feature_df
    feature_df = [None] * len(features)
    for i, feature in enumerate(features):
        feature_df[i] = artwork_with_date_df[artwork_with_date_df[feature] > 0][['date_acquired']]\
            .groupby(['date_acquired'])['date_acquired'].count()

    r = range(1929, 2018, 1)
    feature_counter_df = pd.DataFrame(columns=features, index=r)

    for i in r:
        for j, g in enumerate(features):
            try:
                feature_counter_df.loc[i, g] = feature_df[j][i]
            except Exception:
                feature_counter_df.loc[i, g] = 0

    if pct:
        feature_pct_df = feature_counter_df.divide(feature_counter_df.sum(axis=1) +.000000001, axis=0)
        feature_pct_df.plot(ax=ax, color=color_list)
        ax.set_ylim(top=1, bottom=0)
    else:
        feature_counter_df.plot(ax=ax, color=color_list)

    ax.legend(loc='lower left')
    ax.set_title(title)