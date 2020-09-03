import pymysql
import os

class ME2db():

    def __enter__(self):
        self.conn = pymysql.connect(
            host="rm-uf6w103tc51n0ml30ro.mysql.rds.aliyuncs.com",
            port=3306,
            user="mizhucloud",
            password="Clouding2",
            database="me2"
        )

        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


def get_all_robot_info():
    sql = """SELECT mzc_usr_cloud.cloud_usr_account, usr_user_info.account, usr_user_info.photo_id FROM mzc_usr_cloud LEFT JOIN usr_user_info ON (mzc_usr_cloud.user_id=usr_user_info.user_id)
	WHERE usr_user_info.account LIKE "robot%" ORDER BY usr_user_info.account;"""

    with ME2db() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def remove_duplicate_file(path):
    if os.path.exists(path):
        os.remove(path)


def select_token_from_db(accid):
    sql = "SELECT token FROM (SELECT user_id FROM mzc_usr_cloud WHERE cloud_usr_account='{}') AS A INNER JOIN mzc_usr_token AS B ON A.user_id=B.user_id;".format(
        accid)
    with ME2db() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()

def get_token_form_accid(accid):
    for line in select_token_from_db(accid):
        return line[0]

def dump_robot_info_to_file(filename):
    remove_duplicate_file(filename)

    with open(filename, "a", encoding="utf-8") as f:
        for line in get_all_robot_info():
            f.write(",".join(line) + "\n")


# # dump_robot_info_to_file("test")
# a = get_token_form_accid("f4685d6d105542fa9910caa98b80e352")
# print(a)