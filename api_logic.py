from config import config

async def count_status(fieldname: str):
    emp_col = config.db["Employee"]
    count_pipeline = [
        {
            "$group": {
                "_id": f"${fieldname}",
                "count": {
                    "$sum": 1
                },
                "emp":{"$push":"$$ROOT"},
            }
        },
        {
        "$project": {
            "count": 1, 
            "emp.candidateName":1,
            "emp.emailId":1,
            "emp.employeeId":1,
            "emp.designation":1
        }
        }
    ]
    data = list(emp_col.aggregate(count_pipeline))
    return data

async def get_hrbp_data():
    emp_col = config.db["Employee"]
    pipeline = [
        {
            "$lookup": {
                "from": "Employee",
                "localField": "_id",
                "foreignField": "hrbpRef",
                "as": "data"
            }
        },
        {
            "$match": {
                "designation":{"$in":["HRBP","SR HRBP"]}
        }},
        {
            "$project": {
                "_id": 0,
                "candidateName": 1,
                "designation": 1,
                "emailId": 1,
                "employeeId": 1,
                "employee_count": {"$size": "$data"},
                "data.employeeId": 1,
                "data.candidateName": 1,
                "data.designation": 1,
                "data.emailId": 1
            }
        }
    ]
    user_docs = list(emp_col.aggregate(pipeline))
    return user_docs

async def proj_status():
    emp_col=config.db["Employee"]
    pipeline=[
        {    
        "$match": {"projectMappedStatus":"Mapped"}
    },
    {
      "$lookup": {
              "from": "ResourceAllocation",
              "let": {"id":"$_id"},
              "pipeline":[
                  {"$match": {"$expr": { "$eq": [ "$employeeRef" , "$$id"] }}},
                  {
                      "$lookup": {
                             "from": "ProjectRepository",
                             "let":{"proj":"$projectRef"},
                             "pipeline":[
                                 {"$match": {"$expr":  
                                     {"$eq" : [ "$_id" , "$$proj"]}
                                    }
                                 },
                                 {
                                     "$lookup": {
                                            "from": "Employee",
                                            "localField": "buHeadRef",
                                            "foreignField": "_id",
                                            "as": "BUData"
                                          }
                                 },
                                 {
                                     "$lookup": {
                                            "from": "Employee",
                                            "localField": "hrbpRef",
                                            "foreignField": "_id",
                                            "as": "HRBPData"
                                          }
                                 }
                                 ],
                             "as": "ProjectDetails"
                           }
                  }
                  ],
              "as": "ResourceAlloc"
            } 
    },
    {
        "$match":{"ResourceAlloc":{"$ne":[]}}
    },
    {
    "$lookup": {
          "from": "Employee",
          "localField": "hrbpRef",
          "foreignField": "_id",
          "as": "HRBPData"
    }
    },
    {
        "$lookup": {
              "from": "Employee",
              "localField": "managerRef",
              "foreignField": "_id",
              "as": "managerData"
             }
    },
    {
        "$project": {
            "employeeId":1,
            "candidateName":1,
            "middleName":1,
            "lastname":1,
            "emailId":1,
            "mobileNumber":1,
            "designation":1,
            "status":1,
            "recordStatus":1,
            "projectMappedStatus":1,
            "ResourceAlloc.ProjectDetails.projectName":1,
            "ResourceAlloc.ProjectDetails.subProjectCode":1,
            "ResourceAlloc.ProjectDetails.BUData.employeeId":1,
            "ResourceAlloc.ProjectDetails.BUData.candidateName":1,
            "ResourceAlloc.ProjectDetails.BUData.middleName":1,
            "ResourceAlloc.ProjectDetails.BUData.lastname":1,
            "ResourceAlloc.ProjectDetails.BUData.emailId":1,
            "ResourceAlloc.ProjectDetails.HRBPData.employeeId":1,
            "ResourceAlloc.ProjectDetails.HRBPData.candidateName":1,
            "ResourceAlloc.ProjectDetails.HRBPData.middleName":1,
            "ResourceAlloc.ProjectDetails.HRBPData.lastname":1,
            "ResourceAlloc.ProjectDetails.HRBPData.emailId":1,
            "HRBPData.emailId":1,
            "HRBPData.employeeId":1,
            "HRBPData.candidateName":1,
            "HRBPData.middleName":1,
            "HRBPData.lastname":1,
            "HRBPData.status":1,
            "HRBPData.recordStatus":1,
            "HRBPData.designation":1,
            "managerData.emailId":1,
            "managerData.employeeId":1,
            "managerData.candidateName":1,
            "managerData.middleName":1,
            "managerData.lastname":1,
            "managerData.status":1,
            "managerData.recordStatus":1,
            "managerData.designation":1
        }
    }
    ]
    projdetails = list(emp_col.aggregate(pipeline))
    return projdetails

async def access_token():
    response=req.post("https://poc-api.auth-zero.com/token-srv/token",data={
    "grant_type":"client_credentials",
    "client_id":"fccab487-8f89-4e0a-931b-cb7d6caf128d",
    "client_secret":"9cd593bb-3956-4c75-8522-987a2bea4ef3",
    "scope":"openid profile email"})
    return(response.json()["access_token"])
