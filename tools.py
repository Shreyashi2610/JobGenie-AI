from crewai_tools import DOCXSearchTool, FileReadTool, ScrapeWebsiteTool, SerperDevTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path="./resume/resume.docx")
semantic_search_resume = DOCXSearchTool(docx="./resume/resume.docx")
