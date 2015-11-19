UPDATE sample
SET
  color = c.color
FROM (values
  ('CK-2','#456AA0'),
  ('CK-3','#FF9700'),
  ('CK-4','#FFD100'),
  ('CK-5','#3A9B88'),
  ('CK-6','#FF2C00'),
  ('CK-7','#8BD750'),
  ('CK-D1','#888888'),
  ('CK-D2','#444444')
  ) AS c(id,color)
WHERE c.id = sample.id;
