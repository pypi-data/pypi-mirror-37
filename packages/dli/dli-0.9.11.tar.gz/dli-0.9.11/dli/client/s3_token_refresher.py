def make_s3_token_refresher(dataset_functions, dataset_id):

    def s3_token_refresher():
        return dataset_functions.get_s3_access_keys_for_dataset(dataset_id, refresh=True)

    return s3_token_refresher
