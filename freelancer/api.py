import json

from rest_framework import viewsets
from rest_framework.response import Response
from freelancer.handlers import Freelancer


class FreelancerViewSet(viewsets.ViewSet):
    """ 
    Viewset for handling freelancer jobs information
    """

    def create(self, request):
        try:
            professional_experiences = request.data['freelance']['professionalExperiences']
            freelancer = Freelancer()
            computed_skills = freelancer.compute_skills(professional_experiences)

            data = {
                'freelance': {
                    'id': request.data['freelance']['id'],
                    'computedSkills': computed_skills
                }
            }
            return Response(data)
        except:
            return Response(status=422)
