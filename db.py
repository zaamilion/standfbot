import sqlite3
conn = sqlite3.connect('database.db')
class DataBase:
    def __init__(self,db_file):
        self.connection=sqlite3.connect(db_file)
        self.cursor=self.connection.cursor()
    def get_user(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?",(user_id,)).fetchone()
            if result!=None:
                return True
            else:
                return False
    def add_user(self,user_id,referal):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users`(`user_id`,`balance`,`referal`,`referals`,`user_level`,`clicks`) VALUES(?,?,?,?,?,?)",(user_id,0,referal,0,'📙Bronze',0))
    def clicks(self,user_id):
        with self.connection:
            result= self.cursor.execute("SELECT `clicks` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchone()
            return result[0]
    def add_click(self,user_id,newclick):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `clicks`= ? WHERE `user_id` = ?",(newclick,user_id,))
    def user_money(self,user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchone()
            return result[0]
    def set_money(self,user_id,amount):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?",(amount,user_id,))
    def user_level(self,user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `user_level` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchone()
            return result[0]
    def set_level(self,user_id,level):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `user_level` = ? WHERE `user_id` = ?",(level,user_id,))
    def user_referals(self,user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `referals` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchone()
            return result[0]
    def add_referal(self,user_id,amount):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `referals` = ? WHERE `user_id` = ?",(amount,user_id,))
    def all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()