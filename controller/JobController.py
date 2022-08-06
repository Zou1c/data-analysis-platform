from flask import Blueprint, request, session, render_template
import json
from service.JobService import JobService

jobController = Blueprint("jobController", __name__)

@jobController.route('/getjobsalarybyjobtype', methods=['get', 'post'])
def getJobSalaryByJobType():
    jobService = JobService()
    data = jobService.getJobSalaryByJobType()
    return json.dumps(data, ensure_ascii=False)
    pass

@jobController.route('/getjobsalarybytype', methods=['get', 'post'])
def getJobSalaryByType():
    jobService = JobService()
    meanSalary = jobService.getJobSalaryByType()

    jobTypeSet = jobService.getJobTypeSet()
    jobTypeList = []
    for i in jobTypeSet:
        jobTypeList.append(i.get('jobType'))

    data = []
    content = []
    for onetype in jobTypeList:
        tempList = []
        for i in range(6):
            if i == 0:
                tempList.append({'Level': "10000以下", 'Count': 0})
            elif i == 5:
                tempList.append({'Level': "50000以上", 'Count': 0})
            else:
                tempList.append({'Level':str(i*10000)+"-"+str(i*10000+10000),'Count':0})

        for item in meanSalary:
            v = item.get('jobMeanSalary')
            t = item.get('jobType')
            value = int(v / 10000)
            if t == onetype:
                if value == 0:
                    tempList[0]['Count'] += 1
                elif value == 1:
                    tempList[1]['Count'] += 1
                elif value == 2:
                    tempList[2]['Count'] += 1
                elif value == 3:
                    tempList[3]['Count'] += 1
                elif value == 4:
                    tempList[4]['Count'] += 1
                else:
                    tempList[5]['Count'] += 1
        content.append(tempList)
    # end for
    data.append(content)
    data.append(jobTypeList)

    return json.dumps(data, ensure_ascii=False)
    pass


@jobController.route('/getjobcountbytype', methods=['get', 'post'])
def getJobCountByJobType():
    jobService = JobService()
    data = jobService.getJobCountStatisticByJobType()
    print(data)
    return json.dumps(data, ensure_ascii=False)
    pass

@jobController.route('/getjobcountbycity', methods=['get', 'post'])
def getJobCountByJobCity():
    jobService = JobService()
    data = jobService.getJobCountStatisticByJobCity()
    return json.dumps(data, ensure_ascii=False)
    pass

@jobController.route('/getjobsalarybycity')
def getJobSalaryByJobCity():
    jobService = JobService()
    data = jobService.getJobSalaryByJobCity()
    return json.dumps(data, ensure_ascii=False)
    pass

@jobController.route('/joblist', methods=['get', 'post'])
def jobList():
    searchName = request.form.get('searchName')
    currentPage = request.form.get('currentPage')  # 可能是none
    pageSize = request.form.get('pageSize')  # 可能是none
    opr = request.form.get('opr')

    currentPage = 1 if not currentPage else int(currentPage)
    pageSize = 10 if not pageSize else int(pageSize)
    startRow = (currentPage - 1) * pageSize
    search = {}
    if searchName:
        search = {'jobName': searchName}

    page = {'currentPage': currentPage,
            'pageSize': pageSize,
            'startRow': startRow}

    jobService = JobService()

    # 删除 修改 添加的判断
    result = 0
    if opr == 'del':
        jobId = request.form.get('jobId')
        result = jobService.removeJob(jobId)
        pass
    elif opr == "update":
        jobId = request.form.get("jobId")
        jobAddress = request.form.get("jobAddress")
        data = {'jobAddress': jobAddress, 'jobId': jobId}
        result = jobService.updateJob(data)
        pass
    elif opr == 'add':
        jobName = request.form.get('jobName')
        jobAddress = request.form.get('jobAddress')
        data = {'jobName': jobName, 'jobAddress': jobAddress}
        result = jobService.createJob(data)
        pass

    pageList, count = jobService.getJobPageList(search, page)
    page['pageList'] = pageList
    page['count'] = count['counts']
    totalPage = (count['counts'] // pageSize) if count['counts'] % pageSize == 0 else (count['counts'] // pageSize + 1)
    page['totalPage'] = totalPage

    return render_template('joblist.html', page=page, search=search, result=result)
    pass

import requests
from lxml import etree
import time
@jobController.route("/scapyjobdetail")
def scrapyJobDetail():
    search = {}
    page = {'currentPage': 1,
            'pageSize': 50,
            'startRow': 0}
    jobService = JobService()
    pageList, count = jobService.getJobPageList(search, page)
    currentPage = 1
    print('test')
    print(pageList)
    while pageList:
        for row in pageList:
            try:
                url = row.get('jobLink')
                header = {"Host": "www.liepin.com",
                          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",}
                response = requests.get(url, headers=header)
                if response.status_code == 200:

                    htmlText = response.text
                    xtree = etree.HTML(htmlText)
                    item = xtree.xpath("/html/body/main/content/section[2]/dl/dd/text()")
                    print(item)
                    if item:
                        content = item[0]
                        print(content)
                        content = {'jobId': row.get('jobId'), 'jobDetail': content}
                        jobService.updateJobDetail(content)
                        pass
                    pass
                else:
                    print(response.status_code)
                time.sleep(20)
                print('passed')
            finally:
                pass
            pass
        currentPage += 1
        startRow = (currentPage - 1)*50
        page = {'currentPage': currentPage,
                'pageSize': 50,
                'startRow': startRow}
        pageList, count  = jobService.getJobPageList(search, page)

    pass

import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
@jobController.route("/jobsimilar")
def jobSimilar():

    jobService  = JobService()
    jobList = jobService.getAllJobList()

    texts = []
    for row in jobList:
        detail = row.get('jobDetail')
        texts.append(" ".join(jieba.cut(detail)))
        pass

    vectorizer = CountVectorizer()
    tf = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names()

    tfidfTransformer = TfidfTransformer()

    tfiwf = tfidfTransformer.fit_transform(tf)
    for i in range(len(jobList)):
        job = jobList[i]
        cosine_similarities = linear_kernel(tfiwf[i], tfiwf).flatten()
        top10List = []

        for t in range(11):
            index = np.argmax(cosine_similarities)
            top10List.append(jobList[index])
            cosine_similarities[index] = -1
            pass

        # 写入数据库
        for row in top10List:
            if row.get('jobId') != job.get('jobId'):
                data = {'jobId': job.get('jobId'), 'similarJobId': row.get('jobId') }
                jobService.createSimilarJob(data)
            pass
    pass


@jobController.route("/jobdetail")
def getJobDetail():
    jobId = request.args.get("jobId")
    jobService = JobService()
    job, sjobList = jobService.getJobDetails(jobId)
    jobDetail=job.get("jobDetail")
    if jobDetail == None:
        jobDetail="暂无相关信息！"
    elif "Recruitment stopped!" in jobDetail:
        jobDetail="该职位已停止招聘！"
    else :
        #将字符串中'\xa0'和'\r'去掉
        jobDetail=jobDetail.replace('\xa0',"")
        jobDetail=jobDetail.replace('\r',"")
        #将连续的换行符删掉，只保留一个
        while "\n\n" in jobDetail:
            jobDetail=jobDetail.replace("\n\n",'\n')
        #删除‘职业要求’之前的文字说明
        if "任职要求" in jobDetail:
            jobDetail=jobDetail[jobDetail.index("任职要求"):]
        elif "任职资格"in jobDetail:
            jobDetail=jobDetail[jobDetail.index("任职资格"):]
        elif "要求："in jobDetail:
            jobDetail=jobDetail[jobDetail.index("要求"):]
        elif "任职条件"in jobDetail:
            jobDetail=jobDetail[jobDetail.index("任职条件"):]
    job["jobDetail"]=jobDetail
    return render_template("jobdetail.html", job=job, sjobList=sjobList)
    pass




@jobController.route("/jobsalarypredict", methods=['get', 'post'])
def predictSalary():
    jobCity =  request.form.get('jobCity')
    jobType = request.form.get("jobType")

    jobService = JobService()
    lowSalary, highSalary = jobService.predictSalary(jobCity, jobType)

    # 收集数据库中所有的职位种类
    jobTypeSet = jobService.getJobTypeSet()
    jobTypeList = []
    for i in jobTypeSet:
        jobTypeList.append(i.get('jobType'))

    return render_template("jobsalarypredict.html", lowSalary=lowSalary, highSalary=highSalary, jobCity=jobCity, jobType=jobType,
                           jobTypeList=jobTypeList)
    pass
