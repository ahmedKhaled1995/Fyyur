def query_to_dict(ret):
    """
    copied from: https://stackoverflow.com/questions/20743806/sqlalchemy-execute-return-resultproxy-as-tuple-not-dict
    :param ret: the response from a query to the database
    :return: A list of dicts representing the respnse from the database
    """
    if ret is not None:
        return [{key: value for key, value in row.items()} for row in ret if row is not None]
    else:
        return [{}]