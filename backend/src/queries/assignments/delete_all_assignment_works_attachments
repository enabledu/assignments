with target_assignment := (
  select Assignment
  filter .id = <uuid>$assignment_id
)
for work in target_assignment.works
union (
  for attachment in work.attachments
  union(
    delete attachment
  )
)