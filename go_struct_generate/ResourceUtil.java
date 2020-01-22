package util;

import org.json.JSONArray;
import org.json.JSONObject;

public class ResourceUtil {

	static StringBuilder sb = new StringBuilder();
	static StringBuilder data = new StringBuilder();

	public static void main(String[] args) {

		// JSONObject jo = (JSONObject) new
		// JSONObject(Jsons.VIRTUAL_SERVER).get("virtual-server");
//		JSONObject jo = (JSONObject) new JSONObject(Jsons.SERVICE_GROUP).get("service-group");
//		JSONObject jo = (JSONObject) new JSONObject(Jsons.SERVERS).get("server");
//		JSONObject jo = (JSONObject) new JSONObject(Jsons.IP).get("ip");
//		JSONObject jo = (JSONObject) new JSONObject(Jsons.OP_ETH).get("ethernet");
//		JSONObject jo = (JSONObject) new JSONObject(Jsons.RIB_ROUTE).get("rib");
//		JSONObject jo = (JSONObject) new JSONObject(Jsons.VRRP_COMMON).get("common");
		// JSONObject jo = (JSONObject) new JSONObject(Jsons.VRRP_VRID).get("vrid");
		// JSONObject jo = (JSONObject) new
		// JSONObject(Jsons.VRRP_PEER_GROUP).get("peer-group");
		// JSONObject jo = (JSONObject) new JSONObject(Jsons.IMPORT).get("import");
		// JSONObject jo = (JSONObject) new JSONObject(Jsons.REBOOT).get("reboot");
		// JSONObject jo = (JSONObject) new
		// JSONObject(Jsons.DNS_PRIMARY).get("primary");
		// JSONObject jo = (JSONObject) new
		// JSONObject(Jsons.SESSION_SYNC).get("session-sync");
		// JSONObject jo = (JSONObject) new JSONObject(Jsons.GLM).get("glm");
		// JSONObject jo = (JSONObject) new JSONObject(Jsons.CONF_SYNC).get("sync");
		// JSONObject jo = (JSONObject) new
		// JSONObject(Jsons.HARMONY_CONTROLLER_PROFILE).get("profile");
//		JSONObject jo = (JSONObject) new JSONObject(Jsons.OVERLAY_TUNNEL_OPTIONS).get("options");
		JSONObject jo = (JSONObject) new JSONObject(Jsons.OVERLAY_TUNNEL_VTEP).get("vtep");

		for (String key : jo.keySet()) {
			eval(key, jo.get(key));
		}

		sb.append("Schema: map[string]*schema.Schema{ \n" + data + "},");

		System.out.println(sb);

	}

	private static void eval(String key, Object obj) {
		key = key.contains("-") ? key.replace("-", "_") : key;
		if (obj instanceof JSONObject) {
			JSONObject jo = (JSONObject) obj;
			data.append("\"" + key + "\": {\n" + "Type: schema.TypeList,\n" + "Optional: true,\n" + "MaxItems: 1,\n"
					+ "Elem: &schema.Resource{\n" + "Schema: map[string]*schema.Schema{\n");

			for (String k : jo.keySet()) {
				eval(k, jo.get(k));
			}

			data.append("}, \n }, \n }, \n");

		} else if (obj instanceof JSONArray) {
			JSONArray ja = (JSONArray) obj;

			for (int i = 0; i < ja.length(); i++) {
				if (ja.get(i) instanceof JSONObject) {
					data.append("\"" + key + "\": {\n" + "Type: schema.TypeList,\n" + "Optional: true,\n"
							+ "Elem: &schema.Resource{\n" + "Schema: map[string]*schema.Schema{\n");
					JSONObject jo = (JSONObject) ja.get(i);
					for (String k : jo.keySet()) {
						eval(k, jo.get(k));
					}
					data.append("}, \n }, \n }, \n");
				} else {
					String elem = ja.get(i) instanceof Integer ? "&schema.Schema{Type: schema.TypeInt},\n"
							: (ja.get(i) instanceof String ? "&schema.Schema{Type: schema.TypeString},\n" : "");

					data.append(
							"\"" + key + "\": {\n" + "Type: schema.TypeList,\n" + "Optional: true,\n" + elem + "\n");

					data.append("}, \n");
				}

			}

		} else {
			String type = obj instanceof Integer ? "schema.TypeInt"
					: (obj instanceof String ? "schema.TypeString" : "");

			data.append("\"" + key + "\":{\n Type:" + type + ",\n Optional: true,\n Description: \"\",\n }, \n");
		}
	}

}
