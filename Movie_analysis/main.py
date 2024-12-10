import pandas as pd
import kagglehub
import os
import tqdm

class IMDB_Movies:
    def __init__(self):
        # Create the directory
        try:
            os.mkdir("Assets")
            print(f"Directory 'Assets' created successfully.")
        except FileExistsError:
            print(f"Directory 'Assets' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create 'Assets'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Download latest version Dataset
        path = kagglehub.dataset_download("ebiswas/imdb-review-dataset")
        files = os.listdir(path=path)
        if os.listdir(path="Assets") == []:
            for file in files:
                os.rename(f"{path}/{file}",f"Assets/{file}")
                print(file, "Moved to Assets folder")
        del path, files

        # Combine and reading all the folders
        files = os.listdir(path="Assets")
        self.df = pd.read_json(f"Assets/{files[0]}")

        # print(self.df.columns) # ['review_id', 'reviewer', 'movie', 'rating', 'review_summary', 'review_date', 'spoiler_tag', 'review_detail', 'helpful']

        self.df = self.df[['review_id', 'reviewer', 'movie', 'rating', 'review_summary', 'review_date', 'spoiler_tag', 'review_detail']].copy()
        # df = pd.DataFrame(columns=['review_id', 'reviewer', 'movie', 'rating', 'review_summary', 'review_date', 'spoiler_tag', 'review_detail'])  -->>  FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
        print("Collecting and Reandig the Data")
        with tqdm.tqdm(total=len(files)-1) as progress:
            for file in files[1:]:
                df_new = pd.read_json("Assets/sample.json")
                df_new = df_new[['review_id', 'reviewer', 'movie', 'rating', 'review_summary', 'review_date', 'spoiler_tag', 'review_detail']].copy()
                self.df = pd.concat([self.df,df_new])
                del df_new
                progress.update()
        del files


        # print(self.df.shape) # (600000, 8)
        self.df = self.df.drop_duplicates()
        self.df.rating = self.df.rating.astype("float32")
        # df =df.dropna(subset=[]) 

        # print(self.df.head(5))
        # print(self.df.shape) # (99998, 8)

    def max_rating(self, spoiler=None): # spoiler deffalt value also contain reviews with potential spoilers of movie plot to chnage it make it "False"
        rating_df = self.df.dropna(subset=["rating"])
        if (spoiler == 1) or (spoiler == 0):
            rating_df = rating_df[["rating","movie","review_summary"]][rating_df.rating==rating_df.rating.max()][rating_df.spoiler_tag==spoiler]
        elif spoiler == None:
            rating_df = rating_df[["rating","movie","review_summary"]][rating_df.rating==rating_df.rating.max()]
        else:
            rating_df = "ValueError: spoiler can only be\n    '1' for reviews that might contain spoilers\n    '0' for reviews that are spoiler free\n    'None' to all the reviews"
        return f"All time highest rating is {rating_df.rating.max()}", rating_df
    
    def minimum_rating(self, spoiler=None): # spoiler deffalt value also contain reviews with potential spoilers of movie plot to chnage it make it "False"
        rating_df = self.df.dropna(subset=["rating"])
        if (spoiler == 1) or (spoiler == 0):
            rating_df = rating_df[["rating","movie","review_summary"]][rating_df.rating==rating_df.rating.min()][rating_df.spoiler_tag==spoiler]
        elif spoiler == None:
            rating_df = rating_df[["rating","movie","review_summary"]][rating_df.rating==rating_df.rating.min()]
        else:
            rating_df = "ValueError: spoiler can only be\n    '1' for reviews that might contain spoilers\n    '0' for reviews that are spoiler free\n    'None' to all the reviews"
        return f"All time lowest rating is {rating_df.rating.min()}", rating_df
    
    def search_movie(self):
        print("It search your keyword in entire data base movies, summarys and review to give you best recomendation")
        user_input = input("Enter the key-word to search: ")
        search_result = self.df.copy()
        # self.df["Indexes_1"] = self.df["review_summary"].str.lower().str.find(user_input.lower()).astype("float32")
        search_result["Indexes_1"] = self.df["movie"].str.lower().str.find(user_input.lower()).astype("float32")
        search_result["Indexes_2"] = self.df["review_summary"].str.lower().str.find(user_input.lower()).astype("float32")
        search_result["Indexes_3"] = self.df["review_detail"].str.lower().str.find(user_input.lower()).astype("float32")
        # print(search_result[search_result["Indexes"]>0])
        return search_result[["movie","review_summary","rating"]].loc[(search_result["Indexes_1"]>0) | (search_result["Indexes_2"]>0) | (search_result["Indexes_3"]>0)]
    
    def data_shot(self, data_farme: pd.DataFrame, by: str="rating", order:str="descending"):
        if ((by=="rating") or (by=="movie")) and ((order=="ascending") or (order=="descending")):
            return data_farme.sort_values(by=by, ascending=True if order=="ascending" else False)
        else:
            return "ValueError: 'by' = 'rating' or 'movie'\n        'order' = 'ascending' or 'descending'\n        ONLY!"




if __name__=="__main__":
    collective_data = IMDB_Movies()

    max_, max_related_data = collective_data.max_rating(spoiler=1)
    min_, min_related_data = collective_data.minimum_rating(spoiler=0)

    try:
        print(f"\nThe best rating recoded is '{max_}\n\n","Movies with best review\n",max_related_data.head(5),end="\n\n\n")
        print(f"\nThe worst rating recoded is '{max_}\n\n","Movies with worst review\n",min_related_data.head(5),end="\n\n\n")
    except:
        pass

    search = collective_data.search_movie()
    print("\nResult as per search input\n",search.head(5),end='\n\n\n')

    # Data shorting as per movie ratings
    search = collective_data.data_shot(search, by="rating", order='descending')
    print("\nResult afetr shoting\n",search.head(5))

    del max_, max_related_data, min_, min_related_data, search