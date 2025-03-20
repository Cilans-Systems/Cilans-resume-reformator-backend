from dotenv import load_dotenv
from datetime import date
from openai import OpenAI
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

from .formats import (
    user_words_ai_summarize_p1,
    user_words_without_ai_p1,
    user_words_ai_summarize_p1_turnpike,
    user_words_without_ai_p1_turnpike,
    p1_system_words_with_ai_summary,
    p1_system_words_without_ai_summary,
    p2_system_words,
    p2_user_words,
)

# Load environment variables from .env file
load_dotenv()

today_date = date.today().strftime("%Y-%m-%d")

open_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=open_api_key)


# Function to extract date ranges, calculate months, and update the HTML
def calculate_and_update_dates(html):
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Regex pattern to match 'Date: MM/YY - MM/YY' or 'Date: MM/YY - Present'
    date_pattern = r"Date: (\d{2}/\d{2}) - (\d{2}/\d{2}|Present|Current)"

    # Get the current date
    current_date = datetime.now()

    # Find all <strong> tags
    strong_tags = soup.find_all("strong")

    for strong_tag in strong_tags:
        # Check if the <strong> tag contains a valid date range
        match = re.search(date_pattern, strong_tag.text)
        if match:
            # Extract the start date from the regex group
            start_date_str = match.group(1)  # e.g., '09/18'

            if start_date_str == "00/00":
                strong_tag.string = "Date: Not Available"
                continue

            # Check if the end date is 'Present'
            end_date_str = match.group(2)  # Either 'MM/YY' or 'Present'

            current_potions = end_date_str.lower()

            if current_potions in ["present", "current"]:
                # Use the current month and year for 'Present'
                end_date = current_date
                end_date_str = end_date.strftime("%m/%y")
            else:
                # Convert the end date to a datetime object if it's not 'Present'
                end_date = datetime.strptime(end_date_str, "%m/%y")

            # Convert the start date to a datetime object
            start_date = datetime.strptime(start_date_str, "%m/%y")

            # Calculate the difference in months
            months_diff = (
                (end_date.year - start_date.year) * 12
                + end_date.month
                - start_date.month
            )

            if current_potions in ["present", "current"]:
                # Update the <strong> tag's text with the calculated months
                new_text = f"Date: {start_date_str} - (Months: {months_diff + 1}) ({current_potions.capitalize()})"
            else:
                # Update the <strong> tag's text with the calculated months
                new_text = f"Date: {start_date_str} - {end_date_str} (Months: {months_diff + 1})"
            strong_tag.string = new_text  # Update the tag's text

    # Return the updated HTML
    return str(soup)


def wrap_keywords_in_b_tags(text, keywords):
    # Sort keywords by length in descending order to avoid partial replacements
    keywords = sorted(keywords, key=len, reverse=True)

    for keyword in keywords:
        # Use re.sub with a lambda to replace the matched keyword with <b>wrapped keyword</b>, ignoring case
        text = re.sub(
            f"(?i)({re.escape(keyword)})",
            lambda match: f"<b>{match.group(0)}</b>",
            text,
        )

    return text


def create_ai_response(client, message, content):

    message_in = [
        {"role": "system", "content": message},
        {"role": "user", "content": content},
    ]

    reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_in,
        temperature=0.1,
        max_tokens=8188,
        n=1,
    )

    reply = reply.choices[0].message.content

    if "```html" in reply and "```" in reply:
        reply = reply.replace("```html", "").replace("```", "").strip()

    return reply


def html_cleanup(completion_p1, completion_p2):
    return completion_p1.replace("</body>", "").replace(
        "</html>", ""
    ) + completion_p2.replace("<html>", "").replace("<body>", "").replace(
        "<!DOCTYPE html>", ""
    ).replace(
        '<html lang="en">', ""
    ).replace(
        "\n\n", "\n"
    )


def formate_message_tallahassee(content, keywords):

    completion_p1 = create_ai_response(
        client,
        p1_system_words_with_ai_summary.replace(" Contact Number,", ""),
        user_words_ai_summarize_p1(content),
    )

    completion_p2 = create_ai_response(client, p2_system_words, p2_user_words(content))

    final_output = html_cleanup(completion_p1, completion_p2)

    # final_output = completion_p1[:-16] + completion_p2[40:]

    try:
        # Process the HTML and print the updated content
        final_output = calculate_and_update_dates(final_output)
    except:
        pass

    if keywords:
        return wrap_keywords_in_b_tags(final_output, keywords)

    return final_output


def formate_message_tallahassee_without_ai_generated_summary(content, keywords):

    completion_p1 = create_ai_response(
        client,
        p1_system_words_without_ai_summary.replace(" Contact Number,", ""),
        user_words_without_ai_p1(content),
    )

    completion_p2 = create_ai_response(
        client,
        p2_system_words,
        p2_user_words(content),
    )

    # final_output = completion_p1[:-16] + completion_p2[40:]
    final_output = html_cleanup(completion_p1, completion_p2)

    try:
        # Process the HTML and print the updated content
        final_output = calculate_and_update_dates(final_output)
    except:
        pass

    if keywords:
        return wrap_keywords_in_b_tags(final_output, keywords)
    return final_output


def formate_message_turnpike_without_ai_generated_summary(content, keywords):

    completion_p1 = create_ai_response(
        client,
        p1_system_words_without_ai_summary,
        user_words_without_ai_p1_turnpike(content),
    )

    completion_p2 = create_ai_response(client, p2_system_words, p2_user_words(content))

    final_output = html_cleanup(completion_p1, completion_p2)

    try:
        # Process the HTML and print the updated content
        final_output = calculate_and_update_dates(final_output)
    except:
        pass

    if keywords:
        return wrap_keywords_in_b_tags(final_output, keywords)

    return final_output


def formate_message_turnpike(content, keywords):

    completion_p1 = create_ai_response(
        client,
        p1_system_words_with_ai_summary,
        user_words_ai_summarize_p1_turnpike(content),
    )

    completion_p2 = create_ai_response(client, p2_system_words, p2_user_words(content))

    final_output = html_cleanup(completion_p1, completion_p2)
    try:
        # Process the HTML and print the updated content
        final_output = calculate_and_update_dates(final_output)
    except:
        pass

    if keywords:
        return wrap_keywords_in_b_tags(final_output, keywords)

    return final_output
