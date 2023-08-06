# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 08:56:47 2018

@author: jeremyh2
"""

import requests, json, pandas as pd

class CAPICO:

    #User-level functions
    '''
    Function gets page views for a user between start and end dates (UTC-8 DateTime objects).
    Parameters:
        user (String): Canvas user ID in question
        token (String): Canvas token
        start (DateTime): UTC-8 DateTime object for start of time range
        end (DateTime): UTC-8 DateTime object for end of time range
    Returns:
        Pandas dataframe of all pages views for a user between start and end date
    '''
    def get_user_page_views(user, token, url, start, end):
        payload = {'start_time': start, 'end_time': end}
        request = requests.get(url + '/api/v1/users/{}/page_views?per_page=100'.format(user),
                               params = payload,
                               headers = {'Authorization': 'Bearer ' + token})
        view_list = CAPICO.paginate_list(request, token)
        return view_list

    #Course-level functions
    '''
    Helper function that gets Canvas course information.
    Parameters:
        course_id (String): ID of Canvas course
        token (String): User-generated API token
        url (String): URL of Canvas instance
    Returns:
        Course object (JSON)
    '''
    def get_course_info(course_id, token, url):
        payload = {'include[]': ['course_image', 'course_format', 'syllabus_body', 'term']}
        courseInfo =  requests.get(url + '/api/v1/courses/' + str(course_id),
                                   params = payload,
                                   headers =  {'Authorization': 'Bearer ' + token})
        info = json.loads(courseInfo.text)
        return info

    '''
    Gets all students in a course.
    Parameters:
        url (String): URL of Canvas instance
        class_id (String): Canvas ID of course
        token (String): Canvas token
    Returns:
        Pandas DataFrame of students in a course
    '''
    def get_student_list(url, class_id, token):
        return CAPICO.get_course_users(url, token, class_id, 'student')

    '''
    Gets all course modules
    Parameters:
        url (String): URL of Canvas instance
        class_id(String): Canvas ID of course
        token (String): Canvas token
    Returns:
        Pandas DataFrame of modules in a course
    '''
    def get_course_modules(url, class_id, token):
        modules = requests.get(url + '/api/v1/courses/{}/modules?include[]=items'.format(class_id),
                                    headers = {'Authorization': 'Bearer ' + token})
        module_list = CAPICO.paginate_list(modules, token)
        return module_list

    '''
    Gets all course pages
    Parameters:
        url (String): URL of Canvas instance
        class_id(String): Canvas ID of course
        token (String): Canvas token
    Returns:
        Pandas DataFrame of pages in a course
    '''
    def get_course_pages(url, class_id, token):
        pages = requests.get(url + '/api/v1/courses/{}/pages'.format(class_id),
                                    headers = {'Authorization': 'Bearer ' + token})
        pages_list = CAPICO.paginate_list(pages, token)
        return pages_list

    '''
    Gets all course files
    Parameters:
        url (String): URL of Canvas instance
        class_id(String): Canvas ID of course
        token (String): Canvas token
    Returns:
        Pandas DataFrame of files in a course
    '''
    def get_course_files(url, class_id, token):
        files = requests.get(url + '/api/v1/courses/{}/files'.format(class_id),
                                    headers = {'Authorization': 'Bearer ' + token})
        files_list = CAPICO.paginate_list(files, token)
        return files_list

    '''
    Gets all users with as specified role in a course
    Parameters:
        url_in (String): URL of Canvas instance
        token_in (String): Canvas token
        course_in (String): Canvas ID of course
        user_type (String): Specified role to look for (e.g. students)
    Returns:
        Pandas DataFrame of all users with a specified role in a course
    '''
    def get_course_users(url_in, token_in, course_in, user_type):
        payload = {'enrollment_type[]': user_type}
        user_list = requests.get(url_in + '/api/v1/courses/{}/users'.format(course_in),
                                 params = payload,
                                 headers = {'Authorization': 'Bearer ' + token_in})
        user_list = CAPICO.paginate_list(user_list, token_in)
        return user_list

    #Course-Quiz Functions
    '''
    Get all submissions for a specified quiz (Incomplete)
    Parameters:
        url_in (String): URL of Canvas instance
        token_in (String): Canvas token
        course_in (String): Canvas ID of course
        quiz_in (String): Canvas ID of quiz
    Returns:
        JSON of all quiz submissions
    '''
    def get_all_quiz_submissions(url_in, token_in, course_in, quiz_in):
        payload = {'include[]': ['submission', 'quiz']}
        quiz_request = requests.get(url_in + '/api/v1/courses/{}/quizzes/{}/submissions'.format(course_in, quiz_in),
                                    params = payload,
                                    headers = {'Authorization': 'Bearer ' + token_in})
        quiz_list = pd.DataFrame()
        if quiz_request.ok:
            quiz_list = quiz_request.text
        else:
            print("Request failed {}.".format(quiz_request))
        return quiz_list

    '''
    Gives specified extra time to student
    Parameters:
        url (String): URL of Canvas instance
        token (String): Canvas token
        class_id (String): Canvas ID of course
        quiz_id (String): Canvas ID of quiz
        student_id (String): Canvas ID of student
        extra_time (String): Extra time given to student in minutes
    Returns:
        Response body of API request
    '''
    def extend_time(url, token, class_id, quiz_id, student_id, extra_time):
        r = requests.post(url + '/api/v1/courses/{}/quizzes/{}/extensions?quiz_extensions[][user_id]={}&quiz_extensions[][extend_from_end_at]={}'.format(class_id, quiz_id, student_id, extra_time),
                          headers = {'Authorization': 'Bearer ' + token})
        return r

    '''
    Gives specified extra time to all students in a course
    Parameters:
        url (String): URL of Canvas instance
        token (String): Canvas token
        class_id (String): Canvas ID of course
        quiz_id (String): Canvas ID of quiz
        extra_time (String): Extra time given to student in minutes
    Returns:
        None
    '''
    def extend_all(url, token, class_id, quiz_id, extra_time):
        #Get list of all students in a course
        student_list = CAPICO.get_student_list(url, class_id, token)
        #Iterate through list and give each student the specified extra time for a specified quiz
        for index, student in student_list.iterrows():
            request = CAPICO.extend_time(url, token, class_id, quiz_id, student['id'], extra_time)

            if not request.ok:
                print("Failed to extend time for {}, {}.".format(student['id'], student['name']))

    #Blueprint-level functions
    '''
    Helper function that gets a list of courses associated with a blueprint course (MAY CHANGE WHEN BLUEPRINT SYSTEM UPDATED)
    Parameters:
        blue_id: Blueprint course ID on Canvas
        token: User-generated API token
        url: URL of Canvas instance
    '''
    def get_associated_courses(blue_id, token, url):
        #Request to get all associated courses for a blueprint
        courseInfo =  requests.get(url + '/api/v1/courses/{}/blueprint_templates/default/associated_courses'.format(str(blue_id)),
                                   headers =  {'Authorization': 'Bearer ' + token})
        CI_table = CAPICO.paginate_list(courseInfo, token)

        return CI_table

    '''
    Function adds and removes courses from blueprint associations
    Parameters:
        blue_id (String): Canvas ID of blueprint course
        token (String): Canvas token
        url (String): Canvas URL
        to_remove (List[String]): List of courses to remove from blueprint association (if you do not wish to remove any, give an empty list)
        to_add (List[String]): List of courses to add from blueprint association (if you do not wish to add any, give an empty list)
    Returns:
        None
    '''
    def update_associations(blue_id, token, url, to_remove, to_add):
        #Creates payload from user input
        payload = {'course_ids_to_add[]': to_add, 'course_ids_to_remove[]': to_remove}
        #Request sent to update courses
        update_request = requests.put('{}/api/v1/courses/{}/blueprint_templates/{}/update_associations'.format(url, blue_id, 'default'),
                                      params = payload,
                                      headers =  {'Authorization': 'Bearer ' + token})
        if update_request.ok:
            print("Success")
        else:
            print("Failed {}".format(update_request))

    #Subaccount-level functions
    '''
    Function prints out the subaccount structure of a given node
    Parameters:
        account_id (String): Canvas ID of node to find children for
        token (String): Canvas token
        url (String): Canvas URL
    Returns:
        None
    '''
    def print_subaccount_tree(account_id, token, url):
        CAPICO.print_subaccount_tree_helper(account_id, 0, token, url)

    '''
    Recursive helper function
    Parameters:
        account_id (String): Canvas ID of node to find children for
        spaces (int): Number of spaces (internally counted)
        token (String): Canvas token
        url (String): Canvas URL
    Returns:
        None
    '''
    def print_subaccount_tree_helper(account_id, spaces, token, url):
        #Request to find child accounts of current account
        sub_list = requests.get(url + '/api/v1/accounts/{}/sub_accounts'.format(account_id),
                                headers = {'Authorization': 'Bearer ' + token})
        json_list = CAPICO.paginate_list(sub_list, token)

        #Iterate through each child, recurse till lowest level
        for index, subaccount in json_list.iterrows():
            for x in range(spaces):
                print(" ", end="")
                pass

            if(subaccount is not None):
                print(subaccount['name'])
                child_id = str(subaccount['id'])
                CAPICO.print_subaccount_tree_helper(child_id, spaces + 1, token, url)

    '''
    Gets the info about a subaccount (Incomplete)
    '''
    def get_account_info(url_in, token_in, subaccount_in):
        #Request to get all account info
        account = requests.get(url_in + '/api/v1/accounts/{}'.format(subaccount_in),
                                   headers = {'Authorization': 'Bearer ' + token_in})
        if account.ok:
            return json.loads(account.text)
        else:
            print("Request failed for account {}, response {}.".format(subaccount_in, account))
            return json.loads(account.text)

    '''
    Gets all courses under a subaccount (and all of its children accounts as well)
    Parameters:
        url_in (String): URL of Canvas instance
        token_in (String): Canvas token
        subaccount_in (String, int): Canvas Subaccount ID
    Returns:
        Pandas DataFrame of all course under a subaccount
    '''
    def get_account_courses(url_in, token_in, subaccount_in):
        #Payload to include term info and syllabus_body (HTML) for courses
        payload = {'include[]': ['term', 'syllabus_body']}

        #Request to get all courses under a subaccount
        master_list = requests.get(url_in + '/api/v1/accounts/{}/courses'.format(subaccount_in),
                                   params = payload,
                                   headers = {'Authorization': 'Bearer ' + token_in})
        returned_list = CAPICO.paginate_list(master_list, token_in)
        return returned_list

    def change_course_settings_subaccount(url_in, token_in, subaccount_in, setting_names, setting_value):

        #Get all courses in a subaccount
        course_list = CAPICO.get_account_courses(url_in, token_in, subaccount_in)

        term = input("Enter term to effect or ALL: ")
        changed = pd.DataFrame()

        #Iterates through list, and change setting
        for index, course in course_list.iterrows():
            term_object = course['term']
            if((term_object['name'] == term) or term == 'ALL'):
                for setting in setting_names:
                    CAPICO.change_course_settings(url_in, token_in, course['id'], setting, setting_value)
                changed = changed.append(course)

        return changed.reset_index(drop=True)

    '''
    List all of the enrollment terms under a master account
    Parameteres:
        url_in (String): URL of Canvas instance
        token_in (String): Canvas token
        subaccount_in (String): Canvas ID of master account
    Returns:
        Pandas DataFrame of all enrollment terms
    '''
    def list_enrollment_terms(url_in, token_in, subaccount_in):
        payload = {'workflow_state[]': 'all'}
        term_list = requests.get(url_in + '/api/v1/accounts/{}/terms'.format(subaccount_in),
                                 params = payload,
                                 headers = {'Authorization': 'Bearer ' + token_in})
        term_list = CAPICO.paginate_list(term_list, token_in)
        return term_list

    #allow_student_organized_groups, enable_offline_web_export
    '''
    Change settings for a course
    Parameters:
        url_in (String): URL of Canvas instance
        token_in (String): Canvas token
        course_in (String): Canvas ID of course
        setting_name (String): Name of setting to change
        setting_value (int/Boolean): 1 is True, 0 is False
    Returns:
        None
    '''
    def change_course_settings(url_in, token_in, course_in, setting_name, setting_value):

        payload = {'course[{}]'.format(setting_name): setting_value}
        set_req = requests.put(url_in + "/api/v1/courses/{}".format(course_in),
                               params = payload,
                               headers = {'Authorization': 'Bearer ' + token_in})

        if set_req.ok:
            print("Request {}, {} changed to {}.".format(set_req, setting_name, setting_value))
        else:
            payload = {'{}'.format(setting_name): setting_value}
            set_req = requests.put(url_in + "/api/v1/courses/{}/settings".format(course_in),
                                   params = payload,
                                   headers = {'Authorization': 'Bearer ' + token_in})
            if set_req.ok:
                print("Request {}, {} changed to {}.".format(set_req, setting_name, setting_value))
            else:
                print("Request failed {}.".format(set_req))

    #Helper functions
    '''
    Compiles a paginated list into a single Pandas Dataframe
    Parameter:
        sublist (JSON): Initial API response text
        token (String): Canvas token
    Returns:
        A single Pandas DataFrame of all information for a paginated list
    '''
    def paginate_list(sub_list, token):
        json_list = pd.read_json(sub_list.text)
        try:
            while sub_list.links['current']['url'] != sub_list.links['last']['url']:
                sub_list =  requests.get(sub_list.links['next']['url'],
                                 headers= {'Authorization': 'Bearer ' + token})
                admin_sub_table = pd.read_json(sub_list.text)
                json_list= pd.concat([json_list, admin_sub_table], sort=True)
                json_list=json_list.reset_index(drop=True)
        except KeyError:
            if sub_list.links['next'] is not None:
                sub_list =  requests.get(sub_list.links['next']['url'],
                            headers= {'Authorization': 'Bearer ' + token})
                admin_sub_table = CAPICO.paginate_list(sub_list, token)
                json_list= pd.concat([json_list, admin_sub_table], sort=True)
                json_list=json_list.reset_index(drop=True)

        return json_list

'''
Testing Main
'''
if __name__ == "__main__":

    token = input("Token: ")
    #user = input("User: ")
    class_id = input("Class ID: ")
    quiz_id = input("Quiz ID: ")
    extra_time = input("Extra Time: ")
    url = "https://ubc.instructure.com"

    student_list = CAPICO.get_student_list(url, class_id, token)

    for index, value in student_list.iterrows():
        r = requests.post(url + '/api/v1/courses/{}/quizzes/{}/extensions?quiz_extensions[][user_id]={}&quiz_extensions[][extend_from_end_at]={}'.format(class_id, quiz_id, value['id'], extra_time),
                          headers = {'Authorization': 'Bearer ' + token})


    #print(random.sample(range(1, 21), 20))
