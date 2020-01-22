# user_param = (methods, function_name, struct_instance, axapi_url)

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

	for method in methods:
		if method == "Get":
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
		elif method == "Post":
			extra_param = ""
			dict_params = post_params
			request = "POST"
			payload_strings = payload
			http_data = post_http_data
			return_error = ""
			url = axapi_url
			get_return = ""
			delete_return = ""
		elif method == "Put":
			extra_param = ""
			dict_params = put_params
			request = "PUT"
			payload_strings = payload
			http_data = put_http_data
			return_error = ""
			url = axapi_url + "/"
			get_return = ""
			delete_return = ""


		code_block = 'func {method}{function_name}({dict_params}) {extra_param} {{ \n\
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
}}'.format(method = method, function_name = function_name, dict_params = dict_params, 
		extra_param = extra_param, payload_strings = payload_strings, request = request, axapi_url = url, 
		http_data = http_data, return_error = return_error, struct_instance = struct_instance,
		get_return = get_return, delete_return = delete_return)
		print(code_block, "\n")

if __name__ == '__main__':

	# Convert methods from list to no if methods.
	methods = ("Get", "Post")
	function_name = "VrrpPeerGroup"
	struct_instance = "PeerGroup"
	axapi_url = "vrrp-a/peer-group"
	name = False
	executor(methods, function_name, struct_instance, axapi_url, name)
