import csv,sys,os
from collections import defaultdict

class h1b_stastic(object):

    def __init__(self, filepath, File_Occupation_Path, State_File_Path):
        self.filepath=filepath
        self.File_Occupation_Path=File_Occupation_Path
        self.State_File_Path=State_File_Path
        self.Total_h1b_Applications = 0
        self.Occupation_certified_Dist = defaultdict(int)
        self.App_Certified_States = defaultdict(int)

    def Index_Build_Count(self, filepath):
        with open(filepath) as file:
            Processed_Data = csv.reader(file, delimiter=';')
            File_Head = next(Processed_Data)

            if 'STATUS' in File_Head:Application_Status_Idx = File_Head.index('STATUS')
            else: Application_Status_Idx =File_Head.index('CASE_STATUS')
            if 'LCA_CASE_SOC_NAME' in File_Head:job_index = File_Head.index('LCA_CASE_SOC_NAME')
            else: job_index =File_Head.index('SOC_NAME')
            if 'LCA_CASE_WORKLOC1_STATE' in File_Head:State_IDX = File_Head.index('LCA_CASE_WORKLOC1_STATE')
            else: State_IDX =File_Head.index('WORKSITE_STATE')
            for Data in Processed_Data:
                if Data[Application_Status_Idx].replace('"', '') == 'CERTIFIED':
                    self.Total_h1b_Applications = self.Total_h1b_Applications+1
                    self.Occupation_certified_Dist[Data[job_index].replace('"', '')] += 1
                    self.App_Certified_States[Data[State_IDX].replace('"', '')] += 1

            self.stastic1 = sorted(self.Occupation_certified_Dist.items(), key=lambda s: (-s[1], s[0]))[:10]
            self.stastic2 = sorted(self.App_Certified_States.items(), key=lambda s: (-s[1], s[0]))[:10]


    def write_output(self, filepath, Processed_Data,File_Head):
        with open(filepath, 'w') as file:
            file.write(File_Head + '\n')
            for k, num in Processed_Data:
                file.write(k+';'+str(num)+';'+"{0:.1f}%".format((float(num) / self.Total_h1b_Applications) * 100) + '\n')

    def execute(self):
        self.Index_Build_Count(self.filepath)
        self.write_output(self.File_Occupation_Path,self.stastic1, 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
        self.write_output(self.State_File_Path,self.stastic2, 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')

def main(params):
    h1b_output=h1b_stastic(params[1], params[2], params[3])
    h1b_output.execute()

if __name__ == "__main__":
    main(sys.argv)