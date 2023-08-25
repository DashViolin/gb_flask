reset:
	docker-compose down
	sleep 1
	sudo rm -rf ../data/pgdata_dev/
	docker-compose up -d
	sleep 2
	poetry run flask init-db
	poetry run flask load-fixtures
