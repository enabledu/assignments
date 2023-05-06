insert Assignment {
  owner := (
    select User
    filter .id = <uuid>$owner_id
  ),
  title := <str>$title,
  deadline := <datetime>$deadline,
  description := <str>$description,
  max_grade := <int16>$max_grade,
}