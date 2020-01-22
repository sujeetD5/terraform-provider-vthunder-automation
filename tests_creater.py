
def main(func_name, config_name, resource_attrs, test_check_func='', check_destroy=True):

	if check_destroy:
		destroy_block = "CheckDestroy: testCheck{func_name}Destroyed,".format(func_name=func_name)
	else:
		destroy_block = ''
	resource_test_check = str()
	for attr in resource_attrs[1]:
		resource_test_check += '\t\t\t\t\tresource.TestCheckResourceAttr({attr_0}, {attr}),\n'.format(attr_0=resource_attrs[0], attr=attr)


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
	print(code_block)

if __name__ == '__main__':
	func_name = "VrrpCommon"
	config_name = "VRRP_COMMON"
	test_check_func = ""
	check_destroy = False
	resource_attrs = ['"vthunder_vrrp_common.vrrp_common"', ['"set_id", "1"', '"device_id", "1"', '"action", "enable"']]

	main(func_name, config_name, resource_attrs, test_check_func, check_destroy)