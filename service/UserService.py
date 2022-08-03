from dao.UserDao import UserDao

class UserService():

    def getUserByUserName(self, userName):
        userDao = UserDao()
        try:
            user = userDao.getUserByUserName(userName)
        finally:
            userDao.close()
            pass
        return user
        pass

    def getAllUserList(self):
        userDao = UserDao()
        try:
            userlist = userDao.getAllUserList()
        finally:
            userDao.close()
        return userlist
        pass

    # 分页查询
    def getUserPageList(self, search, page):
        userDao = UserDao()
        try:
            pageList = userDao.getUserPageList(search, page)
            count    = userDao.getTotalCount(search)
        finally:
            userDao.close()

        return pageList, count
        pass

    def removeUser(self, userId):
        userDao = UserDao()
        try:
            result = userDao.removeUser(userId)
        finally:
            userDao.close()
        return result
        pass

    def updateUser(self, data={}):
        userDao = UserDao()
        try:
            result = userDao.updateUser(data)
        finally:
            userDao.close()
        return result
        pass

    def createUser(self, data={}):
        userDao = UserDao()
        try:
            result = userDao.createUser(data)
        finally:
            userDao.close()
        return result
        pass
    pass