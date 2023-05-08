with target_work := (
  select Work
  filter .id = <uuid>$work_id
)
select target_work.<works[is Assignment] {
  id,
  owner
} limit 1