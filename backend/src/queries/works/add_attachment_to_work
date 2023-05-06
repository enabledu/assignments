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
}