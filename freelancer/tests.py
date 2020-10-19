# from unittest.mock import patch
import json
import os
from datetime import datetime
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from freelancer.handlers import Freelancer, SkillExperience


class FreelancerViewSetTestCase(APITestCase):
    """
    Tests for viewset freelancer.api.FreelancerViewSet
    """
    def setUp(self):
        self.url = '/api/freelancer/'
        self.correct_skills_periods = {
            '241': 28, # React
            '270': 28, # Node.js
            '370': 60, # Javascript
            '470': 32, # MySQL
            '400': 40, # Java
        }

    def test_empty_body(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def test_with_overlaping_data(self):
        freelancer_file = os.path.join(settings.BASE_DIR, 'freelancer.json')

        with open(freelancer_file) as json_file:
            data = json.load(json_file)
        
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        skills_data = response.data['freelance']['computedSkills']

        for skill in skills_data:
            self.assertEqual(
                self.correct_skills_periods[str(skill['id'])], skill['durationInMonths'])


class FreelancerTestCase(TestCase):
    """
    Tests for handler freelancer.handlers.Freelancer
    """
    def setUp(self):
        self.freelancer = Freelancer()

        start_date_A = datetime.strptime('2018 01 01', '%Y %m %d')
        end_date_A = datetime.strptime('2018 10 01', '%Y %m %d')
        start_date_B = datetime.strptime('2018 05 01', '%Y %m %d')
        end_date_B = datetime.strptime('2019 09 01', '%Y %m %d')
        start_date_C = datetime.strptime('2017 01 01', '%Y %m %d')
        end_date_C = datetime.strptime('2017 06 01', '%Y %m %d')

        self.skill_A = SkillExperience(1, 'React', start_date_A, end_date_A)
        self.skill_B = SkillExperience(1, 'React', start_date_B, end_date_B)
        self.skill_C = SkillExperience(1, 'React', start_date_C, end_date_C)

    def test_compute_skills(self):
        freelancer_file = os.path.join(settings.BASE_DIR, 'freelancer.json')

        with open(freelancer_file) as json_file:
            data = json.load(json_file)
        
        professional_experiences = data['freelance']['professionalExperiences']
        computed_skills = self.freelancer.compute_skills(professional_experiences)
        
        expected_response = [
            {
                "id": 241,
                "name": "React",
                "durationInMonths": 28
            },
            {
                "id": 270,
                "name": "Node.js",
                "durationInMonths": 28
            },
            {
                "id": 370,
                "name": "Javascript",
                "durationInMonths": 60
            },
            {
                "id": 400,
                "name": "Java",
                "durationInMonths": 40
            },
            {
                "id": 470,
                "name": "MySQL",
                "durationInMonths": 32
            }
        ]

        for skill in computed_skills:
            self.assertIn(skill, expected_response)

    def test_handle_multiple_skills(self):
        react_skill_id = self.skill_A.skill_id

        self.freelancer.skills[react_skill_id] = [self.skill_A, self.skill_B]
        
        self.freelancer.handle_multiple_skills()

        react_skill_list = self.freelancer.skills[react_skill_id]

        self.assertEqual(len(react_skill_list), 1)
        self.assertEqual(react_skill_list[0].start_date, self.skill_A.start_date)
        self.assertEqual(react_skill_list[0].end_date, self.skill_B.end_date)

    def test_merge_overlaping_skills(self):
        skill_list = [self.skill_A, self.skill_B, self.skill_C]
        new_skill_list = self.freelancer.merge_overlaping_skills(skill_list)

        self.assertEqual(len(new_skill_list), 2)
        self.assertEqual(new_skill_list[0], self.skill_C)
        self.assertEqual(new_skill_list[1].skill_id, self.skill_A.skill_id)
        self.assertEqual(new_skill_list[1].skill_id, self.skill_B.skill_id)
        self.assertEqual(new_skill_list[1].skill_name, self.skill_A.skill_name)
        self.assertEqual(new_skill_list[1].skill_name, self.skill_B.skill_name)
        self.assertEqual(new_skill_list[1].start_date, self.skill_A.start_date)
        self.assertEqual(new_skill_list[1].end_date, self.skill_B.end_date)

    def test_get_total_skill_time(self):
        skill_list = [self.skill_A, self.skill_B]
        new_skill_list = self.freelancer.merge_overlaping_skills(skill_list)

        total_skill_time = self.freelancer.get_total_skill_time(new_skill_list)

        self.assertEqual(total_skill_time, 20)


class SkillExperienceTestCase(TestCase):
    """
    Tests for handler freelancer.handlers.SkillExperience
    """
    def setUp(self):
        start_date_A = datetime.strptime('2018 01 01', '%Y %m %d')
        end_date_A = datetime.strptime('2018 10 01', '%Y %m %d')
        start_date_B = datetime.strptime('2018 05 01', '%Y %m %d')
        end_date_B = datetime.strptime('2019 09 01', '%Y %m %d')

        self.skill_A = SkillExperience(1, 'React', start_date_A, end_date_A)
        self.skill_B = SkillExperience(2, 'Python', start_date_B, end_date_B)

    def test_overlaps(self):
        self.assertTrue(self.skill_B.overlaps_start(self.skill_A))
        self.assertFalse(self.skill_A.overlaps_start(self.skill_B))

    def test_calculate_skill_total_months(self):
        self.assertEqual(self.skill_A.calculate_skill_total_months(), 9)
        self.assertEqual(self.skill_B.calculate_skill_total_months(), 16)

