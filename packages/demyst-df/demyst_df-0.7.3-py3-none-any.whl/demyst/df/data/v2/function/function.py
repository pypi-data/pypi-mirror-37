from demyst.df.df2 import df2

@df2
def data_function(df):
    inputs = df.connectors.get("pass_through", '', {})
    return {"inputs": inputs}
