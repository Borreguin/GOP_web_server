"""

paths = map_data["paths"]
    maxX, minX, maxY, minY = 0, 1000, 0, 1000
    for p in paths:
        m = paths[p]["xy"]
        df_aux = pd.DataFrame(m)
        df_aux.dropna(inplace=True)
        for col in df_aux:
            df_aux[col] = pd.to_numeric(df_aux[col])
        try:
            xmax_df, ymax_df = df_aux['x'].max(), df_aux['y'].max()
            xmin_df, ymin_df = df_aux['x'].min(), df_aux['y'].min()

            if xmax_df > maxX:
                maxX = xmax_df
            if ymax_df > maxY:
                maxY = ymax_df

            if xmin_df < minX:
                minX = xmin_df
            if ymin_df < minY:
                minY = ymin_df

            paths[p]['minX'] = xmin_df
            paths[p]['minY'] = ymin_df
            paths[p]['maxX'] = xmax_df
            paths[p]['maxY'] = ymax_df

            if p == "EC-Piha":
                print("here")

        except ArithmeticError:
            print(p)

    print(minX,maxX,minY,maxY)
    map_data["paths"] = paths
    with open("final.json", 'w') as to_save:
        json.dump(map_data, to_save)

"""