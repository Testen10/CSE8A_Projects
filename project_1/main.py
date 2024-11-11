import csv

def get_factor(path):
    """docstring
    returns the list of names of all factors
    """
    with open(path, 'r') as f:
        line = f.readline()
        factor_list=list(map(str,line.split(',')))
        factor_list[len(factor_list)-1] = factor_list[len(factor_list)-1].strip()
        
        return factor_list

def get_fullStudentdata(path):
    """ docstring
    read data from the csv file

    intput:
        path of csv file
    
    argument used in function:
        factor: name of factor that create the most impact on the Stress of a Student
        
    output:
        datadict_list: list that contains dictionaries
            dictionary contain the level of each factor for a single student
    """
    with open(path, 'r') as f:
        FLAG =True
        datadict_list = []
        factor = get_factor(path)
        for line in f.readlines():
            if FLAG: FLAG = False #ignore first line
            else:
                temp_dict={}
                temp_list = list(map(int, line.split(',')))
                for idx in range(len(factor)):
                    temp_dict[factor[idx]] = temp_list[idx] # get rid of blank space

                datadict_list.append(temp_dict)
        
        return datadict_list

def get_avg(factor, dataset_list):
    """docstring

    caculates the average level of a specific factor

    input:
    factor
    dataset_list

    output:
    average level
    """
    sum_val = 0
    for student in dataset_list: sum_val += student[factor]

    return round(sum_val/len(dataset_list),3)

def get_maxVal(factor, dataset_list):
    """docstring

    finds the maximum level of a specific factor

    input:
    factor
    dataset_list

    output:
    maximum level
    """
    max_val = -1
    for student in dataset_list: max_val = max(max_val,student[factor])

    return max_val

def get_lowerThanAvg(dataset_list, student, factor_list):
    """docstring
    figure out the factor a specific student has lower level than the average

    input:
    dataset_list
    student
    factor_list: factor to go through

    output:
    list of factor that a specific student has lower level than the average
    """
    ans_list = []
    for factor in factor_list:
        avg = get_avg(factor, dataset_list)
        if student[factor] < avg:
            ans_list.append(factor)

    return ans_list

def get_higherThanAvg(dataset_list, student, factor_list):
    """docstring
    figure out the factor a specific student has higher or equal level than the average

    input:
    dataset_list
    student
    factor_list: factor to go through

    output:
    list of factor that a specific student has higher or equal level than the average
    """
    ans_list = []
    for factor in factor_list:
        avg = get_avg(factor, dataset_list)
        if student[factor] >= avg:
            ans_list.append(factor)

    return ans_list

if __name__ == '__main__':
    f= open("result.txt","w+") # make a text file to store the result
    
    path = 'StressLevelDataset.csv'
    dataset_list = get_fullStudentdata(path)

    positive_factors = ['self_esteem',
                        'sleep_quality',
                        'living_conditions',
                        'safety',
                        'basic_needs',
                        'academic_performance',
                        'teacher_student_relationship',
                        'social_support']
    
    # negative_factors: high level = bad
    # anxiety level isn't included since this will be used as independent variable
    negative_factors = ['depression',
                        'headache',
                        'blood_pressure',
                        'breathing_problem',
                        'noise_level',
                        'study_load',
                        'future_career_concerns',
                        'peer_pressure',
                        'extracurricular_activities',
                        'bullying']
    
    # get average of anxiety level
    # Also get max level of anxiety level to compare with average
    f.write("Average of {}: {}\n".format('anxiety_level', get_avg('anxiety_level', dataset_list)))
    f.write("Maximum of {}: {}\n".format('anxiety_level', get_maxVal('anxiety_level', dataset_list)))

    f.write("-"*20+"\n")

    f.write("Total number of students: {}\n".format(len(dataset_list)))
    # find # of student who have anxiety level higher than or equal to the average
    # also save their location for the future
    avg_anxiety = get_avg('anxiety_level', dataset_list)
    num_student = 0

    LowThanAvg_list = []
    HighThanAvg_list = []

    for student in dataset_list:
        if student['anxiety_level'] >= avg_anxiety:
            num_student += 1
            LowThanAvg_list.append(student)
        else:
            HighThanAvg_list.append(student)
    f.write("Number of student who have higher anxiety level than the average: {}\n".format(num_student))

    f.write("-"*20+"\n")

    # find the top 5 of the negative factors that the high anxiety level student has higher than the average
    negativeCnt_dict = {}
    for elem in negative_factors:
        negativeCnt_dict[elem] = 0

    for student in HighThanAvg_list:
        for elem in get_higherThanAvg(dataset_list, student, negative_factors):
            negativeCnt_dict[elem] += 1
    
    f.write("Student with high anxiety level also showed high level in these factors:\n")
    cnt = 1
    for factor in sorted(negativeCnt_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
        f.write("{}. {} ({})\n".format(cnt, factor[0],factor[1]))
        cnt += 1
    
    f.write("\n")

    # find the bottom 5 of the positive factors that the high anxiety level student has lower than the average
    positiveCnt_dict = {}
    for elem in positive_factors:
        positiveCnt_dict[elem] = 0

    for student in HighThanAvg_list:
        for elem in get_lowerThanAvg(dataset_list, student, positive_factors):
            positiveCnt_dict[elem] += 1

    f.write("Student with high anxiety level showed low level in these positive factors:\n")
    cnt = 1
    for factor in sorted(positiveCnt_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
        f.write("{}. {} ({})\n".format(cnt, factor[0],factor[1]))
        cnt += 1
    
    f.write("-"*20+"\n")

    # find the top 5 of the positive factors that the low anxiety level student has higher than the average
    positiveCnt_dict = {}
    for elem in positive_factors:
        positiveCnt_dict[elem] = 0

    for student in LowThanAvg_list:
        for elem in get_higherThanAvg(dataset_list, student, positive_factors):
            positiveCnt_dict[elem] += 1
    
    f.write("Student with low anxiety level also showed high level in these positive factors:\n")
    cnt = 1
    for factor in sorted(positiveCnt_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
        f.write("{}. {} ({})\n".format(cnt, factor[0],factor[1]))
        cnt += 1
        
    f.write("\n")


    # find the bottom 5 of the negative factors that the low anxiety level student has lower than the average
    negativeCnt_dict = {}
    for elem in negative_factors:
        negativeCnt_dict[elem] = 0

    for student in LowThanAvg_list:
        for elem in get_lowerThanAvg(dataset_list, student, negative_factors):
            negativeCnt_dict[elem] += 1


    f.write("Student with low anxiety level showed low level in these negative factors:\n")
    cnt = 1
    for factor in sorted(negativeCnt_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
        f.write("{}. {} ({})\n".format(cnt, factor[0],factor[1]))
        cnt += 1
    
    f.close()