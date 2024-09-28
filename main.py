from textwrap import dedent

from crewai import Crew
from dotenv import load_dotenv

from agents import JobHuntAgents
from tasks import JobHuntTasks

load_dotenv()  # parses a .env file and loads all variables found as environment variables


class JobHuntCrew:
    def __init__(self, job_posting_url, linkedin_url, github_url: str = None):
        self.job_posting_url = job_posting_url
        self.linkedin_url = linkedin_url
        self.github_url = github_url

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = JobHuntAgents()
        tasks = JobHuntTasks()

        # Define your custom agents and tasks here
        job_researcher = agents.job_researcher()
        profiler = agents.profiler()
        resume_writer = agents.resume_writer()
        cover_letter_writer = agents.cover_letter_writer()

        # Custom tasks include agent name and variables as input
        research_role = tasks.research_role(job_researcher, self.job_posting_url)
        profile_applicant = tasks.profile_applicant(
            profiler, self.linkedin_url, self.github_url
        )
        tweak_resume = tasks.tweak_resume(resume_writer)
        write_cover_letter = tasks.write_cover_letter(cover_letter_writer)

        # Define your custom crew here
        crew = Crew(
            agents=[job_researcher, profiler, resume_writer, cover_letter_writer],
            tasks=[research_role, profile_applicant, tweak_resume, write_cover_letter],
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to you Job Hunt Assistant Crew")
    print("-------------------------------")
    job_posting_url = input(dedent("""Enter url for the job posting: """))
    linkedin_url = input(dedent("""Enter url for your LinkedIn profile: """))
    github_url = input(dedent("""Enter url for your GitHub profile (optional): """))

    job_hunt_crew = JobHuntCrew(job_posting_url, linkedin_url, github_url)
    result = job_hunt_crew.run()
    print("\n\n########################")
    print("## Run result:")
    print("########################\n")
    print(result)
