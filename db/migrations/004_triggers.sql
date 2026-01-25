CREATE OR REPLACE FUNCTION prevent_update()
RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'Updates are not allowed on records';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER no_update
BEFORE UPDATE ON records
FOR EACH ROW
EXECUTE FUNCTION prevent_update();
