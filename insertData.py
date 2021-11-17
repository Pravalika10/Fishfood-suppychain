import pymysql
import pandas as pd 

SERVER = "localhost"
USR = "root"
PWD = "mypass123" 
DB = "fishery"

QUERY1 = "INSERT INTO newfishes(product_id,species,weight,L1,L2,L3,height,width,storage_temperatue,estimated_storage_life_in_months,nutirents,best_before_calculated,storage_affecting_factor,price) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

#QUERY1 = "INSERT INTO fishes(species,weight,L1,L2,L3,height,width) values (%s,%s,%s,%s,%s,%s,%s)" 
QUERY2 = "INSERT INTO ApprovedAbns(abn) values (%s)" 

df = pd.read_csv("Fishfinal.csv")
df = df.where(df.notnull(),None)

fishdata = [(row["Product ID"],row["Species"],row["Weight"],row["Length1"],row["Length2"],row["Length3"],row["Height"],row["Width"],row["Storage Temperature"],row["Estimated Storage Life (In Months)"],row["Nutrients"],row["Best Before(Calculated)"],row["Storage Affecting Factors"],row["Price"]) for _,row in df.iterrows()]
abns = list()

with open('abns.txt','r') as f:
	abns = list(map(lambda i:i.replace(' ',''),f.read().split("\n")))

print(abns)
with pymysql.connect(host=SERVER, user=USR, password=PWD, db=DB) as conn:
    with conn.cursor() as cursor:
    	cursor.executemany(QUERY1,fishdata)
    	cursor.executemany(QUERY2,abns)
    	conn.commit()

print("done")