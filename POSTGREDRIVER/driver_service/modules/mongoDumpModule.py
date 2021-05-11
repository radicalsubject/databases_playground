import os, logging
from datetime import date
from modules.dbconfig import MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, MONGO_URL

def dump_database():
	"""
	this doesnt work bc it is executed inside bot_container, but i need to execute in mondodbapi from inside bot_container. take a look at docker-compose networks??
	"""
	today = date.today()
	# dd.mm.YY
	current_date = today.strftime("%d.%m.%Y")
	path = os.getcwd()
	path = os.path.join(path, "mongodumps", "{}".format(current_date))
	logging.info(path)
	# exec_into_docker_command = "docker exec -it mongodb bash"
	# logging.info(os.system(exec_into_docker_command))

	# запуск команды по дампу
	command = "mongodump --host {} -u {} -p {} --authenticationDatabase admin -o={}".format("mongodb_api", MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, path)
	response = os.system(command)
	logging.info(response)

	# запуск команды архивирования
	command = f"zip -r {path}.zip {path}"
	response = os.system(command)
	logging.info(response)

	return (response, path)