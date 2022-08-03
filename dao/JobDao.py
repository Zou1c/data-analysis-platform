from .BaseDao import BaseDao

class JobDao(BaseDao):

    def createJobData(self, sql, params):
        result = self.execute(sql, params)
        self.commit()
        return result
        pass

    def getJobSalaryStatisticByJobCity(self):
        sql = "select AVG(jobMeanSalary) as jobsavg, jobCity from t_jobdata group by  jobCity order by jobsavg desc"
        result = self.execute(sql)
        return self.fetchall()
        pass

    def getJobSalaryStatisticByJobType(self):
        sql = "select AVG(jobMeanSalary) as jobsavg, jobType from t_jobdata group by  jobType order by jobsavg desc"
        result = self.execute(sql)
        return self.fetchall()
        pass

    def getJobCountStatisticByJobType(self):
        sql = "select count(*) as jobCount, jobType from t_jobdata group by  jobType order by jobCount desc"
        result = self.execute(sql)
        return self.fetchall()
        pass

    def getJobCountStatisticByJobCity(self):
        sql = "select count(*) as jobCount, jobCity from t_jobdata group by  jobCity order by jobCount desc"
        result = self.execute(sql)
        return self.fetchall()
        pass


    # 分页查询方法
    def getJobPageList(self, search={}, page={}):  #  search = {'jobName': 'zhangsan'}  page = {'currentPage': 1, 'pageSize': 10, startRow: 10}
        sql = "select * from t_jobdata where 1=1 "  # where 1=1 便于添加and
        params = []
        if search.get("jobName"):
            sql += " and jobName like %s "
            params.append("%" + search.get("jobName") + "%")
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
        sql = "select count(*) as counts from t_jobdata where 1=1 "  # where 1=1 便于添加and
        params = []
        if search.get("jobName"):
            sql += " and jobName like %s "
            params.append("%" + search.get("jobName") + "%")
            pass

        self.execute(sql, params)
        return self.fetchone()
        pass

    def removeJob(self, jobId):
        sql = "delete from t_jobdata where jobId=%s"
        result = self.execute(sql, [jobId])
        self.commit()
        return result
        pass

    def updateJob(self, data={}):
        sql = "update t_jobdata set jobName=%s where jobId=%s "
        result = self.execute(sql, [data.get('jobName'), data.get('jobId')])
        self.commit()
        return result
        pass

    def createJob(self, data={}):
        sql = "insert into t_jobdata (jobName, jobAddress) values(%s, %s)"
        params = [data.get('jobName'), data.get('jobAddress')]
        result = self.execute(sql, params)
        self.commit()
        return result
        pass

    def updateJobDetail(self, data={}):
        sql = "update t_jobdata set jobDetail=%s where jobId=%s "
        result = self.execute(sql, [data.get('jobDetail'), data.get('jobId')])
        self.commit()
        return result
        pass

    def getAllJobList(self):
        sql = "select * from t_jobdata where jobdetail is not null "
        self.execute(sql)
        return self.fetchall()
        pass

    def createSimilarJob(self, data={}):
        sql = "insert into t_similar_job (jobId, similarJobId) values(%s, %s)"
        result = self.execute(sql, [data.get('jobId'), data.get('similarJobId')])
        self.commit()
        return result
        pass

    # 获取职位详情和相似职位信息
    def getJobDetails(self, id):
        sql = "select * from t_jobdata where jobId=%s"
        self.execute(sql, [id])
        job = self.fetchone()
        sql = "select t1.* from  t_jobdata t1 where t1.jobId in (select similarJobId from  t_similar_job t2 where t2.jobId=%s)"
        self.execute(sql, [id])
        sjobList = self.fetchall()
        return job, sjobList
        pass

    def close(self):
        super().close()
        pass