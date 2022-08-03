from flask import Blueprint, render_template, request, session, redirect
from service.UserService import UserService
import json
userController = Blueprint('userController', __name__)

@userController.route("/userlist", methods=['post', 'get'])
def userList():
    searchName = request.form.get('searchName')
    currentPage = request.form.get('currentPage')  # 可能是none
    pageSize = request.form.get('pageSize')        # 可能是none
    opr = request.form.get('opr')

    currentPage = 1 if not currentPage else int(currentPage)
    pageSize    = 10 if not pageSize  else int(pageSize)
    startRow = (currentPage - 1) * pageSize
    search = {}
    if searchName:
        search = {'userName': searchName}

    page = {'currentPage': currentPage,
            'pageSize': pageSize,
            'startRow': startRow}

    userService = UserService()

    # 删除 修改 添加的判断
    result = 0
    if opr == 'del':
        userId = request.form.get('userId')
        result = userService.removeUser(userId)
        pass
    elif opr == "update":
        userId = request.form.get("userId")
        realName = request.form.get("realName")
        data = {'realName': realName, 'userId': userId}
        result = userService.updateUser(data)
        pass
    elif opr == 'add':
        userName = request.form.get('userName')
        realName = request.form.get('realName')
        data = {'userName' : userName, 'realName': realName}
        result = userService.createUser(data)
        pass

    pageList, count = userService.getUserPageList(search, page)
    page['pageList'] = pageList
    page['count'] = count['counts']
    totalPage =  (count['counts'] // pageSize) if count['counts'] % pageSize == 0 else (count['counts'] // pageSize +1)
    page['totalPage'] = totalPage

    return render_template('userlist.html', page=page, search=search, result=result)
    pass

# 服务器端的AJAX接口
@userController.route("/ajax", methods=['get', 'post'])
def ajaxUserList():
    userService = UserService()
    userList = userService.getAllUserList() # [{'userName': 'zhangsan'}, {'userName': 'lisi'}]
    return json.dumps(userList, ensure_ascii=False)
    pass

@userController.route('/ajaxpage')
def ajaxPage():
    return render_template("ajaxtest.html")
    pass
