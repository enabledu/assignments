select Attachment {
  id,
  filename,
  content_type,
  file
} filter .id = <uuid>$attachment_id