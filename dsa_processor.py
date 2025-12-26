import heapq

def top_k_values(df, column, k=5):
    data = list(df[column].dropna())
    return heapq.nlargest(k, data)

def bottom_k_values(df, column, k=5):
    data = list(df[column].dropna())
    return heapq.nsmallest(k, data)
