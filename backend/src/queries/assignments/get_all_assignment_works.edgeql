with assignment := (
  select Assignment
  filter .id = <uuid>$assignment_id
)
select assignment.works {
  id,
  owner: {
    id,
    username
  },
  is_submitted,
  grade
}