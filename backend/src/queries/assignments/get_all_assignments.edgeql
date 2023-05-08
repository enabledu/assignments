select Assignment {
  id,
  owner {
    id,
    username
  },
  title,
  deadline,
  description,
  max_grade
}