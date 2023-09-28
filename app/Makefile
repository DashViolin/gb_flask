reset:
	docker-compose down
	sleep 1
	sudo rm -rf ../data/pgdata_dev/
	docker-compose up -d
	sleep 4
	poetry run flask init-db
	sleep 2
	poetry run flask load-fixtures


restart:
	docker-compose down
	sleep 1
	docker-compose up -d
