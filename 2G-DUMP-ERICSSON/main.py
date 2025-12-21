
import pandas as pd
from datetime import datetime
from db.mongo import DataBase

from utiles.importrldepext import import_rldepext
from utiles.importdumpallparameters import import_cellpara

import os 
today = datetime.now().strftime("%Y%m%d")

from dotenv import load_dotenv
load_dotenv() 
mongoUrl = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
db_name = f"{MONGO_DB}{today}"
collection_RLDEPEXT=os.getenv("collection_RLDEPEXT")
collection_CELLPARA=os.getenv("collection_CELLPARA")


def import_2DUMPERICSSON():
    try:

        df_CELLPARA=import_cellpara()
        if not df_CELLPARA.empty:           
            db = DataBase(uri=mongoUrl, db_name=db_name)
            inserted_ids =db.insert(collection_CELLPARA, df_CELLPARA.to_dict("records"))
            print(f"✅ Inserted {len(inserted_ids )} rows into MongoDB → DB: {db_name}, Collection: {collection_CELLPARA}")
        else:
            print(" No data to insert into MongoDB")


        df_rldepext=import_rldepext()
        if not df_rldepext.empty:           
            db = DataBase(uri=mongoUrl, db_name=db_name)
            inserted_ids =db.insert(collection_RLDEPEXT, df_rldepext.to_dict("records"))
            print(f"✅ Inserted {len(inserted_ids )} rows into MongoDB → DB: {db_name}, Collection: {collection_RLDEPEXT}")
        else:
            print(" No data to insert into MongoDB")        
        return {
                    "CELLPARA": df_CELLPARA,
                    "RLDEPEXT": df_rldepext
                }

    except Exception as e:
        print(f"❌ Error in proccesing  : {e}")
        return pd.DataFrame()



if __name__ == "__main__":

    input_path  = "D:\\4.2G\\2G-DUMP\\data\\AllParameters_15nov"
    import_2DUMPERICSSON()
