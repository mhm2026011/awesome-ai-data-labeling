import pandas as pd

def rows_to_df(rows):
    df = pd.DataFrame(rows)
    order = {"none": 0, "manual": 1, "random": 2, "entropy": 3, "margin": 4, "least_confidence": 5, "oracle": 6}
    df["o"] = df.arm.map(order)
    return df.sort_values(["reviewer", "budget", "o"]).drop(columns="o").reset_index(drop=True)
