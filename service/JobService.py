from dao.JobDao import JobDao

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
    pass