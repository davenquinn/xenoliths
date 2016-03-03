UPDATE sample
SET
  color = c.color
FROM (values
  ('CK-3','#FF9700'),
  ('CK-4','#ffc600'),
  ('CK-6','#FF2C00'),
  ('CK-5','#3A9B88'),
  ('CK-7','#4e9c11'),
  ('CK-2','#456AA0'),
  ('CK-D1','#888888'),
  ('CK-D2','#444444')
  ) AS c(id,color)
WHERE c.id = sample.id;
