CREATE OR REPLACE VIEW western_states AS
  SELECT * FROM state_geology
  WHERE "state" IN  ('AZ', 'NV', 'CA');

CREATE OR REPLACE VIEW simplified_western_states AS
  SELECT *,
    CASE
      WHEN lith62 IN ('Granodiorite','Granite','Tonalite','Diorite',
          'Plutonic rock','Quartz monzonite','Granitoid','Quartz diorite',
          'Glacial drift','Peraluminous granite')
        OR lith62mino IN ('Granitoid','Granite')
        THEN 'granitic'
      WHEN lith62 IN ('Gabbro','Anorthosite','Diabase')
        THEN 'mafic intrusive'
      WHEN lith62 = 'Mica schist'
         AND unit_age = 'Late Cretaceous to Eocene'
          OR unit_link = 'AZKJo;0'
          OR gid = 24348
        THEN 'subduction-channel schist'
     WHEN lith62 = 'Sandstone'
        AND lith62mino IN ('Mudstone','Siltstone')
        AND unit_age LIKE '%Cretaceous%'
        THEN 'subduction complex'
      WHEN lith62 IN ('Sandstone','Conglomerate','Shale','Siltstone',
        'Mudstone','Chert','Claystone','Lake or marine sediment',
        'Quartzite','Orthoquartzite','Arkose')
        AND unit_age NOT LIKE '%Proterozoic%'
        THEN 'clastic overlap'
      WHEN lith62 IN ('Limestone','Dolomite','Dolostone','Marble',
        'Sandstone','Conglomerate','Shale','Siltstone',
        'Mudstone','Chert','Claystone','Lake or marine sediment',
        'Quartzite','Orthoquartzite','Arkose')
        AND unit_age LIKE '%Proterozoic%'
        THEN 'Pz passive margin'
      WHEN lith62 IN ('Rhyolite','Felsic volcanic rock','Andesite',
        'Dacite','Intermediate volcanic rock','Volcanic breccia','Quartz latite')
        OR lith62mino = 'Rhyolite'
        OR lith62 LIKE 'volcanic'
        OR lith62mino LIKE 'volcanic'
        THEN 'felsic volcanic'
      WHEN lith62 IN ('Basalt','Andesite')
        AND unit_age LIKE '%Tertiary%'
        THEN 'felsic volcanic' -- proxy for teriary right now
      WHEN (lith62 IN ('Basalt','Mafic volcanic rock',
        'Alkaline basalt','Tephrite','Trachybasalt')
        OR lith62mino LIKE 'basalt')
        AND unit_age = 'Jurassic'
        THEN 'ophiolite'
      WHEN lith62 IN ('Basalt','Mafic volcanic rock',
        'Alkaline basalt','Tephrite','Trachybasalt')
        OR lith62mino LIKE 'basalt'
        THEN 'felsic volcanic'
      WHEN unit_link IN ('CAm;0','CAsch1;0')
        OR lith62 = 'Hornfels'
        OR (lith62 = 'Mica schist' AND lith62mino = 'Marble')
        THEN 'pendant'
      WHEN lith62 IN ('Greenstone','Greenschist','Blueschist',
        'Melange','Serpentinite')
        OR (lith62 LIKE 'Meta' OR lith62mino LIKE 'Meta')
        THEN 'subduction complex'
      WHEN lith62 IN ('Argillite','Peridotite','Graywacke','Slate')
        OR (lith62 = 'Slate' and lith62mino = 'Graywacke')
        OR unit_link IN ('CAsch7;0','CAPZ7;0')
        THEN 'ophiolite'
      WHEN lith62 IN ('Phyllite','Schist','Gneiss')
        AND lith62mino IN ('Schist','Gneiss','Mylonite')
        THEN 'core complex'
      WHEN lith62 IN ('Phyllite','Schist','Metasedimentary rock','Metavolcanic rock')
        THEN 'metamorphic'
    END AS lithology
  FROM western_states
  WHERE lith62 NOT IN ('water','Gravel','Sand','Alluvium','Dune sand','Playa','Landslide')
