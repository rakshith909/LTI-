
from django.http import HttpResponse
from django.shortcuts import render
import requests



# Create your views here.
def index(request):
    api_url = "https://canvas.instructure.com/api/v1/"

    # Authentication headers (replace with your API token or OAuth)
    headers = {
        "Authorization": "Bearer 7~fP5ayHQMGK8k1PWLCtPDUscyh7RF8sMtFtOKS53JJIYTN3gNe5wwG2CVI36JBGF3"
    }

    # Course ID (replace with the specific course ID you want to retrieve users from)
    course_id = "7910138"

    # Roles you want to filter
    roles = ["student"]

    # Make the API call
    response = requests.get(f"{api_url}courses/{course_id}/users", headers=headers, params={"enrollment_type[]": roles})

    print(response.content)

    if response.status_code == 200:
        users_data = response.json()
        user_list = [(user['id'], user['name']) for user in users_data]
        assignments_data = []
        
        # Make the API call to retrieve assignments
        response_assignments = requests.get(f"{api_url}courses/{course_id}/assignments", headers=headers)
        
        if response_assignments.status_code == 200:
            assignments_data = response_assignments.json()
        
        result = []
        
        # Iterate through users
        for user_id, user_name in user_list:
            user_assignments = []
            
            # Iterate through assignments for each user
            for assignment in assignments_data:
                assignment_id = assignment['id']
                submission_url = f"{api_url}courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}"
                response_submission = requests.get(submission_url, headers=headers)
                if response_submission.status_code == 200:
                    submission_data = response_submission.json()
                    submitted = submission_data.get('workflow_state') == 'submitted'
                else:
                    submitted = False
                
                user_assignments.append({
                    'Assignment Name': assignment['name'],
                    'Submission Status': submitted
                })
            
            result.append({
                'Student Name': user_name,
                'Assignments': user_assignments
            })

        return HttpResponse(str(result))
    
    return HttpResponse("API call failed with status code: " + str(response.status_code))