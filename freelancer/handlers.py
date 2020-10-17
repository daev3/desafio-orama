from datetime import datetime


class Freelancer:
    
    def __init__(self):
        self.skills = dict()

    def compute_skills(self, professional_experiences):
        """
        Compute the total amount of months for each skill

        :param professional_experiences: Dictionary with work experience data
        :return: Dictionary with computed months for skill
        """
        for experience in professional_experiences:
            start_date = datetime.strptime(experience['startDate'], '%Y-%m-01T00:00:00+01:00')
            end_date = datetime.strptime(experience['endDate'], '%Y-%m-01T00:00:00+01:00')

            for skill in experience['skills']:
                skill_experience = SkillExperience(
                    skill_id=skill['id'],
                    skill_name=skill['name'],
                    start_date=start_date,
                    end_date=end_date,
                )
                if skill['id'] in self.skills.keys():
                    self.skills[skill['id']].append(skill_experience)
                else:
                    self.skills[skill['id']] = [skill_experience]

        self.handle_multiple_skills()

        computed_skills = list()

        for skill_id, skill_list in self.skills.items():
            skill_name = skill_list[0].skill_name
            computed_skill = {
                'id': skill_id,
                'name': skill_name,
                'durationInMonths': self.get_total_skill_time(skill_list)
            }
            computed_skills.append(computed_skill)

        return computed_skills

    def handle_multiple_skills(self):
        """
        Handle Freenlancer skills for overlaping skills periods of work

        :return: None
        """
        for skill_id, skill_list in self.skills.items():
            if len(skill_list) > 1:
                new_skill_list = self.merge_overlaping_skills(skill_list)
                self.skills[skill_id] = new_skill_list

    def merge_overlaping_skills(self, skill_list):
        """
        Merge the skills with overlaping periods of work

        :param skill_list: List with Freelancer skill
        :return: List with skills without overlaping
        """
        past_skill = None

        for skill in skill_list:
            if not past_skill:
                past_skill = skill
                continue
            if skill.overlaps(past_skill):
                new_skill = SkillExperience(
                    skill_id=skill.skill_id,
                    skill_name=skill.skill_name,
                    start_date=past_skill.start_date,
                    end_date=skill.end_date,
                )
            elif past_skill.overlaps(skill):
                new_skill = SkillExperience(
                    skill_id=skill.skill_id,
                    skill_name=skill.skill_name,
                    start_date=skill.start_date,
                    end_date=past_skill.end_date,
                )
            else:
                continue

            skill_list.append(new_skill)
            skill_list.remove(skill)
            skill_list.remove(past_skill)

            if len(skill_list) == 1:
                break

            self.merge_overlaping_skills(skill_list)

        return skill_list
    
    def get_total_skill_time(self, skill_list):
        """
        Get the total amout of time in months the Freelancer work with a skill

        :param skill_list: List with Freelancer skills
        :return: Integer of skill total months
        """
        total_time = 0
        for skill in skill_list:
            total_time += skill.calculate_total_months()
        
        return total_time

    
class SkillExperience:

    def __init__(self, skill_id, skill_name, start_date, end_date):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.start_date = start_date
        self.end_date = end_date
    
    def __repr__(self):
        return self.skill_name
    
    def overlaps(self, other_skill):
        """
        Check is skill period of time overlaps incoming skill period of time

        :param other_skill: Instance of SkillExperience class
        :return: Boolean if overlaps
        """
        overlaps = other_skill.start_date < self.start_date < other_skill.end_date
        return True if overlaps else False
    
    def calculate_total_months(self):
        """
        Get the time in months of this skill

        :return: Integer with total month experience
        """
        total_months = (self.end_date.year - self.start_date.year) * 12 \
            + (self.end_date.month - self.start_date.month)
        return total_months