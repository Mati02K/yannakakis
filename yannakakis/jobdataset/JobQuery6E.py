class JobQuery6E:
    def __init__(self):
        self.columns = {
                "aka_title": ["id", "movie_id", "title", "imdb_index", "kind_id", "production_year", "phonetic_code", "episode_of_id", "season_nr", "episode_nr", "note", "md5sum"],
                "company_name": ["id", "name", "country_code", "imdb_id", "name_pcode_nf", "name_pcode_sf", "md5sum"],
                "company_type": ["id", "kind"],
                "info_type": ["id", "info"],
                "keyword": ["id", "keyword", "phonetic_code"],
                "movie_companies": ["id", "movie_id", "company_id", "company_type_id", "note"],
                "movie_info": ["id", "movie_id", "info_type_id", "info", "note"],
                "movie_keyword": ["id", "movie_id", "keyword_id"],
                "title": ["id", "title", "imdb_index", "kind_id", "production_year", "imdb_id", "phonetic_code", "episode_of_id", "season_nr", "episode_nr", "series_years", "md5sum"]
        }
            
        
        self.selection_criteria = {
            "company_name": [
                {"column": "country_code", "operator": "==", "value": "[us]"},
                {"column": "name", "operator": "==", "value": "YouTube"}
            ],
            "info_type": [
                {"column": "info", "operator": "==", "value": "release dates"}
            ],
            "movie_companies": [
                {"column": "note", "operator": "like", "value": "%(200%)%"},
                {"column": "note", "operator": "like", "value": "%(worldwide)%"}
            ],
            "movie_info": [
                {"column": "note", "operator": "like", "value": "%internet%"},
                {"column": "info", "operator": "like", "value": "USA:% 200%"}
            ],
            "title": [
                {"column": "production_year", "operator": "between", "value": [2005, 2010]}
            ]
        }


        self.projection_criteria = {}

        self.join_tree = [
            {"left": "title", "right": "aka_title", "left_key": "id", "right_key": "movie_id"},
            {"left": "title", "right": "movie_info", "left_key": "id", "right_key": "movie_id"},
            {"left": "title", "right": "movie_keyword", "left_key": "id", "right_key": "movie_id"},
            {"left": "title", "right": "movie_companies", "left_key": "id", "right_key": "movie_id"},
            {"left": "movie_keyword", "right": "movie_info", "left_key": "movie_id", "right_key": "movie_id"},
            {"left": "movie_keyword", "right": "movie_companies", "left_key": "movie_id", "right_key": "movie_id"},
            {"left": "movie_keyword", "right": "aka_title", "left_key": "movie_id", "right_key": "movie_id"},
            {"left": "movie_info", "right": "movie_companies", "left_key": "movie_id", "right_key": "movie_id"},
            {"left": "movie_info", "right": "aka_title", "left_key": "movie_id", "right_key": "movie_id"},
            {"left": "movie_companies", "right": "aka_title", "left_key": "movie_id", "right_key": "movie_id"},
            {"left": "movie_keyword", "right": "keyword", "left_key": "keyword_id", "right_key": "id"},
            {"left": "movie_info", "right": "info_type", "left_key": "info_type_id", "right_key": "id"},
            {"left": "movie_companies", "right": "company_name", "left_key": "company_id", "right_key": "id"},
            {"left": "movie_companies", "right": "company_type", "left_key": "company_type_id", "right_key": "id"}
        ]
        
        
        self.query = """SELECT COUNT(*) FROM aka_title AS at, company_name AS cn, company_type AS ct, info_type AS it1, 
        keyword AS k, movie_companies AS mc, movie_info AS mi, movie_keyword AS mk, title AS t 
        WHERE cn.country_code  = '[us]' and cn.name = 'YouTube' AND it1.info  = 'release dates' 
        AND t.production_year  between 2005 and 2010 AND 
        t.id = at.movie_id AND t.id = mi.movie_id AND t.id = mk.movie_id AND 
        t.id = mc.movie_id AND mk.movie_id = mi.movie_id AND mk.movie_id = mc.movie_id 
        AND mk.movie_id = at.movie_id AND mi.movie_id = mc.movie_id AND mi.movie_id = at.movie_id 
        AND mc.movie_id = at.movie_id AND k.id = mk.keyword_id AND it1.id = mi.info_type_id AND 
        cn.id = mc.company_id AND ct.id = mc.company_type_id;"""