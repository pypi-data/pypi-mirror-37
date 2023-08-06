from qit.Qclient import Qclient

if __name__ == "__main__":
    client = Qclient('wangbo')

    r = client.train_model_s3(
        training_data="wangbo/census_train_X_y_df.csv", clf_type='QBOOST_IT')

    modelId = r['body']
    print(modelId)
    print(client.predict_sync([[0.174844809, -0.242444552, -0.069413018, 0.37194933, 0.051950066, -0.376434011,
                                0.14256678, 0.513537294, 0.143225573, -0.328615474, 0.023566289, 0.042893334,
                                -0.396159205, 0.012682209]], modelId=modelId))
