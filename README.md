# PyForge_my_awesome_project

## Instalation:
git_clone https://github.com/Barabaika/PyForge_my_awesome_project.git && cd PyForge_my_awesome_project && docker-compose up -d --build && docker-compose exec web python manage.py clear_db

## Usage:
### CLI for adding compound:
docker-compose exec web python manage.py add --compound_name "<compound_name>" \
(Avalible values for compound_name: ["ADP", "ATP", "STI", "ZID", "DPM", "XP9", "18W", "29P"]) 
### CLI for printing table:
docker-compose exec web python manage.py print_info 
