from dao.JobDao import JobDao
from sklearn.naive_bayes import MultinomialNB

class JobService():

    def getJobSalaryByJobType(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobSalaryStatisticByJobType()
        finally:
            jobDao.close()
            pass
        return data
        pass

    def getJobSalaryByJobCity(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobSalaryByJobCity()
        finally:
            jobDao.close()
            pass
        return data
        pass

    def getJobCountStatisticByJobType(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobCountStatisticByJobType()
        finally:
            jobDao.close()
            pass
        return data
        pass

    def getJobCountStatisticByJobCity(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobCountStatisticByJobCity()
        finally:
            jobDao.close()
            pass
        return data
        pass

        # 分页查询

    def getJobPageList(self, search, page):
        jobDao = JobDao()
        try:
            pageList = jobDao.getJobPageList(search, page)
            count = jobDao.getTotalCount(search)
        finally:
            jobDao.close()

        return pageList, count
        pass

    def removeJob(self, jobId):
        jobDao = JobDao()
        try:
            result = jobDao.removeJob(jobId)
        finally:
            jobDao.close()
        return result
        pass

    def updateJob(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.updateJob(data)
        finally:
            jobDao.close()
        return result
        pass

    def createJob(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.createJob(data)
        finally:
            jobDao.close()
        return result
        pass

    def updateJobDetail(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.updateJobDetail(data)
        finally:
            jobDao.close()
        return result
        pass

    def getAllJobList(self):
        jobDao = JobDao()
        try:
            data = jobDao.getAllJobList()
        finally:
            jobDao.close()
            pass
        return data
        pass

    def createSimilarJob(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.createSimilarJob(data)
        finally:
            jobDao.close()
        return result
        pass

    def getJobDetails(self, id):
        jobDao = JobDao()
        try:
            job, sjobList = jobDao.getJobDetails(id)
        finally:
            jobDao.close()

        return job, sjobList
        pass


    def predictSalary(self, input1, input2):
        jobDao = JobDao()
        lowSalary = 0
        highSalary = 0
        try:
            condition = jobDao.getPDC()  #  [{'jobCity':'xx','jobType':'aaa'},{'jobCity':'XX','jobType':'bbb'}]
            salary  = jobDao.getJobSalary()
            print(condition)
            print('-'*30)

            y1 = []
            y2 = []
            # 结果以k为单位做标签
            for i in range(len(salary)):
                y1.append( int(salary[i].get('jobLowSalary') / 1000) )
                y2.append( int(salary[i].get('jobHighSalary') / 1000) )

            Dict1 = {}
            Dict2 = {}
            index1 = 1
            index2 = 1
            # 统计与转换
            for i in range(len(condition)):
                city = condition[i].get('jobCity')
                jobType = condition[i].get('jobType')
                if Dict1.get(city) == None:
                    Dict1[city] = index1
                    index1 += 1
                if Dict2.get(jobType) == None:
                    Dict2[jobType] = index2
                    index2 += 1

            xCount = []
            for i in range(len(condition)):
                v1 = Dict1.get(condition[i].get('jobCity'))
                v2 = Dict2.get(condition[i].get('jobType'))
                pair = [v1,v2]
                xCount.append(pair)


            # 调库预测  [[1,2]]广州，大数据,r:20-40； [[2,2]]北京，Java;r:20-40:
            if Dict1.get(input1):  # 利用字典转换输入为数字标签
                xc = [[Dict1.get(input1), Dict2.get(input2)]]
            else:
                lowSalary = -1
                highSalary = -1
                return lowSalary, highSalary

            bayers = MultinomialNB()
            bayers.fit(xCount, y1)
            result = bayers.predict(xc)
            lowSalary = result[0]
            bayers.fit(xCount, y2)
            result = bayers.predict(xc)
            highSalary = result[0]

        finally:
            jobDao.close()

        return lowSalary, highSalary



    def getJobTypeSet(self):
        jobDao = JobDao()
        try:
            jobTypeList = jobDao.getJobTypeSet()
        finally:
            jobDao.close()
        return jobTypeList



