class JobQuery5C:
    def __init__(self):
        self.columns = {
            "company_type": ["id", "kind"],
            "info_type": ["id", "info"],
            "movie_companies": ["id", "movie_id", "company_id", "company_type_id", "note"],
            "movie_info": ["id", "movie_id", "info_type_id", "info", "note"],
            "title": ["id", "title", "imdb_index", "kind_id", "production_year", "imdb_id", "phonetic_code", "episode_of_id", "season_nr", "episode_nr", "series_years", "md5sum"]
        }
        
        self.selection_criteria = {
            "movie_companies": [
                {"column": "note", "operator": "not like", "value": "%(TV)%"},
                {"column": "note", "operator": "like", "value": "%(USA)%"}
            ],
            "title": [{"column": "production_year", "operator": ">", "value": 1990}],
            "company_type": [{"column": "kind", "operator": "==", "value": "production companies"}]
        }

        self.projection_criteria = {}

        self.join_tree = [
        {"left": "company_type", "right": "movie_companies", "left_key": "id", "right_key": "company_type_id"},
        {"left": "movie_companies", "right": "title", "left_key": "movie_id", "right_key": "id"},
        {"left": "title", "right": "movie_info", "left_key": "id", "right_key": "movie_id"},
        {"left": "movie_companies", "right": "movie_info", "left_key": "movie_id", "right_key": "movie_id"},
        {"left": "movie_info", "right": "info_type", "left_key": "info_type_id", "right_key": "id"}
        ]
        
        self.query = """SELECT COUNT(*) FROM company_type AS ct, info_type AS it, 
        movie_companies AS mc, movie_info AS mi, title AS t WHERE 
        ct.kind  = 'production companies' AND mc.note not like '%(TV)%' and 
        mc.note like '%(USA)%' AND t.production_year > 1990 AND 
        t.id = mi.movie_id AND t.id = mc.movie_id AND mc.movie_id = mi.movie_id AND 
        ct.id = mc.company_type_id AND it.id = mi.info_type_id;"""