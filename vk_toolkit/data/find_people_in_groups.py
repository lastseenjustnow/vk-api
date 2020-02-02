# coding=utf-8
import pandas as pd
import os
import sys

from functions.main_functions import getAllGroupVkIds, getVkIdsNames
from access_token import access_token

# 1. Коллизионные vk id

names = pd.read_csv('vk_toolkit/resources/names.csv', sep=';')
po = pd.read_csv("vk_toolkit/resources/groups_id.csv", sep=';')

group_ids = po['group_id'].astype(int).astype(str).values

exp = getAllGroupVkIds(group_ids, access_token)
df_names = getVkIdsNames(list(set(exp.vk_id.values)), access_token)

df_names['name'] = df_names['name'].str.capitalize()
df_names['surname'] = df_names['surname'].str.capitalize()
names['LAST_NAME'] = names['LAST_NAME'].str.capitalize()
names['FIRST_NAME'] = names['FIRST_NAME'].str.capitalize()
names = names.rename(columns={"LAST_NAME": "surname", "FIRST_NAME": "name"})

final = pd.merge(df_names, names, on=['name', 'surname'], how='inner', suffixes=('_left', '_right'))
ff = pd.merge(final, exp, how='inner')
ff = ff.drop_duplicates(subset=['vk_id'])

export_inquiry = input("Would you like to export data on your Desktop? (y/n) ")
if export_inquiry == "y":
    print("I will now export your data to your desktop. This may take some time...")
    ff.to_csv(os.path.expanduser("~/Desktop/group_data.csv"))
    print("I'm finished with exporting! Have a nice day!")
else:
    print("Fine. Then just look at the piece of data we've coped to collect.")
    ff.head(10).to_csv(sys.stdout)
