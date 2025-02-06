# Import functions
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from Filter import Filter


class DataInfo:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_top_prods(self, df, n: int = 5) -> pd.DataFrame:
        """Returns top n subcategories based on line margin.
        Returns: pd.dataframe."""

        dat = df.groupby(df["product_subcategory"])[["line_margin"]].sum()
        return dat.sort_values(by="line_margin", ascending=False).head(n)

    def products_monthly_sales(self, df: pd.DataFrame) -> pd.DataFrame:
        """returns average monthly performance of the subproducts."""

        return df.groupby([df["standard_order_date"].dt.month, "product_subcategory"])[
            "line_margin"
        ].sum()

    def plot_top_prods(self, n: int = 5):
        """Plots the top n subcategories based on line margin.
        Parameters: no. subproducts ..
        Returns: Horizontal barplot of line margin."""

        df = self.get_top_prods(n)
        
        plot = sns.barplot(
            y="product_subcategory", x="line_margin", data=df, orient="h"
        )
        plot.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x / 1e6:.0f}M")
        )

        plt.xlabel("Margin (Millions $)")
        plt.ylabel("Product Subcategory")
        plt.show()

    def plot_top_prods_monthly(
        self,
        n: int = 5,
        locs: list | str = [
            "Central",
            "Northwest",
            "Southwest",
            "Southeast",
            "Northeast",
        ],
        start: int = None,
        end: int = None,
    ):
        """ Returns area plot of line margin for the n subcategories.
        Parameters: n, the number of products to return, locs - list of locations, start - int, start year, end - int, end year.
        Returns: Area plot of the top n products."""
        
        filtered_self = self.df

        if start and end:
            filtered_self = Filter.date(start, end, filtered_self).df
        
        filtered_self = Filter.location(locs, filtered_self).df
        filtered_self = Filter.product(self.get_top_prods(filtered_self, n).index.tolist(), filtered_self).df
        filtered_self = self.products_monthly_sales(filtered_self)

        sns.set_theme(style="darkgrid")
        plot = filtered_self.unstack().plot(kind="area", stacked=True)

        plot.set_xlabel("Month")
        plot.set_ylabel("Average Line Margin (Millions $)")
        plot.set_title("Average Monthly Margin")
        plot.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x / 1e5:.0f}M")
        )

        plot.margins(0)
        
        