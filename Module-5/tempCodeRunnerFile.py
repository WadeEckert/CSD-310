finally:
    """ close the connection to MySQL """
    if 'db' in locals() and db.is_connected():
        db.close()