# Data cleaning functions by drashti
def clean_text(text):
    if not text:
        return ""

    return str(text).strip().lower()


def clean_skill_list(skill_list):
    if not skill_list:
        return []

    cleaned = []

    for skill in skill_list:
        skill = clean_text(skill)

        if skill:
            cleaned.append(skill)

    return list(set(cleaned))