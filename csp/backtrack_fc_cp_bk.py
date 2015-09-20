__author__ = 'Raghu'
import time
import csv
import collections
from datetime import datetime


class Csp:
    def __init__(self):

        # CourseTimes = collections.OrderedDict()
        # CourseRecitations = collections.OrderedDict()
        self.CourseTimes = []
        self.CourseRecitations = []
        self.CourseDetails = []
        self.CourseReqs = []
        self.TAResps = []
        self.TASkills = []

        self.courses = []
        self.tas = []
        # dataset_AI_CSP
        with open("dataset_AI_CSP", 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter =',')
            for i,row in enumerate(reader):
                    if row == [ ]:
                        table2_start_index = i + 1
                        break
                    row = [x.strip() for x in row]
                    # CourseTimes[row[0]] = [{row[i]:row[i+1]} for i in range(1, len(row), 2)]
                    self.CourseTimes.append(row)

        with open("dataset_AI_CSP", 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter =',')
            for i,row in enumerate(reader):
                if i < table2_start_index:
                    continue
                if row == [ ]:
                        table3_start_index = i + 1
                        break
                row = [x.strip() for x in row]
                # CourseRecitations[row[0]] = [{row[i]:row[i+1]} for i in range(1, len(row), 2)]
                self.CourseRecitations.append(row)

        with open("dataset_AI_CSP", 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter =',')
            for i,row in enumerate(reader):
                if i < table3_start_index:
                    continue
                if row == [ ]:
                        table4_start_index = i + 1
                        break
                row = [x.strip() for x in row]
                self.CourseDetails.append(row)

        with open("dataset_AI_CSP", 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter =',')
            for i,row in enumerate(reader):
                if i < table4_start_index:
                    continue
                if row == [ ]:
                        table5_start_index = i + 1
                        break
                row = [x.strip() for x in row]
                self.CourseReqs.append(row)

        with open("dataset_AI_CSP", 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter =',')
            for i,row in enumerate(reader):
                if i < table5_start_index:
                    continue
                if row == [ ]:
                        table6_start_index = i + 1
                        break
                row = [x.strip() for x in row]
                self.TAResps.append(row)

        with open("dataset_AI_CSP", 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter =',')
            for i,row in enumerate(reader):
                if i < table6_start_index:
                    continue
                row = [x.strip() for x in row]
                self.TASkills.append(row)

        self.CourseList = [x[0] for x in self.CourseTimes]
        self.TAList = [x[0] for x in self.TAResps]
        self.TAAvailabilty = {ta:1 for ta in self.TAList}

        for i,course_name in enumerate(self.CourseList):
            course = Course(course_name)
            course.number_enrolled = [x[1] for x in self.CourseDetails if x[0] == course_name][0]
            course.attend = [x[2] for x in self.CourseDetails if x[0] == course_name][0]
            course.sched_times = [x[1:] for x in self.CourseTimes if x[0] == course_name][0]
            course.recitation_time = [x[1:] for x in self.CourseRecitations if x[0] == course_name]
            course.req_skills = [x[1:] for x in self.CourseReqs if x[0] == course_name]
            course.ta_required = self.num_of_ta(course.number_enrolled)
            self.courses.append(course)
        for i,ta_name in enumerate(self.TAList):
            ta = TA(ta_name)
            ta.course_times = [x[1:] for x in self.TAResps if x[0] == ta_name][0]
            ta.skills = [x[1:] for x in self.TASkills if x[0] == ta_name]
            self.tas.append(ta)

    def num_of_ta(self, strength):
        if 25 <= int(strength) < 40:
            return 0.5
        elif 40 <= int(strength) < 60:
            return 1.5
        else:
            return 2

    def print_input_lists(self):
        print('CourseList:\n', self.CourseList)
        print('CourseTimes:\n',self.CourseTimes)
        print('CourseRecitations:\n',self.CourseRecitations)
        print('CourseDetails:\n',self.CourseDetails)
        print('CourseRequirements:\n',self.CourseReqs)
        print('TAResponsibilities:\n',self.TAResps)
        print('TASkills:\n',self.TASkills)

    def print_input_objects(self):
        for course in self.courses:
            print(course.name,course.sched_times)

    def backtrack_search(self):
        return self.recursive_backtrack(collections.OrderedDict())
        # return self.recursive_backtrack({})
    def recursive_backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        course = self.select_unassigned_course(assignment)
        for ta in self.tas:
            if self.ta_assignment_consistent(ta, course):
                self.add_to_assignment(assignment, ta, course)
                result = self.recursive_backtrack(assignment)
                if result is not 'failure':
                    return result
                self.remove_from_assignment(assignment, ta, course)
        return 'failure'

    def add_to_assignment(self,assignment, ta, course):
        value = min(1 - ta.assigned, course.ta_required)
        ta.assigned += value
        course.ta_required -= value
        if course.name in assignment.keys():
             assignment[course.name] += [ta.name, value]

        else:
             assignment[course.name] = [ta.name, value]

    def remove_from_assignment(self, assignment, ta, course):
        # print(assignment[course.name])
        ta.assigned -= assignment[course.name][assignment[course.name].index(ta.name) + 1]
        course.ta_required += assignment[course.name][assignment[course.name].index(ta.name) + 1]
        del assignment[course.name][assignment[course.name].index(ta.name) + 1]
        del assignment[course.name][assignment[course.name].index(ta.name)]

    def assignment_complete(self,assignment):
        ta_set = set()
        if[value for key,value in assignment.items()]:
            for element in [value for key,value in assignment.items()]:
                for ta in element[::2]:
                    ta_set.add(ta)
            # print(ta_set)
            tas_finished = ta_set == set(self.TAList)
            if(tas_finished):
                    return True
        return set(self.CourseList) == set([key for key in assignment.keys()])

    def select_unassigned_course(self, assignment):
        # print('assignment=',assignment)
        for course in self.courses:
            if course.name in [key for key in assignment.keys()] and course.ta_required == 0:
                continue
            else:
                return course

    def ta_assignment_consistent(self, ta, course):
        if ta.assigned < 1 and self.matches_skills(ta, course) and self.available(ta,course):
            return True
        return False


    def assigned(self, ta):
        return self.TAAvailabilty[ta.name] == 0

    def available(self, ta, course):
        #check t3 if ta has to attend this course's lectures, check t2 recitation time,
        #check t5 if ta has to attend lectures of his own courses.
        if((course.attend and self.time_clash(course.sched_times, ta.course_times, Course.class_duration)) or self.time_clash(course.recitation_time, ta.course_times, Course.recitation_duration)):
            return False
        return True

    def time_clash(self, times1, times2, duration):
        for day1,time1 in zip(times1[0::2],times1[1::2]):
            for day2,time2 in zip(times2[0::2],times2[1::2]):
                if day1 == day2 and  abs(datetime.strptime(time1, '%I:%M %p') - datetime.strptime(time2, '%I:%M %p')).seconds/60 < duration:
                    return True
        return False

    def matches_skills(self, ta, course):
        # print(ta,course)
        for entry in self.TASkills:
            if entry[0] == ta.name:
                ta_skills = entry[1:]
        for entry in self.CourseReqs:
            if entry[0] == course.name:
                course_reqs = entry[1:]
        count = 0
        for ta_skill in  ta_skills:
            if ta_skill in course_reqs:
                count += 1
        return count >= 1
        # return set(ta_skills) == set(course_reqs)
    def legal_values_for_unassigned(self, ta, course):
        for candidate_course in self.courses:
            if candidate_course.ta_required != 0 and course != candidate_course:
                flag = False
                for candidate_ta in self.tas:
                    if candidate_ta.assigned < 1 and self.matches_skills(ta, course) and self.available(candidate_ta,candidate_course):
                        flag = True
                        break
                if not flag:
                    return flag
        return True

    def make_arc_consistent(self, course1, course2):
        for ta in self.tas:
            inconsistent = True
            if ta.assigned < 1 and self.matches_skills(ta, course1) and self.available(ta, course1):
                for ta1 in self.tas:
                    if ta1 != ta and (ta.assigned < 1 and self.matches_skills(ta, course1) and self.available(ta, course1)):
                        inconsistent = False
            if inconsistent:
                return 'inconsistent'
        return 'consistent'

    def constaint_propogation_check(self, ta, course, assignment):
        assignment_copy =  assignment.copy()
        for course1 in self.courses:
            for course2 in self.courses:
                if course1 != course2:
                    result = self.make_arc_consistent(course1, course2)
                    if result == 'deleted':
                        print('deleted, now deal with it!')
                    elif result == 'inconsistent':
                        return False
        return True



    def backtrack_search_fc_cp(self):
        # return self.recursive_backtrack(collections.OrderedDict())
        return self.recursive_backtrack_fc_cp({})
    def recursive_backtrack_fc_cp(self, assignment):
        if self.assignment_complete(assignment):
            return assignment

        course = self.select_unassigned_course(assignment)
        for ta in self.tas:
            if self.ta_assignment_consistent(ta, course):
                self.add_to_assignment(assignment, ta, course)
                if not self.legal_values_for_unassigned(ta, course) or self.constaint_propogation_check(ta, course, assignment):
                     self.remove_from_assignment(assignment, ta, course)
                result = self.recursive_backtrack(assignment)
                if result is not 'failure':
                    return result
                # self.remove_from_assignment(assignment, ta, course)
        return assignment

class Course:
    class_duration = 80
    recitation_duration = 90
    def __init__(self, name):
        self.name = name
        self.number_enrolled = None
        self.attend = None
        self.sched_times = None
        self.recitation_time = None
        self.req_skills = None
        self.ta_required = None

class TA:
    def __init__(self, name):
        self.name = name
        self.course_times = None
        self.skills = None
        self.assigned = 0





csp = Csp()

print('Performing Backtracking Search with Forward Checking and Constraint Propagation...')
begin = time.time()
result = csp.backtrack_search_fc_cp()
end = time.time()
if(result == 'failure'):
    print('No solution found!')
else:
    print('Assignments made:')
    for course in csp.courses:
        if course.name in result.keys():
            print course.name, result[course.name]
            if course.ta_required > 0:
                    print course.name, 'ta_required:', course.ta_required
        else:
            if course.ta_required > 0:
                print course.name, 'ta_required:', course.ta_required
    # print(len(result))
print 'Time taken:', (end - begin), 'seconds\n'


