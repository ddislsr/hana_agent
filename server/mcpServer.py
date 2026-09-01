from __future__ import annotations
import logging, json
import os
import sys
import time
import logging
#from fastmcp.client.transports import http
#from fastmcp.server.server import Transport
from hana_ml import ConnectionContext
#from hana_ai.tools.toolkit import HANAMLToolkit
from mcp.server.mcpserver import MCPServer,Context



from utilities import JNJUtilities

try:
    from dotenv import load_dotenv
    _env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(_env_path):
        load_dotenv(_env_path)
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger()

mcp_server_name, mcp_server_host, mcp_server_port, mcp_transport, mcp_context_path = JNJUtilities.getMcpServerPropsFromEnvironment()
hana_host, hana_user, hana_password, hana_proc_schema , hana_proc_name= JNJUtilities.getHanaCredentialsFromEnvironment()

mcp = MCPServer(name=mcp_server_name,  instructions="")

def main(): 

    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
 
    #toolkit = HANAMLToolkit(connection_context=cc)
    
    # toolkit.launch_mcp_server(
    #    server_name  = mcp_server_name,
    #    host         = mcp_server_host,
    #    port         = mcp_server_port,
    #    transport    = str(mcp_transport),
    #    max_retries=5
    # )

    mcp.run(transport="streamable-http", stateless_http=True, host=mcp_server_host, port=mcp_server_port)
    logging.info("MCP server is running. Press Ctrl+C to stop.")
  
  
    try:
        # Keep main thread alive while server runs in background
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutdown requested. Exiting...")


@mcp.tool()
def get_data_discoagent(query: str ) -> dict:
    
    ctx = build_connection_context()
    conn = ctx.connection
    logging.info("Connecting to HANA at %s", ctx.address)            
    print("Connecting to HANA at %s", ctx.address) 
    cursor = conn.cursor()
    result =cursor.callproc(hana_proc_schema +'.'+ hana_proc_name,(json.dumps({"query": query}),None))
    print({"response":json.dumps(result, default=str)})
    cursor.close()
    
    return {"result": result}




def build_connection_context():

    params = {
        "address": hana_host,
        "port": 443,
        "user": hana_user,
        "password": hana_password
    }
    params["encrypt"] = True
    params["sslValidateCertificate"] = True
    return ConnectionContext(**params)



if __name__ == "__main__":
  main()
    
