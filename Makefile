DB = xenoliths_flask

.PHONY: colors
colors: sql/insert-colors.sql
	-psql $(DB) -f $^
