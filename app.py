import sys
import json
from github import Github
from flask import Flask
import yaml

#instantiate class Github to use API
g = Github()
argrepo = ''
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Dockerized Flask App!!"

@app.route("/v1/<filename>")
def get_config(filename):
    repo = g.get_repo(argrepo)
    configfilename = filename.rsplit(".", 1)[0]
    invalidfile = 'Not a valid config file'
    filecontent = ''
    checkymlflag = ''
    if filename.endswith('.yml') or filename.endswith('.json'):
        try:
            filecontent = repo.get_file_contents("/" + filename)
            return filecontent.decoded_content
        except:
            if filename.endswith('.json'):
                checkymlflag = 'Y'
            else:
                return invalidfile
    else:
        return invalidfile
    if checkymlflag == 'Y':
        try:
            ymlContent = repo.get_file_contents("/" + configfilename + ".yml")
            return json.dumps(yaml.load(ymlContent.decoded_content), sort_keys=True, indent=2)
        except:
            return invalidfile
if __name__ == '__main__':
    # argrepo = 'SnehaVM/cmpe273-assignment1'
    # app.run(debug=True, host='0.0.0.0')
    if len(sys.argv) > 1:
        argrepo = sys.argv[1]
        argrepo = argrepo.replace('https://github.com/', '')
        app.run(debug=True, host='0.0.0.0')
    else:
        print "Please enter the url"
