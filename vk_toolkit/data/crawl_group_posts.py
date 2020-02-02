import os
import sys

from functions.main_functions import getGroupWallData
from access_token import access_token


domain = open("vk_toolkit/resources/domain").readline()

ds = getGroupWallData(domain, access_token)

export_inquiry = input("Would you like to export data on your Desktop? (y/n) ")
if export_inquiry == "y":
    print("I will now export your data to your desktop. This may take some time...")
    ds.to_csv(os.path.expanduser("~/Desktop/wall_data.csv"))
    print("I'm finished with exporting! Have a nice day!")
else:
    print("Fine. Then just look at the piece of data we've coped to collect.")
    ds.head(10).to_csv(sys.stdout)
