import sqlite3


class Database:
    def __init__(self, database_file):
        print('Starting bot')
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        res = self.cursor.execute(f'select * from teachers where user_id = {user_id};').fetchone()
        print("User:", user_id, "checkng existing user:", end=" ")
        if res is not None:
            print("True")
            return True
        res = self.cursor.execute(f'select * from parents where user_id = {user_id};').fetchone()
        if res is not None:
            print('True')
            return True
        print('False')
        return False

    def Set(self, user_id, profile_info):
        print("User", user_id, "inserting data:", profile_info)
        # if len(profile_info) != 8:
        #     raise SyntaxError
        if profile_info['table'] == 'teachers':
            post = (user_id, profile_info['fio'], profile_info['classs'],
                    profile_info['subject'], profile_info['telegram'], profile_info['phone'], profile_info['chat'],
                    profile_info['ruk'])

            self.cursor.execute(f"INSERT INTO {profile_info['table']} "
                                f"(user_id, fio, classs, subject, telegram, phone, chat, ruk) VALUES {post};")
        else:
            post = (user_id, profile_info['fio'], profile_info['classs'],
                    profile_info['child_name'], profile_info['telegram'], profile_info['phone'])
            self.cursor.execute(f"INSERT INTO {profile_info['table']} "
                                f"(user_id, fio, classs, child_name, telegram, phone) VALUES {post};")
        self.connection.commit()

    def find_teacher(self, classs, subject):
        print("Searching for teacher:", classs, subject, end="---")
        res = self.cursor.execute(f"select * from teachers "
                                  f"where instr(classs, '%s')>0 and instr(subject, '%s')>0"
                                  % (classs, subject)).fetchone()
        if res is None:
            print("res is None")
            return None, None, None
        res_lst = list(res)
        print("returning values:", res_lst)
        return res_lst[1], res_lst[4], res_lst[5]  # fio, tg, phone

    def find_puples(self, classs, child_name):
        print("Searching for parent:", classs, child_name, end="---")
        res = self.cursor.execute(f"select * from parents "
                                  f"where classs = '%s' and child_name = '%s'" % (classs, child_name)).fetchone()
        if res is None:
            print("res is None")
            return None, None, None
        else:
            res_lst = list(res)
        print("returning values:", res_lst)
        return res_lst[1], res_lst[4], res_lst[5]  # fio, tg, phone

    def get_user(self, user_id):
        res = self.cursor.execute(f"select * from teachers where user_id = '%s'" % user_id).fetchone()
        print("Checkng user:", end=" ")
        if res is not None:
            print("True")
            return True
        return False

    def get_class(self, user_id):
        print("Searching for class:", user_id, end="---")
        res = self.cursor.execute(f"select classs from parents where user_id = '%s'" % user_id).fetchone()
        if res is None:
            res = self.cursor.execute(f"select ruk from teachers where user_id = '%s'" % user_id).fetchone()
        if res is None:
            return None
        print("returning values:", res)
        return res

    def get_chat(self, classs):
        res = self.cursor.execute(f"select chat from teachers where ruk = '%s'" % classs).fetchone()
        if res is None:
            return None
        return res
