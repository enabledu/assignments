with work := (
  select Work
  filter .id = <uuid>$work_id
)
select work.attachments {
  id,
  filename,
  content_type
}