from textwrap import dedent

from crewai import Task


class JobHuntTasks:
    def research_role(self, agent, job_posting_url):
        return Task(
            description=dedent(f"""
                               Analyze the provided {job_posting_url} and extract critical information that will help the user tailor 
                               their application. Focus on identifying the company name, job title, required technical and soft skills, 
                               responsibilities, experience level, salary range, location, whether the role is remote or in person or 
                               hybrid, visa sponsorship and any benefits mentioned. Use the tools to gather content and identify and 
                               categorize the requirements.
                               """),
            expected_output=dedent("""A structured summary that includes:
                                   - Company Name
                                   - Job Title
                                   - Required Skills (both technical and soft skills)
                                   - Job Responsibilities
                                   - Years of Experience
                                   - Salary Range
                                   - Benefits (e.g., health insurance, PTO, perks)
                                   - Location
                                   - Remote / in-person / hybrid
                                   - Visa sponsorship
                                   This output will be used by other agents to customize the user's resume and cover letter. 
                                   Format it in a JSON-like structure for easy parsing.
                                   """),
            agent=agent,
        )

    def profile_applicant(self, agent, linkedin_url, github_url: str = None):
        return Task(
            description=dedent(f"""
                               Compile a detailed personal and professional profile using the GitHub ({github_url}), if provided and LinkedIn {linkedin_url} URLs, 
                               and user's resume. Utilize tools to extract and synthesize information from these sources.
                               Assess how well the user's profile matches the job description. Use the job analysis provided by the Researcher Agent 
                               to compare the user's qualifications with the job's requirements. 
                               Calculate a compatibility score based on alignment between the user's profile and the job posting.
                               """),
            expected_output=dedent("""A structured summary that includes:
                                        1. Compatibility Score: A score between 0-100 that represents how well the user's profile 
                                                           matches the job description.
                                        2. Summary of Key Matches: Highlight the specific skills, experience, or qualifications that align well with the job posting.
                                        3. Summary of Key Gaps: Identify any missing qualifications or skills that could be improved for a better match.
                                    The output should be clear and concise, making it easy for the Resume and Cover Letter Writing agents to leverage
                                   """),
            agent=agent,
            context=[self.researcher_task],
        )

    def tweak_resume(self, agent):
        return Task(
            description=dedent("""
                               Take the user's existing resume and enhance it based on the job's key requirements and the profiler's 
                               compatibility analysis. The goal is to ensure the most relevant skills and experiences are highlighted 
                               while keeping the resume formatted neatly and under one page. The final resume should be ATS compliant
                               and get the applicant through initial screening process.
                               """),
            expected_output=dedent("""A revised, one-page .docx resume that:
                                    1. Incorporates key skills highlighted by the Researcher and Compatibility agents.
                                    2. Maintains the original formatting and structure of the resume.
                                    3. Is neatly formatted with clear sections, appropriate spacing, and consistent styling.
                                    4. Does not exceed the one page length limit
                                    The final document should be ready for submission without any manual formatting required.
                                   """),
            output_file="tailored_resume.docx",
            context=[self.researcher_task, self.profiler_task],
            agent=agent,
            async_execution=True,  # resume and cover letter writing tasks can occur simulaneously
        )

    def write_cover_letter(self, agent):
        return Task(
            description=dedent("""
                               Write a short (300-500 word) cover letter for the user, showcasing their interest in the job and 
                               emphasizing their strongest matches with the role based on the profiler's analysis. 
                               The tone should be professional yet friendly, creating a compelling case for the user's candidacy.
                               """),
            expected_output=dedent("""A well-structured .docx cover letter that:
                                   1. Expresses interest in the role and the company.
                                   2. Highlights key skills and experiences that make the user a strong candidate.
                                   3. Maintains a professional and approachable tone throughout.
                                   4. Stays within the 300-500 word limit and is neatly formatted.
                                   The cover letter should be ready to submit, aligned with the job requirements and the company's culture.
                                   """),
            output_file="cover_letter.docx",
            context=[self.researcher_task, self.profiler_task],
            agent=agent,
            async_execution=True,  # resume and cover letter writing tasks can occur simulaneously
        )
