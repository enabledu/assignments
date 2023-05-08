with
  attachment := (
    insert Attachment {
        filename := <str>$filename,
        content_type := <str>$content_type,
        file := <bytes>$file
      }
  ),
  work := (
    update Work
    filter .id = <uuid>$work_id
    set {
        attachments += attachment
    }
  )
select attachment