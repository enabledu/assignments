update Assignment
filter .id = <uuid>$assignment_id
set {
  title := <optional str>$title,
  deadline := <optional datetime>$deadline,
  description := <optional str>$description,
  max_grade := <optional int16>$max_grade,
}