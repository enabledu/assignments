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