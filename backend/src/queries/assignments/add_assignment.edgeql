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