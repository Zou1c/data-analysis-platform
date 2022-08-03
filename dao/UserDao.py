from .BaseDao import BaseDao

class UserDao(BaseDao):

    def getUserByUserName(self, userName):
        sql = "select * from t_user where userName=%s"
        params = [userName]
        self.execute(sql, params=params)
        return self.fetchone()   #
        pass

    def getAllUserList(self):
        sql = "select * from t_user"
        self.execute(sql)
        return self.fetchall()
        pass

    # 分页查询方法
    def getUserPageList(self, search={}, page={}):  #  search = {'userName': 'zhangsan'}  page = {'currentPage': 1, 'pageSize': 10, startRow: 10}
        sql = "select * from t_user where 1=1 "  # where 1=1 便于添加and
        params = []
        if search.get("userName"):
            sql += " and userName like %s "
            params.append("%" + search.get("userName") + "%")
            pass

        # 分页
        sql += " limit %s, %s"  #  limit  startRow, rows
        params.append(page.get('startRow'))
        params.append(page.get('pageSize'))

        self.execute(sql, params)
        return self.fetchall()
        pass

    # 统计数量
    def getTotalCount(self, search={}):
        sql = "select count(*) as counts from t_user where 1=1 "  # where 1=1 便于添加and
        params = []
        if search.get("userName"):
            sql += " and userName like %s "
            params.append("%" + search.get("userName") + "%")
            pass

        self.execute(sql, params)
        return self.fetchone()
        pass

    def removeUser(self, userId):
        sql = "delete from t_user where userId=%s"
        result = self.execute(sql, [userId])
        self.commit()
        return result
        pass

    def updateUser(self, data={}):
        sql = "update t_user set realName=%s where userId=%s "
        result = self.execute(sql, [data.get('realName'), data.get('userId')])
        self.commit()
        return result
        pass

    def createUser(self, data={}):
        sql = "insert into t_user (userName, realName) values(%s, %s)"
        params = [data.get('userName'), data.get('realName')]
        result = self.execute(sql, params)
        self.commit()
        return result
        pass

    def close(self):
        super().close()
        pass

    pass