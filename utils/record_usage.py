from models.api_usage import APIUsage


def record_usage(api_key, input_tokens, output_tokens, cost):
    from database import get_db

    db_session = next(get_db())

    new_record = APIUsage(
        api_key=api_key,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=cost,
    )

    db_session.add(new_record)
    db_session.commit()
