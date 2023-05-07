from __future__ import annotations
import dataclasses
import datetime
import edgedb
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_validators__(cls):
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class AddAssignmentResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class GetAllAnswersResultAuthor(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class AddAttachmentToWorkResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class DeleteAllAssignmentAttachmentsResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class GetAllAssignmentAttachmentsResult(NoPydanticValidation):
    id: uuid.UUID
    filename: str | None
    content_type: str | None


@dataclasses.dataclass
class GetAllAssignmentWorksResult(NoPydanticValidation):
    id: uuid.UUID
    owner: GetAllAnswersResultAuthor
    is_submitted: bool | None
    grade: int | None


@dataclasses.dataclass
class GetAllAssignmentsResult(NoPydanticValidation):
    id: uuid.UUID
    owner: GetAllAnswersResultAuthor
    title: str
    deadline: datetime.datetime | None
    description: str | None
    max_grade: int | None


@dataclasses.dataclass
class GetAttachmentResult(NoPydanticValidation):
    id: uuid.UUID
    file: bytes


async def add_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    owner_id: uuid.UUID,
    title: str,
    deadline: datetime.datetime,
    description: str,
    max_grade: int,
) -> AddAssignmentResult:
    return await executor.query_single(
        """\
        insert Assignment {
          owner := (
            select User
            filter .id = <uuid>$owner_id
          ),
          title := <str>$title,
          deadline := <datetime>$deadline,
          description := <str>$description,
          max_grade := <int16>$max_grade,
        }\
        """,
        owner_id=owner_id,
        title=title,
        deadline=deadline,
        description=description,
        max_grade=max_grade,
    )


async def add_attachment_to_assignment(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: uuid.UUID,
    filename: str,
    content_type: str,
    file: bytes,
) -> AddAssignmentResult | None:
    return await executor.query_single(
        """\
        update Assignment
        filter .id = <uuid>$assignment_id
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
        assignment_id=assignment_id,
        filename=filename,
        content_type=content_type,
        file=file,
    )


async def add_attachment_to_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: uuid.UUID,
    filename: str,
    content_type: str,
    file: bytes,
) -> AddAttachmentToWorkResult | None:
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
    owner_id: uuid.UUID,
    filename: str,
    content_type: str,
    file: bytes,
    assignment_id: uuid.UUID,
) -> AddAssignmentResult | None:
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
    assignment_id: uuid.UUID,
) -> list[DeleteAllAssignmentAttachmentsResult]:
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
    assignment_id: uuid.UUID,
) -> list[AddAttachmentToWorkResult]:
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
    assignment_id: uuid.UUID,
) -> list[DeleteAllAssignmentAttachmentsResult]:
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
    assignment_id: uuid.UUID,
) -> AddAssignmentResult | None:
    return await executor.query_single(
        """\
        delete Assignment
        filter .id = <uuid>$assignment_id\
        """,
        assignment_id=assignment_id,
    )


async def get_all_assignment_attachments(
    executor: edgedb.AsyncIOExecutor,
    *,
    assignment_id: uuid.UUID,
) -> list[GetAllAssignmentAttachmentsResult]:
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
    assignment_id: uuid.UUID,
) -> list[GetAllAssignmentWorksResult]:
    return await executor.query(
        """\
        with assignment := (
          select Assignment
          filter .id = <uuid>$assignment_id
        )
        select assignment.works {
          id,
          owner,
          is_submitted,
          grade
        }\
        """,
        assignment_id=assignment_id,
    )


async def get_all_assignments(
    executor: edgedb.AsyncIOExecutor,
) -> list[GetAllAssignmentsResult]:
    return await executor.query(
        """\
        select Assignment {
          id,
          owner,
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
    work_id: uuid.UUID,
) -> list[GetAllAssignmentAttachmentsResult]:
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


async def get_attachment(
    executor: edgedb.AsyncIOExecutor,
    *,
    attachment_id: uuid.UUID,
) -> GetAttachmentResult | None:
    return await executor.query_single(
        """\
        select Attachment {
          file
        } filter .id = <uuid>$attachment_id\
        """,
        attachment_id=attachment_id,
    )


async def grade_work(
    executor: edgedb.AsyncIOExecutor,
    *,
    work_id: uuid.UUID,
    grade: int,
) -> AddAttachmentToWorkResult | None:
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
    work_id: uuid.UUID,
) -> AddAttachmentToWorkResult | None:
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
    work_id: uuid.UUID,
) -> AddAttachmentToWorkResult | None:
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
    assignment_id: uuid.UUID,
    title: str,
    deadline: datetime.datetime,
    description: str,
    max_grade: int,
) -> AddAssignmentResult | None:
    return await executor.query_single(
        """\
        update Assignment
        filter .id = <uuid>$assignment_id
        set {
          title := <str>$title,
          deadline := <datetime>$deadline,
          description := <str>$description,
          max_grade := <int16>$max_grade,
        }\
        """,
        assignment_id=assignment_id,
        title=title,
        deadline=deadline,
        description=description,
        max_grade=max_grade,
    )
