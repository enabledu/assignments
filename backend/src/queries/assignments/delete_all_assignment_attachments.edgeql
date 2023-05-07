with target_assignment := (
  select Assignment
  filter .id = <uuid>$assignment_id
)
for attachment in target_assignment.attachments
union (
  delete attachment
)