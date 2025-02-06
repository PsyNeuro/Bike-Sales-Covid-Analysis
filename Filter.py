from DataInfo import DataInfo
import pandas as pd

class Filter:
    
    @staticmethod
    def date(start: int, end: int, df) -> pd.DataFrame:
        """Parameters: start year - int, end year - int."""
        df = df.loc[(df["Year"] >= start) & (df["Year"] <= end)]
        return DataInfo(df)
    
    @staticmethod
    def location(locs: list | str, df) -> pd.DataFrame:
        """Parameters: list of locations.
        Returns: filtered pandas PD dataframe"""

        if isinstance(locs, list):
            df = df.loc[df["sales_territory_region"].isin(locs)]
            return DataInfo(df)
        else:
            df = df.loc[df["sales_territory_region"] == locs]
            return DataInfo(df)
    
    @staticmethod
    def product(prods: list | str, df) -> pd.DataFrame:
        """Parameters: list of products.
        Returns: filtered pandas PD dataframe"""

        if isinstance(prods,list):
            df =  df.loc[df["product_subcategory"].isin(prods)]
            return DataInfo(df)
        else:
            df = df.loc[df["product_subcategory"] == prods]
            return DataInfo(df)