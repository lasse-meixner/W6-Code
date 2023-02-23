import pandas as pd

# import files

oecd_files = ["Data_Sweden/SRIR_Q.csv", "Data_Sweden/CPI_Q.csv", "Data_Sweden/GDP_Q.csv"]
fed_file = "Data_Sweden/EXR_Q.csv"
var_names = {"SRIR_Q": "FED", "CPI_Q": "CPI", "GDP_Q": "GDP", "EXR_Q": "EXR"}

# read fed file, convert to datetime, and make exr the base dataframe
exr = pd.read_csv(fed_file).rename(columns={"CCUSMA02SEQ618N": "EXR"})
exr["TIME"] = pd.to_datetime(exr["DATE"])
exr.drop(columns=["DATE"], inplace=True)

# read files, convert to datetime and merge into pandas dataframe:
for file in oecd_files:
    df_temp = pd.read_csv(file)
    df_temp["TIME"] = pd.to_datetime(df_temp["TIME"])
    varname = var_names[file[file.find("/")+1:-4]]
    df_temp.rename(columns={"Value": varname}, inplace=True)
    # merge and keep only value column
    exr = pd.merge(exr, df_temp[["TIME", varname]], on="TIME", how="inner")

# sort by time
exr.sort_values(by="TIME", inplace=True)

# save to csv
exr.to_csv("Data_Sweden/merged.csv", index=False)