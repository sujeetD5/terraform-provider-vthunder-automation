import json


def func_caller(func_name, methods, data_to_func, data_to_func_params, name_key_value, set_id_params, get_func_params, name=True):

	if name:
		update_request_params = "client.Token, name, data, client.Host"
	else:
		update_request_params = "client.Token, {set_id_params}, data, client.Host".format(set_id_params=set_id_params)


	create_code = 'logger.Println("[INFO] Creating {func_name} (Inside resource{func_name}Create) ")\n \
		{name_key_value} \n\
		data := {data_to_func}({data_to_func_params})\n \
		logger.Println("[INFO] received V from method data to {func_name} --")\n \
		d.SetId({set_id_params})\n \
		go_vthunder.Post{func_name}(client.Token, data, client.Host)\n \
\n\
		return resource{func_name}Read(d, meta)\n'.format(func_name=func_name, data_to_func=data_to_func,
			set_id_params=set_id_params, name_key_value=name_key_value,
			data_to_func_params=data_to_func_params)

	update_code = 'logger.Println("[INFO] Modifying {func_name}   (Inside resource{func_name}Update) ")\n \
		{name_key_value} \n\
		data := {data_to_func}({data_to_func_params})\n \
		logger.Println("[INFO] received V from method data to {func_name} ")\n \
		d.SetId({set_id_params})\n \
		go_vthunder.Put{func_name}(client.Token, name, data, client.Host)\n \
\n \
		return resource{func_name}Read(d, meta)\n'.format(func_name=func_name, data_to_func=data_to_func,
			set_id_params=set_id_params, name_key_value=name_key_value,
			data_to_func_params=data_to_func_params)

	read_code = 'name := d.Id()\n\
		logger.Println("[INFO] Fetching service Read" + name)\n \
		data, err := go_vthunder.Get{func_name}({get_func_params})\n \
		if data == nil {{\n \
			logger.Println("[INFO] No data found " + name)\n \
			d.SetId("")\n \
			return nil\n \
		}}\n\
		return err'.format(func_name=func_name, get_func_params=get_func_params)

	delete_code = 'name := d.Id()\n \
		logger.Println("[INFO] Deleting instance (Inside resource{func_name}Delete) " + name)\n \
		err := go_vthunder.Delete{func_name}(client.Token, name, client.Host)\n\
		if err != nil {{\n\
			log.Printf("[ERROR] Unable to Delete resource instance  (%s) (%v)", name, err)\n\
			return err\n\
		}}\n\
		d.SetId("")\n\
		return nil'.format(func_name=func_name)
	with open("{}.go".format(func_name), "w") as file:
		for method in methods:
			read_log = ""
			if method == "Create":
				inner_code = create_code
			elif method == "Update":
				inner_code = update_code
			elif method == "Read":
				read_log = 'logger.Println("[INFO] Reading {func_name} (Inside resource{func_name}Read)"\n'.format(func_name=func_name)
				inner_code = read_code
			elif method == "Delete":
				inner_code = delete_code

			code_block = '\nfunc resource{func_name}{method}(d *schema.ResourceData, meta interface{{}}) error {{\n \
	logger := util.GetLoggerInstance()\n \
	client := meta.(vThunder)\n \
	{read_log} \
\n\
	if client.Host != "" {{\n \
		{inner_code}\n\
	}}\n \
	return nil\n \
}}\n\
	'.format(func_name=func_name, method=method, read_log=read_log, inner_code=inner_code)

			file.write(code_block)

def executor(methods, function_name, struct_instance, axapi_url, name = True):

	get_delete_params = "id string, name string, host string"
	post_params = "id string, inst {struct_instance}, host string".format(struct_instance = struct_instance)
	put_params = "id string, name string, inst {struct_instance}, host string".format(struct_instance = struct_instance)

	# payload_strings => if methd in ('POST', 'PUT') else ""
	payload = 'payloadBytes, err := json.Marshal(inst)\n\
	logger.Println("[INFO] input payload bytes - " + string((payloadBytes)))\n\
	if err != nil {\n\
		logger.Println("[INFO] Marshalling failed with error ", err)\n\
	}\n'

	post_http_data = ", bytes.NewReader(payloadBytes), headers"
	put_http_data = "+name, bytes.NewReader(payloadBytes), headers"
	get_delete_http_data = "+name, nil, headers"
	no_name_http_data = ", nil, headers"

	with open("resource_vthunder_{}.go".format(func_name), "w") as file:
		for method in methods:
			if method == "Read":
				method = "Get"
				extra_param = "(*{struct_instance}, error)".format(struct_instance = struct_instance)
				dict_params = get_delete_params
				request = "GET"
				payload_strings = ""
				if name:
					http_data = get_delete_http_data
				else:
					http_data = no_name_http_data
				return_error = "return nil, err"
				get_return = "return &m,nil"
				delete_return = ""
				url = axapi_url + "/"
			elif method == "Delete":
				extra_param = "error"
				dict_params = get_delete_params
				request = "DELETE"
				payload_strings = ""
				http_data = get_delete_http_data
				return_error = "return err"
				get_return = ""
				delete_return = "return nil"
				url = axapi_url + "/"
			elif method == "Create":
				method = "Post"
				extra_param = ""
				dict_params = post_params
				request = "POST"
				payload_strings = payload
				http_data = post_http_data
				return_error = ""
				url = axapi_url
				get_return = ""
				delete_return = ""
			elif method == "Update":
				method = "Put"
				extra_param = ""
				dict_params = put_params
				request = "PUT"
				payload_strings = payload
				http_data = put_http_data
				return_error = ""
				url = axapi_url + "/"
				get_return = ""
				delete_return = ""


			code_block = '\nfunc {method}{function_name}({dict_params}) {extra_param} {{ \n\
\n\
	logger := util.GetLoggerInstance()\n\
\n\
	var headers = make(map[string]string)\n\
	headers["Accept"] = "application/json"\n\
	headers["Content-Type"] = "application/json"\n\
	headers["Authorization"] = id\n\
	logger.Println("[INFO] Inside {method}{function_name}")\n\
	{payload_strings}\n\
	resp, err := DoHttp("{request}", "https://"+host+"/axapi/v3/{axapi_url}"{http_data})\n\
\n\
	if err != nil {{\n\
		logger.Println("The HTTP request failed with error ", err)\n\
		{return_error}\n\
	}} else {{\n\
		data, _ := ioutil.ReadAll(resp.Body)\n\
		var m {struct_instance}\n\
		erro := json.Unmarshal(data, &m)\n\
		if erro != nil {{\n\
			logger.Println("Unmarshal error ", err)\n\
			{return_error}\n\
		}} else {{\n\
			logger.Println("[INFO] GET REQ RES..........................", m)\n\
			{get_return}\n\
		}}\n\
	}}\n\
	{delete_return}\n\
}}\n'.format(method = method, function_name = function_name, dict_params = dict_params, 
		extra_param = extra_param, payload_strings = payload_strings, request = request, axapi_url = url, 
		http_data = http_data, return_error = return_error, struct_instance = struct_instance,
		get_return = get_return, delete_return = delete_return)

			file.write(code_block)


def test_generator(func_name, config_name, resource_attrs, resource_name, create_import, check_func=True, check_destroy=True):

	if check_destroy:
		destroy_block = "CheckDestroy: testCheck{func_name}Destroyed,".format(func_name=func_name)
	else:
		destroy_block = ''
	resource_test_check = str()
	for attr in resource_attrs[1]:
		resource_test_check += '\t\t\t\t\tresource.TestCheckResourceAttr({attr_0}, {attr}),\n'.format(attr_0=resource_attrs[0], attr=attr)

	if check_func:
		test_check_func = "testCheck{func_name}Exists({resource_name}, true),".format(func_name=func_name, resource_name=resource_name)
	else:
		test_check_func = ""

	code_data = dict()
	code_block = 'func TestAccVthunder{func_name}_create(t *testing.T) {{\n\
	resource.Test(t, resource.TestCase{{\n\
		PreCheck: func() {{\n\
			testAcctPreCheck(t)\n\
		}},\n\
		Providers:    testAccProviders,\n\
		{destroy_block}\n\
		Steps: []resource.TestStep{{\n\
			{{\n\
				Config: TEST_{config_name}_RESOURCE,\n\
				Check: resource.ComposeTestCheckFunc(\n\
					{test_check_func}\n{resource_test_check}\
				),\n\
			}},\n\
		}},\n\
	}})\n\
}}'.format(func_name=func_name, config_name=config_name.upper(), destroy_block=destroy_block, test_check_func=test_check_func, resource_test_check = resource_test_check)
	code_data["acceptance"] = code_block

	if create_import:
		code_block = '\nfunc TestAccVthunder{func_name}_import(t *testing.T) {{\n\
	resource.Test(t, resource.TestCase{{\n\
		PreCheck: func() {{\n\
			testAcctPreCheck(t)\n\
		}},\n\
		Providers:    testAccProviders,\n\
		CheckDestroy: testCheck{func_name}Destroyed,\n\
		Steps: []resource.TestStep{{\n\
			{{\n\
				Config: TEST_{config_name}_RESOURCE,\n\
				Check: resource.ComposeTestCheckFunc(\n\
					testCheck{func_name}Exists({resource_name}, true),\n\
				),\n\
				ResourceName:      {resource_name},\n\
				ImportState:       false,\n\
				ImportStateVerify: true,\n\
			}},\n\
		}},\n\
	}})\n\
}}\n'.format(func_name = func_name, config_name= config_name, resource_name=resource_name)
		code_data["import"] = code_block
		return code_data


if __name__ == '__main__':
	attrs = open("./config.json").read()
	attr = json.loads(attrs)
	func_name = attr["func_name"]
	methods = attr["methods"]
	name_key_value = attr["name_key_value"]
	data_to_func = attr["data_to_func"]
	data_to_func_params = attr["data_to_func_params"]
	set_id_params = attr["set_id_params"]
	get_func_params = attr["get_func_params"]
	name = attr["name"]

	#API calling functions.
	func_caller(func_name, methods, data_to_func, data_to_func_params, name_key_value, set_id_params, get_func_params, name)


	struct_instance = attr["struct_instance"]
	axapi_url = attr["axapi_url"]

	# API function executors.
	executor(methods, func_name, struct_instance, axapi_url, name)

	# Test generator.
	test_config = attr["test_params"]
	config_name = test_config["config_name"]
	check_func = test_config["check_func"]
	check_destroy = test_config["check_destroy"]
	resource_attrs = test_config["resource_attrs"]

	resource_name = test_config["resource_name"]
	create_import = test_config["create_import"]

	data = test_generator(func_name, config_name, resource_attrs, resource_name, create_import, check_func, check_destroy)
	with open("resource_vthunder_{}_test.go".format(func_name), "w") as f:
		f.write(data["acceptance"])
		import_code = data.get("import", None)
		if import_code:
			f.write(data["import"])

	# To run JAVA code.
	# import os
	# os.execute()