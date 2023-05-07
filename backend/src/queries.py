from uuid import UUID

import edgedb


async def accept_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """
        insert Assignment {
        owner := (
          select User
          filter .id = <uuid>$owner_id
        ),
        title := <str>$title,
        deadline := <datetime>$deadline,
        description := <str>$description,
        max_grade := <int16>$max_grade,
        }
        """,
        id=id,
    )