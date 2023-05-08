from __future__ import annotations
import datetime
import edgedb
from uuid import UUID

from assignments.backend.src.models import Assignment, Attachment, Work, AttachmentFile, AssignmentID, WorkID, AttachmentID, OwnerID


async def add_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    owner_id: UUID,
    **kwargs
) -> AssignmentID:
    return await executor.query_single(
        """\
        insert Assignment {
          owner := (
            select User
            filter .id = <uuid>$owner_id
          ),
          title := <str>$title,
          deadline := <optional datetime>$deadline,
          description := <optional str>$description,
          max_grade := <optional int16>$max_grade,
        }
        """,
        owner_id=owner_id,
        **kwargs
    )


async def add_attachment_to_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
    filename: str,
    content_type: str,
    file: bytes,
) -> AttachmentID:
    return await executor.query_single(
        """\
        with
        attachment := (
          insert Attachment {
                filename := <str>$filename,
                content_type := <str>$content_type,
                file := <bytes>$file
              }
        ),
        updated_assignment := (
          update Assignment
          filter .id = <uuid>$assignment_id
          set {
            attachments += attachment
          }
        )
        select attachment
        """,
        assignment_id=assignment_id,
        filename=filename,
        content_type=content_type,
        file=file,
    )


async def add_attachment_to_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: UUID,
    filename: str,
    content_type: str,
    file: bytes,
) -> WorkID:
    return await executor.query_single(
        """\
        update Work
        filter .id = <uuid>$work_id
        set {
            attachments += (
              insert Attachment {
                filename := <str>$filename,
                content_type := <str>$content_type,
                file := <bytes>$file
              }
            )
        }\
        """,
        work_id=work_id,
        filename=filename,
        content_type=content_type,
        file=file,
    )


async def add_work_to_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    owner_id: UUID,
    filename: str,
    content_type: str,
    file: bytes,
    assignment_id: UUID,
) -> AssignmentID:
    return await executor.query_single(
        """\
        with
          owner := (
            select User
            filter .id = <uuid>$owner_id
          ),
          attachment := (
            insert Attachment {
              filename := <str>$filename,
              content_type := <str>$content_type,
              file := <bytes>$file
            }
          ),
          work := (
            insert Work {
              owner := owner,
              attachments := attachment,
            }
          )
        update Assignment
        filter .id = <uuid>$assignment_id
        set {
          works += work
        }\
        """,
        owner_id=owner_id,
        filename=filename,
        content_type=content_type,
        file=file,
        assignment_id=assignment_id,
    )


async def delete_all_assignment_attachments(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> list[AttachmentID]:
    return await executor.query(
        """\
        with target_assignment := (
          select Assignment
          filter .id = <uuid>$assignment_id
        )
        for attachment in target_assignment.attachments
        union (
          delete attachment
        )\
        """,
        assignment_id=assignment_id,
    )


async def delete_all_assignment_works(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> list[WorkID]:
    return await executor.query(
        """\
        with target_assignment := (
          select Assignment
          filter .id = <uuid>$assignment_id
        )
        for work in target_assignment.works
        union (
          delete work
        )\
        """,
        assignment_id=assignment_id,
    )


async def delete_all_assignment_works_attachments(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> list[AttachmentID]:
    return await executor.query(
        """\
        with target_assignment := (
          select Assignment
          filter .id = <uuid>$assignment_id
        )
        for work in target_assignment.works
        union (
          for attachment in work.attachments
          union(
            delete attachment
          )
        )\
        """,
        assignment_id=assignment_id,
    )


async def delete_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> AssignmentID:
    return await executor.query_single(
        """\
        delete Assignment
        filter .id = <uuid>$assignment_id\
        """,
        assignment_id=assignment_id,
    )


async def delete_attachment(
    executor: edgedb.AsyncIOExecutor,
    *,
    attachment_id: UUID,
) -> AttachmentID:
    return await executor.query_single(
        """\
        delete Attachment
        filter .id = <uuid>$attachment_id\
        """,
        attachment_id=attachment_id,
    )


async def get_all_assignment_attachments(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> list[Attachment]:
    return await executor.query(
        """\
        with assignment := (
          select Assignment
          filter .id = <uuid>$assignment_id
        )
        select assignment.attachments {
          id,
          filename,
          content_type
        }\
        """,
        assignment_id=assignment_id,
    )


async def get_all_assignment_works(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> list[Work]:
    return await executor.query(
        """\
        with assignment := (
          select Assignment
          filter .id = <uuid>$assignment_id
        )
        select assignment.works {
          id,
          owner: {
            id,
            username
          },
          is_submitted,
          grade
        }\
        """,
        assignment_id=assignment_id,
    )


async def get_all_assignments(
    executor: edgedb.AsyncIOExecutor,
) -> list[Assignment]:
    return await executor.query(
        """\
        select Assignment {
          id,
          owner: {
            id,
            username
          },
          title,
          deadline,
          description,
          max_grade
        }\
        """,
    )


async def get_all_work_attachments(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: UUID,
) -> list[Attachment]:
    return await executor.query(
        """\
        with work := (
          select Work
          filter .id = <uuid>$work_id
        )
        select work.attachments {
          id,
          filename,
          content_type
        }\
        """,
        work_id=work_id,
    )


async def get_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> AssignmentID:
    return await executor.query_single(
        """\
        select Assignment
        filter .id = <uuid>$assignment_id
        """,
        assignment_id=assignment_id,
    )


async def get_assignment_of_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: UUID,
) -> AssignmentID:
    return await executor.query_single(
        """\
        with target_work := (
          select Work
          filter .id = <uuid>$work_id
        )
        select target_work.<works[is Assignment] {
          id,
          owner
        } limit 1
        """,
        work_id=work_id,
    )


async def get_assignment_owner(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
) -> OwnerID:
    return await executor.query_single(
        """\
        with target_assignment := (
          select Assignment
          filter .id = <uuid>$assignment_id
        )
        select target_assignment.owner
        """,
        assignment_id=assignment_id,
    )


async def get_attachment(
    executor: edgedb.AsyncIOExecutor,
    *,
    attachment_id: UUID,
) -> AttachmentFile:
    return await executor.query_single(
        """\
        select Attachment {
          file
        } filter .id = <uuid>$attachment_id\
        """,
        attachment_id=attachment_id,
    )


async def get_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: UUID,
):
    return await executor.query_single(
        """\
        select Work {
          id,
          owner
        }
        filter .id = <uuid>$work_id
        """,
        work_id=work_id,
    )


async def grade_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: UUID,
    grade: int,
) -> WorkID:
    return await executor.query_single(
        """\
        update Work
        filter .id = <uuid>$work_id
        set {
          grade := <int16>$grade
        }\
        """,
        work_id=work_id,
        grade=grade,
    )


async def submit_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: UUID,
) -> WorkID:
    return await executor.query_single(
        """\
        update Work
        filter .id = <uuid>$work_id
        set {
          is_submitted := True
        }\
        """,
        work_id=work_id,
    )


async def unsubmit_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: UUID,
) -> WorkID:
    return await executor.query_single(
        """\
        update Work
        filter .id = <uuid>$work_id
        set {
          is_submitted := False
        }\
        """,
        work_id=work_id,
    )


async def update_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: UUID,
    **kwargs
) -> AssignmentID:
    return await executor.query_single(
        """\
        update Assignment
        filter .id = <uuid>$assignment_id
        set {
          title := <optional str>$title,
          deadline := <optional datetime>$deadline,
          description := <optional str>$description,
          max_grade := <optional int16>$max_grade,
        }
        """,
        assignment_id=assignment_id,
        **kwargs
    )
