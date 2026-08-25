from typing import Literal


class JNJUtilities:

    @staticmethod
    def getHanaCredentialsFromEnvironment():
        import os

        hana_host =     JNJUtilities.getRequiredEnvironmentValue("HANA_HOST")
        hana_user =     JNJUtilities.getRequiredEnvironmentValue("HANA_USER")
        hana_password = JNJUtilities.getRequiredEnvironmentValue("HANA_PASSWORD")
            
            
        hana_proc_schema =  os.environ.get('HANA_PROC_SCHEMA',  'JNJ_FINANCE')
        hana_proc_name =    os.environ.get('HANA_PROC_NAME',    'DATA_RETRIEVAL_TOOL_JNJ_FINANCE')

        return hana_host, hana_user, hana_password, hana_proc_schema, hana_proc_name

    @staticmethod
    def getMcpServerPropsFromEnvironment():
        import os
        mcp_server_name   = os.environ.get('MCP_SERVER_NAME','hana-agent-mcp-llm')
        mcp_server_host   = os.environ.get('MCP_SERVER_HOST','0.0.0.0')
        mcp_server_port   = int(os.environ.get('PORT',     8080))
        mcp_context_path  = os.environ.get('MCP_SERVER_CONTEXT_PATH', '/mcp')
        mcp_transport     = Literal[os.environ.get('MCP_SERVER_TRANSPORT',    'http')]
        
        return mcp_server_name, mcp_server_host, mcp_server_port, mcp_transport, mcp_context_path

    @staticmethod
    def getHanaCredentialsFromInput():
        import getpass

        hana_host = input("Enter HANA host: ")
        hana_user = input("Enter HANA user: ")
        hana_password = getpass.getpass("Enter HANA password: ")

        return hana_host, hana_user, hana_password

    @staticmethod
    def getRequiredEnvironmentValue(key):
        import os

        value = os.environ.get(key)
        if value == None:
            raise Exception(f"Environment variable {key} is not set, but it is required.")
        return value
