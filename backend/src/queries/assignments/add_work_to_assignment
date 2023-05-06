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
}