with assignment := (
  select Assignment
  filter .id = <uuid>$assignment_id
)
select assignment.works {
  id,
  owner,
  is_submitted,
  grade
}