# define two empty lists before using function i.e 'completing' and 'starting'
# function to subset courses into completions rates:
def get_complete_figs(b):
    for v in c:
        df = b[(b['program_code'] == v)].groupby(['message_out']).learner_id.nunique().reset_index()
        min = str(dict_start.get(v))
        df['is_beginning'] = df.message_out.apply(lambda x : True if min in x else False)
        df_begin = df[df['is_beginning'] == True]
        begun = df_begin.learner_id.sum()
        max = str(dict_complete.get(v))
        starting.append(begun)
        df['is_completing'] = df.message_out.apply(lambda x : True if max in x else False)
        df_complete = df[df['is_completing'] == True]
        complete = df_complete.learner_id.sum()
        completing.append(complete)

    test_df = pd.DataFrame(list(zip(c,starting,completing)),columns=['code', 'starting','completing'])
    return test_df

# function to get number of learners in a dataframe
def get_learners(b):
    learners = b['learner_id'].nunique()
    return learners

# define two empty lists before using function i.e. 'x' and 'y'
# function to get How long it takes to finish the course on average
def get_duration(b):
    for each in c:
        df_course = b[(b.program_code == each)]
        df = b[(b['program_code']== each)].groupby(['message_out']).learner_id.nunique().reset_index()
        max = str(dict_complete.get(each))
        df['is_completing'] = df.message_out.apply(lambda x : True if max in x else False)
        df_message_complete = df[df['is_completing'] == True]
        word = df_message_complete.message_out.unique()
        df_test = b[(b.message_out == list(word)[0])].reset_index(drop = True)
        df_learners = df_test[['learner_id']]
        df_learners_complete = pd.merge(df_learners, df_course, left_on='learner_id',right_on='learner_id',how='inner')
        df_complete_min = df_learners_complete.groupby(['learner_id']).created_at.min().reset_index()
        df_complete_max = df_learners_complete.groupby(['learner_id']).created_at.max().reset_index()
        df_complete_merge = pd.merge(df_complete_min, df_complete_max, left_on='learner_id',right_on='learner_id',how='inner')
        df_complete_merge['created_at_x'] = pd.to_datetime(df_complete_merge['created_at_x'])
        df_complete_merge['created_at_y'] = pd.to_datetime(df_complete_merge['created_at_y'])
        df_complete_merge['Duration'] = df_complete_merge['created_at_y'] - df_complete_merge['created_at_x']
        df_complete_merge['days'] = df_complete_merge['Duration'].dt.days
        df_complete_merge['hours'] = df_complete_merge['Duration'].dt.seconds // 3600
        df_complete_merge['minutes'] = df_complete_merge['Duration'].dt.seconds // 60
        mean_days = df_complete_merge.days.mean()
        x.append(mean_days)
        mean_minutes = df_complete_merge.minutes.mean()
        y.append(mean_minutes)

    duration_df = pd.DataFrame(list(zip(c,x,y)),columns=['code', 'days','minutes'])
    return duration_df

 # function for getting mode
def get_most_common(srs): 
    x = list(srs) 
    my_counter = collections.Counter(x) 
    return my_counter.most_common(1)[0][0]

# creating user_response column
def create_user_response(df):
    df = df.sort_values(by=['created_at'], ascending=True)
    df['user_response'] = df.groupby('learner_id').message_in.shift(periods = 1)
    return df

# creating dayofweek column
def gen_dayofweek(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['dayofweek'] = df['created_at'].dt.dayofweek
    return df
# Describing time of interactions
def get_interval(x):
    if x < 6:
        return 'Early Morning'
    elif x >= 6 and x < 12:
        return 'Morning'
    elif x >= 12 and x < 16:
        return 'Afternoon'
    elif x >= 16 and x < 21:
        return 'Evening'
    elif x >= 21:
        return 'Night'

# Generating the day, month, year and date columns
df1['Year'] = df1['created_at'].dt.year
df1['month'] = df1['created_at'].dt.month
df1['day'] = df1['created_at'].dt.day
df1['date'] = df1['created_at'].dt.date

# Getting the profile from profile interactions

# Easy Way of subsettign data with multiple conditions
# Create the list
poult_certified = list(google_certificate.learner_id)
poultry_Cert = []
for x in poult_certified:
    df4 = df_poultry[df_poultry.learner_id == x]
    poultry_Cert.append(df4)
# Concat the List
poultCert_int = pd.concat(poultry_Cert)

# Function to extract profile questions
def is_prof(x):
    if 'Question 1:' in x:
        return 'age'
    elif 'Swali 1:' in x:
        return 'age'
    elif 'Question 4:' in x:
        return 'gender'
    elif 'Swali 4:' in x:
        return 'gender'
    elif 'Swali 2:' in x:
        return 'county'
    elif 'Question 2:' in x:
        return 'county'
    else:
        return 'invalid'

# creating user response for the interactions dataset
def user_response(df,list_numbers,a):
    df_response = []
    for each in list_numbers:
        df_test = df[df['phone_number'] == each]
        df_test_sorted = df_test.sort_values(by='created_at', ascending=True)
        df_test_sorted['user_response'] = df_test_sorted['message_in'].shift(a)
        df_response.append(df_test_sorted)

    # Concating the df
    df_full = pd.concat(df_response)
    # Return
    return df_full