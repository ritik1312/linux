#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# ## GreekGods

# In[9]:


gods_df = pd.read_csv("gods_data.csv")
gods_df.head()


# In[10]:


goddess_df = pd.read_csv("goddesses_data.csv")
goddess_df.head()


# In[11]:


# 1.Merge the data from greek_gods.csv and greek_goddesses.csv based on a common field and create a new table
# that includes information about both gods and goddesses.

common_columns = gods_df.columns[1:]

merge_df = pd.DataFrame()
merge_df["Name"] = list(gods_df["God"]) + list(goddess_df["Goddess"])

merge_df[common_columns] = pd.concat((gods_df[common_columns], goddess_df[common_columns]), ignore_index=True)
merge_df


# In[29]:


# 2.Filter the merged table to only include gods and goddesses who are older than 8000 years, then sort them based on their
# ages in descending order.

merge_df.query('Age > 8000').sort_values(by='Age', ascending=False)


# In[30]:


# 3.Join the two tables based on the "Domain" field and calculate the average age of gods and goddesses in each domain.

avg_age_by_domain = merge_df.groupby("Domain")['Age'].mean()
avg_age_by_domain


# In[31]:


# 4.Determine which god/goddess has the highest age, and then find out if they are a god or a goddess.

max_age = merge_df['Age'].max()
oldest = merge_df[merge_df['Age'] == max_age]['Name'][0]

if oldest in list(gods_df['God']):
    print("Oldest: God",oldest)
else:
    print("Oldest: Goddess",oldest)


# In[32]:


# 5.Create a new column in each table called "Age_Group" and categorize the gods/goddesses into groups
# such as "Young" (age < 5000), "Middle-aged" (age between 5000 and 8000), and "Old" (age > 8000).

def categorize_age(age):
    if age < 5000:
        return 'Young'
    elif age >= 5000 and age <= 8000:
        return "Middle-aged"
    else:
        return "Old"

gods_df['Age_Group'] = gods_df['Age'].apply(categorize_age)
goddess_df['Age_Group'] = goddess_df['Age'].apply(categorize_age)
print(gods_df)
print(goddess_df)


# In[33]:


# 6.Compare the average ages of gods and goddesses. Is there a significant age difference between them? If yes,
# which group tends to be older?

avg_gods_age = gods_df['Age'].mean()
avg_goddess_age = goddess_df['Age'].mean()

print("Avg age of Gods:",avg_gods_age)
print("Avg age of Goddess:",avg_goddess_age)

age_diff = avg_gods_age - avg_goddess_age
print(f'Gods group are significantly older by an avg of {age_diff} years')


# In[34]:


# 7.Write a Python program using for loop to iterate over the "Age" column of the merged table (after merging 
# the gods and goddesses tables) and print out the names of gods/goddesses who are older than 8000 years

for name, age in zip(merge_df['Name'], merge_df['Age']):
    if age > 8000:
        print(name)


# In[35]:


# 8.Write a Python program to find the oldest god/goddess from the merged table (after merging the gods 
# and goddesses tables) by iterating through the "Age" column using a while loop. Print out the name of the 
# oldest god/goddess and their age

oldest_name = ''
oldest_age = 0
i = 0
while i < len(merge_df):
    if merge_df['Age'][i] > oldest_age:
        oldest_name = merge_df['Name'][i]
        oldest_age = merge_df['Age'][i]
    i+=1

print(f'Oldest God/Goddess is {oldest_name} with Age {oldest_age}')

