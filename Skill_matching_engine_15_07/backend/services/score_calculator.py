# Score Calculator by drashti.


def calculate_experience_score(experience):

    if experience >= 5:
        return 100

    elif experience >= 3:
        return 80

    elif experience >= 2:
        return 60

    elif experience >= 1:
        return 40

    else:
        return 20


def calculate_technical_score(
    languages,
    frameworks,
    tools,
    experience
):

    skill_count = (
        len(languages)
        + len(frameworks)
        + len(tools)
    )

    skill_count_score = min(
        skill_count * 10,
        100
    )

    experience_score = calculate_experience_score(
        experience
    )

    technical_score = (
        skill_count_score * 0.7
        + experience_score * 0.3
    )

    return round(
        technical_score,
        2
    )


def calculate_learning_score(
    languages,
    frameworks,
    tools
):

    skill_count = (
        len(languages)
        + len(frameworks)
        + len(tools)
    )

    return min(
        skill_count * 10,
        100
    )


def calculate_adaptability_score(
    languages,
    frameworks,
    tools
):

    adaptability = (
        (
            len(languages) * 0.4
        )
        +
        (
            len(frameworks) * 0.3
        )
        +
        (
            len(tools) * 0.3
        )
    ) * 10

    return min(
        round(adaptability, 2),
        100
    )


def calculate_execution_score(
    completed_tasks,
    active_tasks
):

    total_tasks = (
        completed_tasks
        + active_tasks
    )

    if total_tasks == 0:
        return 50

    return round(
        (
            completed_tasks
            / total_tasks
        ) * 100,
        2
    )