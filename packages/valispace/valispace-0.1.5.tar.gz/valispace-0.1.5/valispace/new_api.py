class API:
	def __init__(self, url=None, username=None, password=None):
		pass


	def get_request_headers(self):
		pass


	def get_all_data(self, type=None):
		pass


	def get_vali_list(self, workspace_id=None, workspace_name=None, project_id=None, project_name=None, parent_id=None,
			parent_name=None, tag_id=None, tag_name=None, vali_marked_as_impacted=None):
		pass

	def get_vali_names(self, project_name=None):
		pass


	def get_vali(self, id):
		pass


	def get_vali_by_name(self, vali_name, project_name):
		pass


	def fuzzysearch_vali(self, searchterm):
		pass


	def get_vali_value(self, id):
		pass


	def update_vali(self, id, shortname=None, formula=None, data=None):
		pass


	def impact_analysis(self, id, target_vali_id, range_from, range_to, range_step_size):
		pass


	def what_if(self, vali_name, target_name, value):
		pass


	def get_component_list(self, workspace_id=None, workspace_name=None, project_id=None, project_name=None,
			parent_id=None, parent_name=None, tag_id=None, tag_name=None):
		pass


	def get_component(self, id):
		pass


	def get_component_by_name(self, unique_name, project_name):
		pass


	def get_project_list(self, workspace_id=None, workspace_name=None):
		pass


	def get_project(self, id):
		pass


	def get_project_by_name(self, name):
		pass


	def post_data(self, type=None, data=None):
		pass


	def post(self, url, data=None):
		pass


	def get(self, url, data=None):
		pass


	def request(self, method, url, data=None):


	def get_matrix(self, id):
		pass


	def get_matrix_str(self, id):
		pass


	def update_matrix_formulas(self, id, matrix_formula):
		pass


	def vali_create_dataset(self, vali_id):
		pass


	def create_dataset_and_set_values(self, vali_id, input_data):
		pass
