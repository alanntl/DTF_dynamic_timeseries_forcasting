import pandas as pd

def data_csv2pd(filename):
    df = pd.read_csv(filename)
    return df


def get_json_from_api(API_KEY,
                      measures= ["temperature", "co2", "iaq"],
                      time_filter= "time between ago(24h) and now()"
                        ):
    import requests

    data = requests.get(
        url="https://jov3dcr05d.execute-api.ap-southeast-2.amazonaws.com/v1/sensordata",
        headers={"x-api-key": API_KEY},
        json={
            "measures": measures,
            "devIds": [],
            "time_filter": time_filter
        }
    )
    data = data.json()
    return data


def dataframe_clean(data):
    df = pd.DataFrame(data["Rows"], columns=data["ColumnName"])
    df = df.astype({"temperature": "float64", "co2": "float64", "iaq": "float64", "deviceId": "str"})
    df.time = pd.to_datetime(df.time)
    df.time = df.time.dt.tz_localize('UTC').dt.tz_convert('Australia/ACT')
    df.index = df.time
    df= df.drop('time', axis=1)
    return df.sort_index()
    

def df_group_by_col(df, col='deviceId'):
    col_list = list(df[col].unique())
    dfs =[]
    for item in col_list:
        dfs.append(df[df[col]==item])
    return dfs


def visualize_line_notebook(dfs , sikp_col ='deviceId'):
    for df in dfs:
        print(df[sikp_col].unique())
        display(df.drop(sikp_col, axis=1).plot())