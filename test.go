func resourceServiceGroupCreate(d *schema.ResourceData, meta interface{}) error {
 	logger := util.GetLoggerInstance()
 	client := meta.(vThunder)
 	 
	if client.Host != "" {
 		logger.Println("[INFO] Creating ServiceGroup (Inside resourceServiceGroupCreate) ")
 		name := d.Get("name").(string) 
		data := dataToSg(name, d)
 		logger.Println("[INFO] received V from method data to ServiceGroup --")
 		d.SetId(name)
 		go_vthunder.PostServiceGroup(client.Token, data, client.Host)
 
		return resourceServiceGroupRead(d, meta)

	}
 	return nil
 }	
func resourceServiceGroupRead(d *schema.ResourceData, meta interface{}) error {
 	logger := util.GetLoggerInstance()
 	client := meta.(vThunder)
 	logger.Println("[INFO] Reading ServiceGroup (Inside resourceServiceGroupRead)"
 
	if client.Host != "" {
 		name := d.Id()
		logger.Println("[INFO] Fetching service Read" + name)
 		data, err := go_vthunder.GetServiceGroup(client.Token, name, client.Host)
 		if data == nil {
 			logger.Println("[INFO] No data found " + name)
 			d.SetId("")
 			return nil
 		}
		return err
	}
 	return nil
 }	
func resourceServiceGroupUpdate(d *schema.ResourceData, meta interface{}) error {
 	logger := util.GetLoggerInstance()
 	client := meta.(vThunder)
 	 
	if client.Host != "" {
 		logger.Println("[INFO] Modifying ServiceGroup   (Inside resourceServiceGroupUpdate) ")
 		name := d.Get("name").(string) 
		data := dataToSg(name, d)
 		logger.Println("[INFO] received V from method data to ServiceGroup ")
 		d.SetId(name)
 		go_vthunder.PutServiceGroup(client.Token, name, data, client.Host)
 
 		return resourceServiceGroupRead(d, meta)

	}
 	return nil
 }	
func resourceServiceGroupDelete(d *schema.ResourceData, meta interface{}) error {
 	logger := util.GetLoggerInstance()
 	client := meta.(vThunder)
 	 
	if client.Host != "" {
 		name := d.Id()
 		logger.Println("[INFO] Deleting instance (Inside resourceServiceGroupDelete) " + name)
 		err := go_vthunder.DeleteServiceGroup(client.Token, name, client.Host)
		if err != nil {
			log.Printf("[ERROR] Unable to Delete resource instance  (%s) (%v)", name, err)
			return err
		}
		d.SetId("")
		return nil
	}
 	return nil
 }	
func PostServiceGroup(id string, inst ServiceGroup, host string)  { 

	logger := util.GetLoggerInstance()

	var headers = make(map[string]string)
	headers["Accept"] = "application/json"
	headers["Content-Type"] = "application/json"
	headers["Authorization"] = id
	logger.Println("[INFO] Inside PostServiceGroup")
	payloadBytes, err := json.Marshal(inst)
	logger.Println("[INFO] input payload bytes - " + string((payloadBytes)))
	if err != nil {
		logger.Println("[INFO] Marshalling failed with error ", err)
	}

	resp, err := DoHttp("POST", "https://"+host+"/axapi/v3/slb/service-group", bytes.NewReader(payloadBytes), headers)

	if err != nil {
		logger.Println("The HTTP request failed with error ", err)
		
	} else {
		data, _ := ioutil.ReadAll(resp.Body)
		var m ServiceGroup
		erro := json.Unmarshal(data, &m)
		if erro != nil {
			logger.Println("Unmarshal error ", err)
			
		} else {
			logger.Println("[INFO] GET REQ RES..........................", m)
			
		}
	}
	
} 

func GetServiceGroup(id string, name string, host string) (*ServiceGroup, error) { 

	logger := util.GetLoggerInstance()

	var headers = make(map[string]string)
	headers["Accept"] = "application/json"
	headers["Content-Type"] = "application/json"
	headers["Authorization"] = id
	logger.Println("[INFO] Inside GetServiceGroup")
	
	resp, err := DoHttp("GET", "https://"+host+"/axapi/v3/slb/service-group/"+name, nil, headers)

	if err != nil {
		logger.Println("The HTTP request failed with error ", err)
		return nil, err
	} else {
		data, _ := ioutil.ReadAll(resp.Body)
		var m ServiceGroup
		erro := json.Unmarshal(data, &m)
		if erro != nil {
			logger.Println("Unmarshal error ", err)
			return nil, err
		} else {
			logger.Println("[INFO] GET REQ RES..........................", m)
			return &m,nil
		}
	}
	
} 

func PutServiceGroup(id string, name string, inst ServiceGroup, host string)  { 

	logger := util.GetLoggerInstance()

	var headers = make(map[string]string)
	headers["Accept"] = "application/json"
	headers["Content-Type"] = "application/json"
	headers["Authorization"] = id
	logger.Println("[INFO] Inside PutServiceGroup")
	payloadBytes, err := json.Marshal(inst)
	logger.Println("[INFO] input payload bytes - " + string((payloadBytes)))
	if err != nil {
		logger.Println("[INFO] Marshalling failed with error ", err)
	}

	resp, err := DoHttp("PUT", "https://"+host+"/axapi/v3/slb/service-group/"+name, bytes.NewReader(payloadBytes), headers)

	if err != nil {
		logger.Println("The HTTP request failed with error ", err)
		
	} else {
		data, _ := ioutil.ReadAll(resp.Body)
		var m ServiceGroup
		erro := json.Unmarshal(data, &m)
		if erro != nil {
			logger.Println("Unmarshal error ", err)
			
		} else {
			logger.Println("[INFO] GET REQ RES..........................", m)
			
		}
	}
	
} 

func DeleteServiceGroup(id string, name string, host string) error { 

	logger := util.GetLoggerInstance()

	var headers = make(map[string]string)
	headers["Accept"] = "application/json"
	headers["Content-Type"] = "application/json"
	headers["Authorization"] = id
	logger.Println("[INFO] Inside DeleteServiceGroup")
	
	resp, err := DoHttp("DELETE", "https://"+host+"/axapi/v3/slb/service-group/"+name, nil, headers)

	if err != nil {
		logger.Println("The HTTP request failed with error ", err)
		return err
	} else {
		data, _ := ioutil.ReadAll(resp.Body)
		var m ServiceGroup
		erro := json.Unmarshal(data, &m)
		if erro != nil {
			logger.Println("Unmarshal error ", err)
			return err
		} else {
			logger.Println("[INFO] GET REQ RES..........................", m)
			
		}
	}
	return nil
} 

