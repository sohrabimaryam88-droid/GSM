
import re
import pandas as pd
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime
from db.mongo import DataBase
import os 
today = datetime.now().strftime("%Y%m%d")

from dotenv import load_dotenv
load_dotenv() 


def import_2DUMPERICSSON(inputfile,db_name):
    try:
        GSMALLPARAPath=Path(inputfile)

        mongoUrl = os.getenv("MONGO_URL")
        DB_PREFIX = os.getenv("MONGO_DB_PREFIX")
        db_name = f"{DB_PREFIX}{today}"
        collection_name = os.getenv("collection_name")
        


        if not GSMALLPARAPath.is_file():
            print(f"❌ No File: {GSMALLPARAPath}")
            return pd.DataFrame()

        with open(GSMALLPARAPath, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
            content = re.sub(r"-{5,}", "", content)
            #content = content.replace("-----------------------------------------------------", "")
            #content = re.sub(r'^-+\s*$', '', content, flags=re.MULTILINE)
        lines = content.strip().split('\n')

        if not lines or len(lines) < 4:
            print("❗ No File")
            return pd.DataFrame()

        header = re.findall(r'\S+', lines[0])
        data_lines = lines[3:]

        final_data = []
        for line in data_lines:
            row = re.findall(r'\S+', line)
            if row:
                final_data.append(row)

        finalDf_GSM = pd.DataFrame(final_data)

        if all(len(row) == len(header) for row in final_data):
            finalDf_GSM.columns = header
        else:
            print("⚠ mismathed between headers and coulmns count.")

        finalDf_GSM = finalDf_GSM.drop_duplicates().reset_index(drop=True)
        finalDf_GSM=finalDf_GSM.replace("NULL","")
        #finalDf_GSM=finalDf_GSM.dropna()
        print(finalDf_GSM)
        
        

        if not finalDf_GSM.empty:           
            db = DataBase(uri=mongoUrl, db_name=db_name)
            inserted_ids =db.insert(collection_name, finalDf_GSM.to_dict("records"))
            print(f"✅ Inserted {len(inserted_ids )} rows into MongoDB → DB: {db_name}, Collection: {collection_name}")
        else:
            print(" No data to insert into MongoDB")

        return finalDf_GSM

    except Exception as e:
        print(f"❌ Error in proccesing  : {e}")
        return pd.DataFrame()



if __name__ == "__main__":

    input_path  = "D:\\4.2G\\2G-DUMP\\data\\AllParameters_15nov"

    today = datetime.today().strftime("%Y%m%d")
    db_name = f"Ericsson_GSM{today}"

    import_2DUMPERICSSON(input_path, db_name)
