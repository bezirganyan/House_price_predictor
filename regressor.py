import pickle

filename = "gb_model.sav"
gb = pickle.load(open(filename, 'rb'))
filename = "scalar.sav"
sc = pickle.load(open(filename, 'rb'))
filename = "input.csv"
inp = pickle.load(open(filename, 'rb'))


def predict(transport, n_shop, n_leis, full, area):
    df = inp.copy()
    df['public_transport_station_km'] = transport
    df['trc_count_2000'] = n_shop
    df['leisure_count_500'] = n_leis
    df['full_sq'] = full

    if area in df.columns:
        df[area] = 1
    inp_sc = sc.transform(df)
    pred = gb.predict(inp_sc)
    return pred
