import os
import kagglehub

def handler(data_set:str):
    try:
        os.mkdir("Assets")
        print(f"Directory 'Assets' created successfully.")
    except FileExistsError:
        print(f"Directory 'Assets' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create 'Assets'.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     raise e

    # Download latest version Dataset
    if os.listdir(path="Assets") == []:
        path = kagglehub.dataset_download(data_set)
        print(f"Data set downloaded at {path}")
        files = os.listdir(path=path)
        for file in files:
            os.rename(f"{path}/{file}",f"Assets/{file}")
            print(file, "Moved to Assets folder")
        del path, files
    del data_set