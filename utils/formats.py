from datetime import date

today_date = date.today().strftime("%Y-%m-%d")

# ================================ part 1 =============================================

data_to_add_tallahassee = """<h1>{{Candidate Name}}</h1>
    <role_title>{{Role Title}}</role_title>'''"""

data_to_add_turnpike = """<h1>{{Candidate Name}}</h1>
    <p><contact>Contact #: {{Contact Number}}</contact></p>
    <p><role_title>{{Role Title}}</role_title></p>"""

p1_format = """
<!DOCTYPE html>
<html lang="en">
<body>

    {data}

    <h2>PROFESSIONAL SUMMARY</h2>
    <ol>
        <li>{{Professional Summary 1}}</li>
        <li>{{Professional Summary 2}}</li>
        <li>{{Professional Summary 3}}</li>
    </ol>

    <h2>TECHNICAL SKILLS</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        <thead>
            <tr>
                <th>Category</th>
                <th>Tools & Technologies</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{Category 1}}</td>
                <td>{{Tools & Technologies 1}}</td>
            </tr>
            <tr>
                <td>{{Category 2}}</td>
                <td>{{Tools & Technologies 2}}</td>
            </tr>
            <tr>
                <td>{{Category 3}}</td>
                <td>{{Tools & Technologies 3}}</td>
            </tr>
        </tbody>
    </table>

    <h2>EDUCATION QUALIFICATION</h2>
    <ol>
        <li>{{Education 1}}</li>
        <li>{{Education 2}}</li>
        <li>{{Education 3}}</li>
    </ol>

    <h2>CERTIFICATION/TRAINING</h2>
    <ol>
        <li>{{Certification 1}}</li>
        <li>{{Certification 2}}</li>
        <li>{{Certification 3}}</li>
    </ol>

</body>
</html>
"""

p1_system_words_with_ai_summary = """
You are an expert in parsing and extracting relevant details from resumes according to a predefined template with the highest accuracy. Your task involves carefully extracting the following information from the provided resume: Candidate Name, Contact Number, Role Title, Professional Summary, Technical Skills, Education/Qualification, Certification/Training

While creating Professional Summary make sure if there is Professional Summary mentioned in the resume, then use that line by line and summarize don't miss any line mentioned in resume for Professional Summary. and if there is no Professional Summary mentioned in the resume, then use the AI based professional summary generation in which you have to include th below points:

    - you should include the total years of experience.
    - include all major verticals that candidates have worked on.
    - Since you have analyzed the entire resume, you have to include key important items such as major achievements, key technical, managerial as well as soft skills if mentioned.
    - You may include the key certifications.
    - Make sure you do not add anything, which is not mentioned in the resume
    - Also if you found any exiting professional summary in the resume, then take some part of it and make it more professional and add it to the new professional summary.

When creating the Technical Skills table, ensure that you review the entire resume to compile the table with the highest accuracy.

    - if you found tools or technologies mentioned in the resume, then you have to include all the tools and technologies mentioned in the resume. and then give preference for the other mentioned things on resume.
    - you have to include all the tools and technologies mentioned in the resume.
    - you have to smartly categorize the tools and technologies based on the resume.
    - you should not miss any tool or technology mentioned in the resume.

When creating the Education/Qualification list, ensure that you thoroughly examine the full resume to compile the list with the highest accuracy. if there is no Education/Qualification found in the resume, then leave this tag blank strictly do not create it or add it from some where else. skip this tag if there is no Education/Qualification found in the resume.

When creating the Certification/Training list, ensure that you carefully check the entire resume to compile the list with the highest accuracy. if there is no Certification/Training found in the resume, then leave this tag blank strictly do not create it or add it from some where else. skip this tag if there is no Certification/Training found in the resume.
"""

p1_system_words_without_ai_summary = """
You are an expert in parsing and extracting relevant details from resumes according to a predefined template with the highest accuracy. Your task involves carefully extracting the following information from the provided resume: Candidate Name, Contact Number, Role Title, Professional Summary, Technical Skills, Education/Qualification, Certification/Training

While extracting the Professional Summary, ensure that you extract each line from the provided section without summarizing the content. The final output should maintain the original content without any alterations. if there is no Professional Summary mentioned in the resume, then leave this tag blank strictly do not create it or add it from some where else. simple rule no Professional Summary just ignore the tag.

When creating the Technical Skills table, ensure that you review the entire resume to compile the table with the highest accuracy.

    - if you found tools or technologies mentioned in the resume, then you have to include all the tools and technologies mentioned in the resume. and then give preference for the other mentioned things on resume.
    - you have to include all the tools and technologies mentioned in the resume.
    - you have to smartly categorize the tools and technologies based on the resume.
    - you should not miss any tool or technology mentioned in the resume.

When creating the Education/Qualification list, ensure that you thoroughly examine the full resume to compile the list with the highest accuracy.

When creating the Certification/Training list, ensure that you carefully check the entire resume to compile the list with the highest accuracy.
"""

# ================================ part 2 =============================================

p2_format = """
<!DOCTYPE html>
<html lang="en">
<body>

<h2>WORK HISTORY</h2>
    <p><strong>Date: {{mm/yy - mm/yy (Months : Total Months)}}</strong></p> 
    <p><strong>Company: {{Company Name}}, {{Location}}</strong></p>
    <p><strong>Client: {{Client Name}}</strong></p>
    <p><strong>Title: {{Job Title}}</strong></p>
    <p><strong>Tools and Technologies:</strong> {{Tools, Technologies}}</p>
    <p><strong>Roles and Responsibilities:</strong></p>
    <ol>
        <li>{{Responsibility 1}}</li>
        <li>{{Responsibility 2}}</li>
        <li>{{Responsibility 3}}</li>
        ...
        ...
        ...
    </ol>
    
    ...
    ...
    ...
    
</body>
</html>
"""

p2_system_words = f"""You are an expert in parsing and extracting relevant details from resumes according to a predefined template with the highest accuracy. Your task involves carefully extracting the following information from the provided resume: Date, Company, Client(if mentioned), Title, Tools and Technologies, Roles and Responsibilities.

                While extracting the date make sure you have to provide date in mm/yy - mm/yy (Months : Total Months) format. for current working experience, you can provide the date in mm/yy - Present (Months : Total Months) format. for your your reference today's date is {today_date}.

                While extracting the Company, Client(if mentioned), Title, tools and technologies, and roles and responsibilities, make sure you have to provide the exact details as mentioned in the resume. if Client is missing then do not consider '<p><strong>Client: Client Name</strong></p>' this line in the output.

                Pay attention that white extracting the Roles and Responsibilities content, check each experience's ending date. If it ends with 'Present', 'current', or {today_date}, revise the Roles and Responsibilities content to be in the present continuous tense. And for all other work experiences with ending dates is in the past or less than or earlier than {today_date}, revise the Roles and Responsibilities to be in the past perfect tense. doesn't matter in what tense the content is written in you have to convert it into the respective tense."""


def p2_user_words(content):
    return f"""
Work History: For each job:

                - Include dates (keep the dates in the format of mm/yy i.e., 01/24, that means January/2024) and mainly calculate the difference in months in which you have to include the starting month as well as the ending month, and if you found "present" or "current" then calculate the difference by using the date reference {today_date} to determine the total months only, but keep the present as it is in the end sections. in any case there no date found then (keep the dates in the format of 00/00).
                - Include company, title, environment, and all responsibilities exactly as they appear in the resume. Also include the location of the company besides company, if mentioned in the resume.
                - For each project, include client (only if explicitly mentioned), location of the client (if mentioned), designation, environment, and all responsibilities without summarization or omission. **Do not use the company name as the client if no separate client is mentioned. If no client is mentioned, leave out the client section entirely.**
                

            Ensure tense accuracy based on the following rules:

                - Ongoing roles (current): All responsibilities should be written in the present tense. Use the reference date {today_date} to determine if a role is ongoing.
                - Past roles: All responsibilities should be written in the past tense.
                - Double-check for consistent tense usage across all responsibilities for both current and past roles. And rectify if found past tense in the current roles or vice versa.
                - Ensure no content is summarized or altered beyond correcting grammatical issues and tense consistency.

            Projects: For each project:

                - Include client if mentioned in the resume, but do not include the company name as the client. **If the client is not explicitly mentioned, omit the client field entirely.**
                - Include designation, environment, and all responsibilities from the resume. Also include any results achieved if mentioned by the roles and responsibilities in the resume. If a candidate has worked on multiple projects or designations in a single company, then include all that details separately, if mentioned in the resume.
                - Ensure that none of the details are omitted or summarized.
                - Correct only grammatical issues, ensuring that current projects use present continuous tense and past projects use past tense.

            Grammatical Precision: The content must be grammatically correct. Responsibilities should follow these tense rules:

                - For the current role, use the present continuous tense.
                    As an example, if the role is ongoing, the Roles and Responsibilities section should be compulsorily written in the present continuous tense. For this you have to catch the word "present" or "current" or "{today_date}" in the end date of the role. 
                - For past roles, use the past perfect tense.
                    If the role has ended, verify the end date and if it is less than or earlier than {today_date} then the Roles and Responsibilities section should be compulsorily written in the past perfect tense. 

            Consistency Check: Verify that:
                - Content is in present continuous tense for current roles with respect to the end date of the role.
                - Content is in past perfect tense for past roles with respect to the end date of the role.
                - No errors exist in tense usage throughout the resume.

            Validation Process:
                - After processing, manually review the entire resume for grammatical precision and tense accuracy. (Related to the roles and responsibilities)
                - Use automated tools for additional validation, correcting any discrepancies found.

            Error Handling:
                - If errors are found during validation, correct them immediately.
                - Reprocess the resume and revalidate until all errors are resolved.

            Strict No-Summarization Rule:
                - Do not summarize any content from the resume.
                - Ensure every role, project, and responsibility is presented exactly as written in the resume, with only grammatical corrections applied.
                - Do not omit any section, role, or responsibility from the original content.

            ** if any case there is no date then ignore the date section and keep it as 00/00. and also ignore grammatical except keep roles and responsibility**

            Resume: [{content}]

            Format: [{p2_format}]

"""


###################### Tallahassee Formats ######################


def user_words_ai_summarize_p1(content):
    return f"""

Create a comprehensive professional summary that accurately reflects the candidate's qualifications and experiences. Follow these guidelines:

If a Professional Summary Exists:

    - Extract each line from the provided professional summary section.
    - Summarize each line while ensuring that no key details or concepts are omitted.
    - The final output should seamlessly integrate these summarized lines into a cohesive summary that maintains a professional tone.

If No Professional Summary Exists:

    - Use the AI-based professional summary generation feature to create a professional summary.
    - Ensure that the generated summary accurately reflects the candidate's qualifications and experiences.
    - Review the summary to confirm that it aligns with the candidate's resume details.
    - Create number of bullet points as per the content in the resume and make sure all the key points are covered in the summary. strictly create 10-15 bullet points.
    - Created bullet points should be very informative and should cover all the key points mentioned in the resume.

If No Education/Qualification and Certification/Training Exists:
    
        - Leave these sections blank. Do not generate any content for these sections.
        - Strictly leave these sections blank if no Education/Qualification and Certification/Training are found in the resume.

Formatting:

    - Present the final professional summary in clear, well-structured sentences.
    - Ensure grammatical precision and clarity throughout the summary.

Resume: [{content}]
Format: [{p1_format.format(data=data_to_add_tallahassee)}]

"""


def user_words_without_ai_p1(content):
    return f"""
Create a comprehensive professional summary that accurately reflects the candidate's qualifications and experiences. Follow these guidelines:

If a Professional Summary Exists:

    - Extract the provided professional summary section as is.
    - Only rectify grammatical errors without changing or summarizing the content.
    - The final output should retain the candidate's original professional summary, with improved grammatical accuracy.

If No Professional Summary Exists:

    - Strictly leave this section blank. Do not generate a professional summary.

Formatting:

    - Present the final professional summary in clear, well-structured sentences.
    - Ensure grammatical precision and clarity throughout the summary.

**Strictly if there is no Professional Summary found don't create or add it from some where else, totally ignore tag of Professional Summary**

Resume: [{content}]
Format: [{p1_format.format(data=data_to_add_tallahassee)}]

"""


###################### Turnpike Formats ######################


def user_words_ai_summarize_p1_turnpike(content):
    return f"""

Create a comprehensive Experience Summary that accurately reflects the candidate's qualifications and experiences. Follow these guidelines:

If a Experience Summary Exists:

    - Extract each line from the provided Experience Summary section.
    - Summarize each line while ensuring that no key details or concepts are omitted.
    - The final output should seamlessly integrate these summarized lines into a cohesive summary that maintains a professional tone.

If No Experience Summary Exists:

    - Use the AI-based Experience Summary generation feature to create a Experience Summary.
    - Ensure that the generated summary accurately reflects the candidate's qualifications and experiences.
    - Review the summary to confirm that it aligns with the candidate's resume details.
    - Create number of bullet points as per the content in the resume and make sure all the key points are covered in the summary. strictly create 10-15 bullet points.
    - Created bullet points should be very informative and should cover all the key points mentioned in the resume.

Formatting:

    - Present the final Experience Summary in clear, well-structured sentences.
    - Ensure grammatical precision and clarity throughout the summary.

Resume: [{content}]
Format: [{p1_format.format(data=data_to_add_turnpike)}]

"""


def user_words_without_ai_p1_turnpike(content):
    return f"""

- Extract each line from the provided Professional Summary section.
- Extract as it is and do not summarize the content.
- If no Professional Summary is found, leave this tag blank. Do not generate it or fetch it from anywhere else from the resume.
- Make sure all the information are extracted as it is without any summarization.


**Strictly if there is no Professional Summary found don't create or add it from some where else, totally ignore tag of Professional Summary**

Resume: [{content}]
Format: [{p1_format.format(data=data_to_add_turnpike)}]

"""
