with
  target_assignment := (
    select Assignment
    filter .id = <uuid>$assignment_id
  ),
  works_attachments := (
    for attachment in target_assignment.works.attachments
    union (
      delete attachment
    )
  ),
  works := (
    for work in target_assignment.works
    union (
      delete work
    )
  ),
  assignment_attachments := (
    for attachment in target_assignment.attachments
    union (
      delete attachment
    )
  )
delete target_assignment