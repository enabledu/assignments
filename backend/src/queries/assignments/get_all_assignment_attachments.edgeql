with assignment := (
  select Assignment
  filter .id = <uuid>$assignment_id
)
select assignment.attachments {
  id,
  filename,
  content_type
}