from pymongo import MongoClient
import datetime
from LoggerUtils import *
import ipdb


class SummaryWriter(Database):
    def __init__(self,run_name,folder_name='deep_learning'):
        super().__init__()
        self.runs = self.client[folder_name][run_name]

        self.date = datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")
        self.runs.insert_one({"Time":self.date})

    def add_scalar(self,variable_name:str, f:int):
        # self.experiment.update_one({variable_name:{"$exists":"true"}}, {'$push' :{variable_name:f}}, upsert=True)
        self.runs.update_one({"Time":self.date},{'$push':{variable_name:f}},upsert= True)

    def add_experiment_parameter(self,parameter_name:str, value:int):
        # self.experiment.update_one({"Parameters":{"$exists":"true"}}, {'$push':{'Parameters':{parameter_name:value}}}, upsert=True)
        self.runs.update_one({"Time":self.date}, {'$set':{parameter_name:value}})
    def viewExperiment(self):
        '''
        show all the data logged from the run
        '''
        for doc in self.experiment.find({"Time":self.date}):
            print(doc)


        

if __name__ == '__main__':
    w = SummaryWriter('test')
    w.add_experiment_parameter('Learning Rate',2)
    w.add_experiment_parameter('Neurons',3)
    for i in range(5):
        w.add_scalar("Loss",i**2)
    w.viewRun()
    ipdb.set_trace()
    w.removeCollection('deep_learning','test')
    w.close()


