import argparse
import requests
import subprocess
import json
import urllib.parse
import pprint


def parse_command_line():
    """Parse the command line."""
    parser = argparse.ArgumentParser(description="Send requests to a Jupyter server")
    parser.add_argument('verb', help="HTTP request to use.")
    parser.add_argument('endpoint', help="API Endpoint.")
    parser.add_argument('--port', default=8888, type=int, help="Port number.")
    args = parser.parse_args()
    return args

def get_running_notebooks():
    """Get running notebook server data.
    
    Returns
    -------
    data : dict
        Keys are ports and values are server data.
    """
    output = subprocess.run(
        ['jupyter', 'notebook', 'list', '--json'],
        capture_output=True,
        text=True
    )
    
    # Return Error
    if output.returncode != 0:
        print(out.stderr)
        return
    elif output.stdout is None:
        return 

    text = output.stdout.strip()
    server_list = text.split('\n')

    # Convert to data
    data = {}
    for server in server_list:
        server = json.loads(server)
        data[server['port']] = server
    return data


class JupyterRequester(object):
    """
    """
    def __init__(self, port):
        # Set the port number
        self.port = port
        # Get servers
        server_list = get_running_notebooks()
        server = server_list[self.port]        
        # Get token
        self.token = server['token']
        # Get url
        self.url = server['url']

    def get_path(self, endpoint):
        """Get path."""
        return urllib.parse.urljoin(self.url, endpoint)

    def request(self, verb, endpoint, params={}, *args, **kwargs):
        """"""
        # Add api token to params
        params.update({
            'token': self.token
        })

        method = getattr(requests, verb)
        r = method(self.get_path(endpoint), params=params, *args, **kwargs)
        r.raise_for_status()
        
        try:
            return r.json() 
        except json.decoder.JSONDecodeError:
            return None

    def get(self, endpoint, *args, **kwargs):
        """"""
        return self.request('get', endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        """"""
        return self.request('post', endpoint, *args, **kwargs)

    def put(self, endpoint, *args, **kwargs):
        """"""
        return self.request('out', endpoint, *args, **kwargs)

    def delete(self, endpoint, *args, **kwargs):
        """"""
        return self.request('delete', endpoint, *args, **kwargs)


def main():
    """Main call"""
    args = parse_command_line()
    requester = JupyterRequester(port=args.port)
    
    verb = getattr(requester, args.verb)
    out = verb(args.endpoint)

    pprint.pprint(
        out,
        indent=2
    )

if __name__ == "__main__":

    main()